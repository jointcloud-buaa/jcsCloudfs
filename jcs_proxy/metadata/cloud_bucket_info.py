# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/10/7 19:14'

import json
from config.singleton import Singleton
from config.configuration import CONFIG
from config.cloud_config import CLOUDCONFIG
from zookeeper_client import ZookeeperClient
from tools.get_dict_res import GetDictRes

class MetadataCloudBucketInfo(Singleton):
    """
    cloud_bucket列表
    available_bucket_list
    temporary_fault_bucket_list
    permanent_fault_bucket_list
    """
    def __init__(self):
        self.zk_operate = ZookeeperClient()
        self.user_info_path = CONFIG["zk_cloud_bucket_info_path"]
        self.avalible_bucket_list_path = self.user_info_path+"/avalible_bucket_list"
        self.temporary_fault_bucket_list_path = self.user_info_path + "/temporary_fault_bucket_list"
        self.permanent_fault_bucket_list_path = self.user_info_path + "/permanent_fault_bucket_list"
        self.remove_bucket_list_path = self.user_info_path + "/remove_bucket_list_path"
        self.waiting_delete_list_path = self.user_info_path + "/waiting_delete_file_list"
        # 第一次建立云列表
        if self._first_init:
            self._first_init = False
            cloud_bucket_list = CLOUDCONFIG["cloud_bucket_list"]
            self.zk_operate.create_node_info(self.avalible_bucket_list_path, json.dumps(cloud_bucket_list), True)
            self.zk_operate.create_node_info(self.temporary_fault_bucket_list_path, "[]", True)
            self.zk_operate.create_node_info(self.permanent_fault_bucket_list_path, "[]", True)
            self.zk_operate.create_node_info(self.remove_bucket_list_path, "[]", True)
            self.zk_operate.create_node_info(self.waiting_delete_list_path, "[]", True)

    def zk_stop(self):
        """
        关闭zookeeper连接
        :return:
        """
        self.zk_operate.zk_stop()

    def get_bucket_list_path(self, bucket_list_num):
        """
        bucket_list_num和云列表映射关系
        可用云列表1/临时故障云列表2/超时故障云类表3/待删除云列表4
        :param bucket_list_num:
        :return:
        """
        if bucket_list_num == 1:
            return self.avalible_bucket_list_path
        elif bucket_list_num == 2:
            return self.temporary_fault_bucket_list_path
        elif bucket_list_num == 3:
            return self.permanent_fault_bucket_list_path
        elif bucket_list_num == 4:
            return self.remove_bucket_list_path

    def get_waiting_delete_file_list(self):
        return self.get_bucket_list_from_path(self.waiting_delete_list_path)

    def get_bucket_list_from_path(self, bucket_list_path):
        """
        获取云列表，根据bucket_list_path
        :param cloud_bucket_list_path:
        :return:
        """
        dict_res = self.zk_operate.get_node_info(bucket_list_path)
        return json.loads(dict_res['result'])

    def get_bucket_list_from_num(self, bucekt_list_num):
        """
        获取云列表，根据bucket_list_num
        :param bucekt_list_num:
        :return:
        """
        bucket_list_path = self.get_bucket_list_path(bucekt_list_num)
        return self.get_bucket_list_from_path(bucket_list_path)


    def exchange_bucket(self, from_bucket_list_num, to_bucket_list_num, bucket_name):
        """
        在云列表之间移动bucket
        将bucket_name从from_bucket_list移动到to_bucket_list中，例如，将bucket_name从可用云设置为临时故障云
        考虑bucket_name不存在from_bucket_list中的情况
        :param from_bucket_list:
        :param to_bucket_list:
        :return:
        """

        from_bucket_list = self.get_bucket_list_from_num(from_bucket_list_num)
        to_bucket_list = self.get_bucket_list_from_num(to_bucket_list_num)

        for from_bucket_one in from_bucket_list:
            if from_bucket_one['bucket_name'] == bucket_name:
                from_bucket_list.remove(from_bucket_one)
                to_bucket_list.append(from_bucket_one)
                self.zk_operate.create_node_info(self.get_bucket_list_path(from_bucket_list_num), json.dumps(from_bucket_list), True)
                self.zk_operate.create_node_info(self.get_bucket_list_path(to_bucket_list_num), json.dumps(to_bucket_list), True)


    def insert_cloud_bucket(self, bucket_info):
        """
        插入新的云地域信息 到可用云列表
        :param bucket_info:
        :return:
        """
        # bucket_info :
        # {'cloud_name': 'aliyun', 'area_name': 'qingdao', 'storage_type': 'standard',
        #  'bucket_name': 'jcsproxy-aliyun-qingdao', 'endpoint': 'http://oss-cn-qingdao.aliyuncs.com'}
        # 先检查bucket_name不存在三个云列表中(待做)
        # 检查接口是否可用（待做）
        bucket_list = self.get_bucket_list_from_num(1)
        bucket_list.append(bucket_info)
        self.zk_operate.create_node_info(self.get_bucket_list_path(1), json.dumps(bucket_list), True)

    def remove_cloud_bucket(self, bucket_name):
        """
        从待删除云列表中删除 云地域信息
        :param bucket_info:
        :return:
        """
        bucket_list = self.get_bucket_list_from_num(4)
        for bucket_info in bucket_list:
            if bucket_info['bucket_name'] == bucket_name:
                bucket_list.remove(bucket_info)
        self.zk_operate.create_node_info(self.get_bucket_list_path(4), json.dumps(bucket_list), True)



    def insert_waiting_delete_file(self, bucket_file_dict_list):
        """
        插入云故障 不可删除的文件
        :param bucket_name_file_key_dict:
        :return:
        """
        bucket_file_list = self.get_bucket_list_from_path(self.waiting_delete_list_path)
        for bucket_file_dict in bucket_file_dict_list:
            for bucket_name_one, file_key_one in bucket_file_dict.iteritems():
                new_dict = {}
                new_dict[bucket_name_one] = file_key_one
                bucket_file_list.append(new_dict)
        self.zk_operate.create_node_info(self.waiting_delete_list_path, json.dumps(bucket_file_list), True)

    def get_waiting_delete_file_by_bucket_name(self, bucket_name):
        """
        得到某个bucket_name中未删除的文件
        :param bucket_name:
        :return:
        """
        res_list = []
        bucket_file_list = self.get_bucket_list_from_path(self.waiting_delete_list_path)
        for bucket_file_dict in bucket_file_list:
            for bucket_name_one, file_key_one in bucket_file_dict.iteritems():
                if bucket_name_one == bucket_name:
                    new_dict = {}
                    new_dict[bucket_name_one] =file_key_one
                    res_list.append(new_dict)
        return res_list

    def remove_waiting_delete_file(self, bucket_file_dict_list):
        """
        删除某个waiting_delete_list中的文件 [{bucket_name: file_key}, ]
        :param bucket_name_file_key_dict:
        :return:
        """
        bucket_file_list = self.get_bucket_list_from_path(self.waiting_delete_list_path)
        for bucket_file_dict in bucket_file_dict_list:
            if bucket_file_dict in bucket_file_list:
                bucket_file_list.remove(bucket_file_dict)
        self.zk_operate.create_node_info(self.waiting_delete_list_path, json.dumps(bucket_file_list), True)


    # 监视znode变化
