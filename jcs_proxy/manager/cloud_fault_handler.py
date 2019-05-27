# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/11/2 00:25'

from metadata.cloud_bucket_info import MetadataCloudBucketInfo
from metadata.file_info import MetadataFileInfo
from config.cloud_information import CloudInformation
from cloud_interface.cloud_interface import CloudInterface
from tools.get_func_time import GetFuncTime
import os
from config.configuration import CONFIG
import uuid
from manager_interface import ManagerInterface


class CloudFaultHandler(object):
    """
    数据故障恢复
    """
    def __init__(self):
        self.data_recovery_path = CONFIG['data_recovery_path']

    def waiting_delete_file_handler(self, bucket_name):
        """
        bucket_name恢复，删除与其相关的waiting_delete_file_list中待删除的数据块
        临时故障云 -> 可用云
        超时故障云 -> 可用云
        :param bucket_name:
        :return:
        """
        cloud_bucket_operate = MetadataCloudBucketInfo()
        waiting_delete_file_list = cloud_bucket_operate.get_waiting_delete_file_by_bucket_name(bucket_name)
        self.myprint_list(waiting_delete_file_list, "待删除文件数据块列表")
        # 删除云上的数据块
        cloud_operate_res_list = []
        cloud_operate_time_list = []
        for waiting_delete_file_dict in waiting_delete_file_list:
            for bucket_name in waiting_delete_file_dict:
                cloud_block_path = waiting_delete_file_dict[bucket_name]
                cloud_account = CloudInformation().get_cloud_account_from_bucket_name(bucket_name)
                if cloud_account == None:  # 删除故障云中文件的情况，先不进行处理，以后定期统一处理没有被索引的失效文件
                    continue
                cloud_operate = CloudInterface(cloud_account)
                cloud_operate_res, delete_file_time = GetFuncTime().get_func_time(cloud_operate.delete_file,
                                                                                  (cloud_block_path, ))
                cloud_operate_res_list.append(cloud_operate_res)
                cloud_operate_time_list.append(delete_file_time)
        self.myprint_list(cloud_operate_res_list, "删除数据块结果")
        self.myprint_list(cloud_operate_time_list, "删除数据块耗时")


    def data_recovery_handler(self, bucket_name, bucket_list_num):
        """
        遍历文件数据恢复
        :param bucket_name:
        :param bucket_list_num:  可用云列表1/临时故障云列表2/超时故障云类表3/待删除云列表4
        :return:
        """
        # 1.递归获取所有的 bucket_file_dict中存在==bucket_name的  file_key
        # 2.数据恢复（bucket_name是否还存在故障列表中）
        #   下载文件
        #   删除文件（判断文件是否存在）
        #   重新上传
        # 注意删除文件有个字段值判断，check_insert_waiting_delete_file
        #   如果bucket_list_num == 4，是待删除云，check_insert_waiting_delete_file=False, 不记录waiting_delete_file
        #   如果bucket_list_num == 3，是超时故障云，check_insert_waiting_delete_file=True, 记录waiting_delete_file

        # file_block_list  # 深度遍历提取file_key和bucket_file_dict信息
        file_info_all = MetadataFileInfo().list_all_dir_info("")['result']
        file_block_list = []
        self.deep_file_info(file_info_all, file_block_list)
        self.myprint_list(file_block_list, "所有文件的数据块存储列表：")
        # delete_file_key_list  # 应该进行数据恢复的文件
        delete_file_key_list = self.filter_file_info(bucket_name, file_block_list)
        self.myprint_list(delete_file_key_list, "待数据恢复的文件列表：")
        # 数据恢复，下载，删除，重新上传
        check_insert_waiting_delete_file = True
        if bucket_list_num == 4:
            check_insert_waiting_delete_file =False
        for file_key in delete_file_key_list:
            str_list = file_key.split("/", 1)
            user_name = str_list[0]
            cloud_file_path = str_list[1]
            local_file_path = os.path.join(self.data_recovery_path, str(uuid.uuid1()))
            print "进行一个文件的数据恢复：", file_key
            self.download_delete_upload(user_name, cloud_file_path, local_file_path, check_insert_waiting_delete_file)


    def download_delete_upload(self, user_name, cloud_file_path, local_file_path, check_insert_waiting_delete_file):
        manager_operate = ManagerInterface()
        res = manager_operate.get_file(user_name, cloud_file_path, local_file_path)
        print "data recovery, 下载文件", res
        res = manager_operate.delete_file(user_name, cloud_file_path, check_insert_waiting_delete_file)
        print "data recovery, 删除文件", res   # 更好的应该版本控制，不应该直接删除
        res  = manager_operate.put_file(user_name, cloud_file_path, local_file_path, True)
        print "data recovery, 上传文件", res
        print res['result']['file_info']['cloud_block_path_dict'].keys()
        if os.path.exists(local_file_path):
            os.remove(local_file_path)
            print "data recovery, 删除本地文件"


    def filter_file_info(self, bucket_name, file_block_list):
        """
        根据bucket_name过滤
        :param bucket_name:
        :return:
        """
        delete_file_key_list = []
        for file_block_one in file_block_list:
            file_key = file_block_one['file_key']
            bucket_file_dict = file_block_one['bucket_file_dict']
            for bucket_name_one in bucket_file_dict:
                if bucket_name_one == bucket_name:
                    delete_file_key_list.append(file_key)
        return delete_file_key_list


    def deep_file_info(self, file_info_all, file_block_list, now_dir_path=""):
        """
        深度遍历所有文件，去处file_key，
        :param list_all:
        :param now_dir_path:
        :return:
        """
        for file_info_one in file_info_all:
            file_path = os.path.join(now_dir_path, file_info_one['file_name'])
            if file_info_one['isdir'] == True:
                self.deep_file_info(file_info_one['children'], file_block_list, file_path)
            else:
                if file_info_one.has_key('file_key') and file_info_one.has_key('cloud_block_path_dict'):
                    file_key = file_info_one['file_key']
                    bucket_file_dict = file_info_one['cloud_block_path_dict']
                    new_dict = {}
                    new_dict['file_key'] = file_key
                    new_dict['bucket_file_dict'] = bucket_file_dict
                    file_block_list.append(new_dict)

    def myprint_list(self, printlist, printstr = ""):
        print printstr
        for i in range(len(printlist)):
            print printlist[i]

