# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/6/5 16:26'

import json
from tools.get_dict_res import GetDictRes
from metadata.file_info import MetadataFileInfo
from metadata.user_info import MetadataUserInfo
from metadata.zookeeper_client import ZookeeperClient
from config.cloud_information import CloudInformation
from config.configuration import CONFIG
import copy

class UsedStorge(object):
    def __init__(self):
        self.metadata_file_info = MetadataFileInfo()

    def get_file_info(self, user_name, cloud_file_path):
        """
        获取文件信息
        :param user_name: str, 用户名
        :param cloud_file_path: str, 云端文件路径
        :return: dict_res
        """
        cloud_file_key = user_name + "/" + cloud_file_path
        dict_res = MetadataFileInfo().check_file_exists(cloud_file_key)
        if dict_res["status"] == 0:
            dict_res = MetadataFileInfo().get_file_info(cloud_file_key)
        return dict_res

    ###########################################################################

    def user_used_storage(self, user_name):
        """
        统计某个用户存储量大小（某个用户在所有云地域上的存储量，和用户的总存储量）
        :param user_name:
        :return:
        """
        # 初始化用户在每个云地域存储量为0
        cloud_bucket_list = CloudInformation().get_cloud_bucket_list()
        bucket_used_storage = {}
        for cloud_bucket in cloud_bucket_list:
            bucket_name = cloud_bucket['bucket_name']
            bucket_used_storage[bucket_name] = 0
        # 统计用户在每个云地域的存储量之和
        # file_used_storage = 0.0   # 文件存储量
        file_used_storage = self.deep_statistics_file(bucket_used_storage, user_name)
        # 统计用户总存储量
        redundant_used_storage = 0.0  # 冗余存储量
        bucket_used_storage_simple = copy.deepcopy(bucket_used_storage)
        # 两位小数
        for bucket_name in bucket_used_storage_simple :
            bucket_used_storage_simple[bucket_name] = int(bucket_used_storage_simple[bucket_name]*100)/100.0
        for bucket_name in bucket_used_storage:
            redundant_used_storage += bucket_used_storage[bucket_name]
            if bucket_used_storage_simple[bucket_name] == 0:  # 删去0的值
                bucket_used_storage_simple.pop(bucket_name)
        # 返回值
        user_res = {}
        user_res['file_used_storage'] = file_used_storage
        user_res['redundant_used_storage'] = redundant_used_storage
        user_res['cloud_used_storage'] = bucket_used_storage_simple
        dict_res = GetDictRes().get_dict_res()
        dict_res['status'] = 0
        dict_res['result'] = user_res
        return dict_res

    def deep_statistics_file(self, bucket_used_storage, now_dir_path):
        list_dict_res = self.metadata_file_info.list_dir_name(now_dir_path)
        if list_dict_res['status'] == 1:
            return 0.0
        file_name_list = list_dict_res['result']  # 文件名列表

        file_used_storage = 0.0
        for file_name in file_name_list:
            file_path = now_dir_path+'/'+file_name
            file_info_dict_res = self.metadata_file_info.get_file_info(file_path)
            if file_info_dict_res['status'] == 1:
                continue
            if file_info_dict_res['result']['isdir'] == True:  # 如果是文件夹，则递归遍历
                file_used_storage += self.deep_statistics_file(bucket_used_storage, file_path)
                continue

            file_info = file_info_dict_res['result']
            block_size = file_info['block_size']
            file_used_storage += file_info['file_size']
            for bucket_name in file_info['optimizer_res']['bucket_name_list']:
                bucket_used_storage[bucket_name] += block_size
        return file_used_storage

    #############################################################################


    def all_users_used_storage(self):
        """
        （设想每间隔一段时间）统计所有用户存储量信息，并保存
        :return:
        """
        statistics_path_user = CONFIG['zk_file_statistics_path']+'/user'
        ZookeeperClient().delete_node_info(statistics_path_user, True)  # 删除之前存在的user统计信息

        user_name_list_res = MetadataUserInfo().list_user_name()
        if user_name_list_res['status'] == 1:
            return user_name_list_res
        user_name_list = user_name_list_res['result']
        for user_name in user_name_list:
            user_statistics = self.user_used_storage(user_name)['result']
            ZookeeperClient().create_node_info(statistics_path_user+"/"+user_name, json.dumps(user_statistics), True)



    def cloud_used_storage(self):
        """
        统计每个云地域存储量大小（所有用户在每个云地域上的存储量）
        :return:
        """
        # 路径
        statistics_path_user = CONFIG['zk_file_statistics_path'] + '/user'  # 保存用户统计信息的目录
        statistics_path_cloud = CONFIG['zk_file_statistics_path'] + '/cloud'  # 保存云地域存储信息的目录
        ZookeeperClient().delete_node_info(statistics_path_cloud, True)  # 删除之前存在的cloud统计信息

        # 初始化每个云地域存储量为0
        cloud_bucket_list = CloudInformation().get_cloud_bucket_list()
        bucket_used_storage = {}
        for cloud_bucket in cloud_bucket_list:
            bucket_name = cloud_bucket['bucket_name']
            bucket_used_storage[bucket_name] = 0
        # 所有用户在每个云地域的存储量相加
        user_name_list = MetadataUserInfo().list_user_name()['result']
        file_used_storage = 0.0
        redundant_used_storage = 0.0
        for user_name in user_name_list:
            user_used_storage = ZookeeperClient().get_node_info(statistics_path_user+'/'+user_name)['result']
            user_used_storage = json.loads(user_used_storage)
            user_cloud_used_storage = user_used_storage['cloud_used_storage']
            for bucket_name in user_cloud_used_storage:
                bucket_used_storage[bucket_name] += user_cloud_used_storage[bucket_name]
            file_used_storage += user_used_storage['file_used_storage']
            redundant_used_storage += user_used_storage['redundant_used_storage']
        bucket_used_storage_simple = copy.deepcopy(bucket_used_storage)
        for bucket_name in bucket_used_storage:
            if bucket_used_storage_simple[bucket_name] == 0:  # 删去0的值
                bucket_used_storage_simple.pop(bucket_name)
        ## 保留两个位小数
        for bucket_name in bucket_used_storage_simple:
            bucket_used_storage_simple[bucket_name] = int(bucket_used_storage_simple[bucket_name]*100)/float(100)

        # 总存储量
        # redundant_used_storage = 0
        # bucket_used_storage_simple = copy.deepcopy(bucket_used_storage)
        # for bucket_name in bucket_used_storage:
        #     redundant_used_storage += bucket_used_storage[bucket_name]
        #     if bucket_used_storage_simple[bucket_name] == 0:  # 删去0的值
        #         bucket_used_storage_simple.pop(bucket_name)
        # 写入zk中
        cloud_bucket_statistics = {}
        cloud_bucket_statistics['file_used_storage'] = file_used_storage
        cloud_bucket_statistics['redundant_used_storage'] = redundant_used_storage
        cloud_bucket_statistics['cloud_used_storage'] = bucket_used_storage_simple
        ZookeeperClient().create_node_info(statistics_path_cloud, json.dumps(cloud_bucket_statistics))


    def refresh_cloud_used_storage(self):
        self.all_users_used_storage()
        self.cloud_used_storage()
        statistics_path_cloud = CONFIG['zk_file_statistics_path'] + '/cloud'
        cloud_used_storage = ZookeeperClient().get_node_info(statistics_path_cloud)
        # print cloud_used_storage
        json_str = cloud_used_storage['result']
        cloud_used_storage['result'] = json.loads(json_str)
        return cloud_used_storage