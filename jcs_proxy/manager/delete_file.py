# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/1/17 16:26'

from cloud_interface.cloud_interface import CloudInterface
from metadata.file_info import MetadataFileInfo
from metadata.cloud_bucket_info import MetadataCloudBucketInfo
from tools.get_func_time import GetFuncTime
from tools.get_dict_res import GetDictRes
from config.cloud_information import CloudInformation
from config.configuration import CONFIG

class DeleteFile(object):
    """
    删除文件操作
    """
    def __init__(self):
        self.jcsproxy_area = CONFIG['jcsproxy_area']

    def delete_file(self, user_name, cloud_file_path, check_insert_waiting_delete_file = True):
        """
        删除文件
        :param user_name: str, 用户名
        :param cloud_file_path: str, 云端文件路径
        :return: dict_res
        """
        cloud_file_key = user_name + "/" + cloud_file_path
        # 1.获取用户文件信息，及存储云端信息
        metadata_file_info = MetadataFileInfo()
        file_info = metadata_file_info.get_file_info(cloud_file_key)["result"]
        # 2.删除云存储端文件
        cloud_block_path_dict, cloud_operate_res_list, cloud_operate_time_list = self.delete_file_from_cloud(file_info, check_insert_waiting_delete_file)
        # 3.删除文件元信息
        delete_file_info_res = metadata_file_info.delete_file_info(cloud_file_key)
        # 4.插入数据操作记录
        # datalog_info = PutFileManager().build_datalog_info(cloud_file_key, "delete_file",
        #                                                    cloud_bucket_list, cloud_operate_time_list, self.proxy_name)
        # insert_datalog_res = DataLog().insert_operdata(datalog_info)
        # 返回信息
        dict_res = GetDictRes().get_dict_res()
        dict_res["result"]["file_operate"] = "delete_file"
        dict_res["result"]["file_info"] = file_info
        dict_res["result"]["cloud_operate_res"] = cloud_operate_res_list
        dict_res["result"]["cloud_operate_time_res"] = cloud_operate_time_list
        dict_res["result"]["delete_bucket_file_dict"] = cloud_block_path_dict
        return dict_res

    def delete_file_from_cloud(self, file_info, check_insert_waiting_delete_file):
        cloud_block_path_dict = file_info['cloud_block_path_dict']
        # optimizer_res = file_info['optimizer_res']
        # bucket_name_list = optimizer_res['bucket_name_list']

        # 检查云是否可用，是否可删除云中的文件。不可删除的文件保存下来
        if check_insert_waiting_delete_file ==  True:
            cloud_block_path_dict = self.check_avalible_bucket_list(cloud_block_path_dict)

        # 删除云上的纠删码块
        cloud_operate_res_list = []
        cloud_operate_time_list = []
        for bucket_name, cloud_block_path in cloud_block_path_dict.iteritems():
            cloud_account = CloudInformation().get_cloud_account_from_bucket_name(bucket_name)
            if cloud_account == None:  # 删除故障云中文件的情况，先不进行处理，以后定期统一处理没有被索引的失效文件
                continue
            cloud_operate = CloudInterface(cloud_account)
            cloud_operate_res, delete_file_time = GetFuncTime().get_func_time(cloud_operate.delete_file,
                                                                              (cloud_block_path, ))
            cloud_operate_res_list.append(cloud_operate_res)
            cloud_operate_time_list.append(delete_file_time)
        return cloud_block_path_dict, cloud_operate_res_list, cloud_operate_time_list

    def check_avalible_bucket_list(self, bucket_file_dict):
        # cloud_block_path_dict (bucket_file_dict)
        # {u'jcsproxy-aliyun-qingdao-low': 'liuyf_test/liuyf/remote.txt.3_5.fec',
        #  u'jcsproxy-aliyun-huhehaote-low': 'liuyf_test/liuyf/remote.txt.0_5.fec',
        #  u'jcsproxy-aliyun-zhangjiakou': 'liuyf_test/liuyf/remote.txt.4_5.fec',
        #  u'jcsproxy-aliyun-huhehaote': 'liuyf_test/liuyf/remote.txt.2_5.fec',
        #  u'jcsproxy-aliyun-beijing': 'liuyf_test/liuyf/remote.txt.1_5.fec'}
        # 检查云是否可用，是否可删除云中的文件。不可删除的文件保存下来

        cloud_bucket_name_list = CloudInformation().get_cloud_bucket_name_list()
        # 找到不可用的bucket_name
        fault_list = []
        for bucket_name, file_key in bucket_file_dict.iteritems():
            if bucket_name not in cloud_bucket_name_list:
                new_dict = {}
                new_dict[bucket_name] = file_key
                fault_list.append(new_dict)
        if len(fault_list) == 0:
            return bucket_file_dict
        # 不可用的bucket_name和file_key的dict记录到zk中
        MetadataCloudBucketInfo().insert_waiting_delete_file(fault_list)
        # 删除不可用的bucket_name
        for fault_dict in fault_list:
            for bucket_name in fault_dict:
                bucket_file_dict.pop(bucket_name)
        return bucket_file_dict


if __name__ == '__main__':
    print("manager delete file")
    manager_delete_file = DeleteFile()

    user_name = "liuyf_test"
    cloud_file_path = "dir/remote.txt"

    res = manager_delete_file.delete_file(user_name, cloud_file_path)
    print(res)