# list all dir name
# {'status': 0, 'result': [{'isdir': True, 'file_name': 'liuyf_test', 'children': [{'isdir': True, 'file_name': 'liuyf', 'children': [{'isdir': False, 'file_name': 'remote.txt'}]}]}, {'isdir': True, 'file_name': 'liuyf', 'children': [{'isdir': False, 'file_name': 'test.txt'}, {'isdir': True, 'file_name': 'dir', 'children': [{'isdir': False, 'file_name': 'test2.pdf'}]}]}]}

# file_block_list   # 深度遍历提取file_key和bucket_file_dict信息
# [{'bucket_file_dict': {u'jcsproxy-aliyun-qingdao-low': u'liuyf_test/liuyf/remote.txt.3_5.fec', u'jcsproxy-aliyun-huhehaote-low': u'liuyf_test/liuyf/remote.txt.0_5.fec', u'jcsproxy-aliyun-zhangjiakou': u'liuyf_test/liuyf/remote.txt.4_5.fec', u'jcsproxy-aliyun-huhehaote': u'liuyf_test/liuyf/remote.txt.2_5.fec', u'jcsproxy-aliyun-beijing': u'liuyf_test/liuyf/remote.txt.1_5.fec'}, 'file_key': u'liuyf_test/liuyf/remote.txt'}]

# delete_file_key_list  # 应该进行数据恢复的文件
# [liuyf_test/liuyf/remote.txt]

if __name__ == '__main__':
    cloud_fault_handler = CloudFaultHandler()
    cloud_fault_handler.data_recovery_handler("jcsproxy-aliyun-beijing", 4)