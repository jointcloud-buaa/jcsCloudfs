# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/6/21 14:48'

from datalog_operation.datalog_monitor import DatalogMonitor
from metadata.file_info import MetadataFileInfo
from config.cloud_information import CloudInformation
import copy
import os
from config.configuration import CONFIG
from cloud_interface.cloud_interface import CloudInterface
import datetime
from manager.manager_interface import ManagerInterface
from config.configuration import CONFIG

class AdjustmentTruth(object):
    """
    真实数据获取，真实执行动态调整操作
    """

    def __init__(self):
        self.timedelta_daily = 1  # 侧重于每天下载量多的文件尽快调整，统计1天内文件下载模式
        self.timedelta_monthly = 30  # 侧重于每个月的下载量少的文件调整，统计30天内文件下载模式
        self.dynamic_path = CONFIG['test_file_path']  # 动态调整数据块的下载路径

    def check_file_exists(self, file_key):
        return MetadataFileInfo().check_file_exists(file_key)


    def get_file_download_mode_daily(self):
        """
        统计一天内，文件下载模式
        包括：文件名，下载的jcsproxy，下载次数
        :return:
        """
        now = datetime.datetime.now()
        start_time = now - datetime.timedelta(days=self.timedelta_daily)
        end_time = now
        data_monitor = DatalogMonitor()
        file_download_mode = data_monitor.count_download_file(start_time, end_time)  # 如果一天内没有文件下载，返回{}
        # print "\n获取每天的下载模式", file_download_mode
        return file_download_mode

    def get_file_download_mode_monthly(self, file_key):
        """
        统计一个月内，一个文件下载模式
        包括：文件名，下载的jcsproxy，下载次数
        :return:
        """
        now = datetime.datetime.now()
        start_time = now - datetime.timedelta(days=self.timedelta_monthly)
        end_time = now
        data_monitor = DatalogMonitor()
        file_download_mode = data_monitor.count_download_file(start_time, end_time, file_key)
        if len(file_download_mode) == 0:  # 如果此文件一个月内没有下载，返回{"file_key":{}}
            file_download_mode = {}
            file_download_mode[file_key] = {}
        # print "\n获取每月的下载模式",file_download_mode
        return file_download_mode

    def list_all_dir_name(self, dir_path=""):
        metadata_file_info = MetadataFileInfo()
        list_all_dir_name = metadata_file_info.list_all_dir_name(dir_path)['result']
        # [] # 返回空
        # [{'isdir': True, 'file_name': 'liuyf_test', 'children': [{'isdir': False, 'file_name': 'remote.txt'}]}]
        return list_all_dir_name

    def get_file_metadata(self, file_key):
        """
        获取文件元数据信息
        :param file_key:
        :return:
        """
        metadata_file_info = MetadataFileInfo()
        file_info_res = metadata_file_info.get_file_info(file_key)
        file_info = file_info_res["result"]
        # 计算动态调整策略需要用到的一些值
        res_dict = {}
        res_dict['file_key'] = file_key
        res_dict['file_size'] = file_info['file_size']
        # print "\nfile_size**************\n",res_dict['file_size']
        res_dict['block_size'] = file_info['block_size']
        res_dict['storage_time'] = file_info['optimizer_res']['storage_time']
        res_dict['jcsproxy_request_features'] = file_info['optimizer_res']['jcsproxy_request_features']
        # res_dict['placement'] = file_info['optimizer_res']['placement']
        res_dict['bucket_name_list'] = file_info['optimizer_res']['bucket_name_list']
        res_dict['jcsproxy_bucket_name_list'] = file_info['optimizer_res']['jcsproxy_bucket_name_list']
        res_dict['cloud_block_path_dict'] = file_info['cloud_block_path_dict']
        # MyPrint().myprintdict(res_dict, "file_metadata")
        return res_dict

    ###########################################################

    def data_block_migration(self, file_key, file_request_features, new_policy, cloud_block_path_dict):
        """
        纠删码块动态迁移
        :param file_metadata:
        :param migration_diff:
        :param new_policy:
        :return:
        """
        print "data_block_migration"
        # download_bucket_name_list = migration_diff.keys()
        # upload_bucket_name_list = migration_diff.values()
        # download_local_block_path = []
        # download_cloud_block_path = []
        # for old_bucket_name in migration_diff:
        #     block_name = self.get_file_name(cloud_block_path_dict[old_bucket_name])
        #     local_block_path = os.path.join(self.dynamic_path, block_name)
        #     download_local_block_path.append(local_block_path)
        #     download_cloud_block_path.append(cloud_block_path_dict[old_bucket_name])
        #
        # self.get_migration_file(download_bucket_name_list, download_cloud_block_path, download_local_block_path)  # 下载
        # self.put_migration_file(upload_bucket_name_list, download_cloud_block_path, download_local_block_path)  # 上传
        # self.update_metadata(file_key, new_policy, migration_diff)  # 更新元数据
        # self.delete_migration_file(download_bucket_name_list, download_cloud_block_path, download_local_block_path)  # 删除

        str_list = file_key.split('/', 1)
        user_name = str_list[0]
        cloud_file_path = str_list[1]
        local_file_path = CONFIG['test_file_path']+'dynamic_file'
        manager_operate = ManagerInterface()
        manager_operate.get_file(user_name, cloud_file_path, local_file_path)
        manager_operate.delete_file(user_name, cloud_file_path)
        manager_operate.put_file(user_name, cloud_file_path, local_file_path, jcsproxy_request_features=file_request_features)
        if os.path.exists(local_file_path):
            os.remove(local_file_path)





    def get_migration_file(self, download_bucket_name_list, download_cloud_block_path, download_local_block_path):
        print "下载迁移数据块"
        for i, download_bucket_name in enumerate(download_bucket_name_list):
            cloud_account = CloudInformation().get_cloud_account_from_bucket_name(download_bucket_name)
            cloud_operate = CloudInterface(cloud_account)
            cloud_operate.get_file(download_cloud_block_path[i], download_local_block_path[i])

    def put_migration_file(self, upload_bucket_name_list, download_cloud_block_path, download_local_block_path):
        print "上传迁移数据块"
        for i, upload_bucket_name in enumerate(upload_bucket_name_list):
            cloud_account = CloudInformation().get_cloud_account_from_bucket_name(upload_bucket_name)
            cloud_operate = CloudInterface(cloud_account)
            cloud_operate.put_file(download_cloud_block_path[i], download_local_block_path[i])

    def delete_migration_file(self, download_bucket_name_list, download_cloud_block_path, download_local_block_path):
        print "删除迁移数据块"
        for i, download_bucket_name in enumerate(download_bucket_name_list):
            cloud_account = CloudInformation().get_cloud_account_from_bucket_name(download_bucket_name)
            cloud_operate = CloudInterface(cloud_account)
            cloud_operate.delete_file(download_cloud_block_path[i])
        print "删除本地文件"
        for local_block_path in download_local_block_path:
            os.remove(local_block_path)

    def get_file_name(self, cloud_file_key):
        file_split = str.split(cloud_file_key.encode('utf-8'), "/")
        return file_split[len(file_split) - 1]


    ##########################################################

    def update_metadata(self, file_key, change_policy, migration_diff=None):
        """
        更新文件元数据信息
        :param file_key:
        :param change_policy:
        :param new_cloud_block_path_dict:
        :return:
        """
        print "update_metadata"
        metadata_file_info = MetadataFileInfo()
        file_info = metadata_file_info.get_file_info(file_key)["result"]
        bucket_name_list = file_info['optimizer_res']['bucket_name_list']
        cloud_block_path_dict = file_info['cloud_block_path_dict']
        # 如果数据放置策略不同，需要更新cloud_block_path_dict
        if not migration_diff == None:
            cloud_block_path_dict = self.update_cloud_block_path_dict(cloud_block_path_dict, migration_diff)

        # print "更新文件元数据信息"
        # MyPrint().myprintdict(file_info, "old_info")
        file_info['cloud_block_path_dict'] = cloud_block_path_dict
        file_info['optimizer_res'] = change_policy
        # MyPrint().myprintdict(file_info, "new_info")
        MetadataFileInfo().create_file_info(file_key, file_info, True)  # 重新写入


    def update_cloud_block_path_dict(self, cloud_block_path_dict, migration_diff):
        """
        根据替换节点，重新
        :param old_cloud_block_path_dict:
        :param old_bucket_name_list:
        :param new_bucket_name_list:
        :return:
        """
        for old_bucket_name, new_bucket_name in migration_diff.iteritems():
            cloud_block_path_dict[new_bucket_name] = copy.deepcopy(cloud_block_path_dict[old_bucket_name])
            cloud_block_path_dict.pop(old_bucket_name)
        return cloud_block_path_dict

    def get_list_diff(self, old_list, new_list):
        list_same = set(old_list) & set(new_list)
        old_diff = set(old_list) - list_same
        new_diff = set(new_list) - list_same
        old_diff = list(old_diff)
        new_diff = list(new_diff)
        diff_dict = {}
        for i, old_one in enumerate(old_diff):
            diff_dict[old_one] = new_diff[i]
        return diff_dict


