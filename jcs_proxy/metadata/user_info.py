# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/1/16 14:12'

import json
from config.configuration import CONFIG
from zookeeper_client import ZookeeperClient

class MetadataUserInfo(object):
    """
    用户账号信息管理
    """
    def __init__(self):
        self.zk_operate = ZookeeperClient()
        self.user_info_path = CONFIG["zk_user_info_path"]

    def zk_stop(self):
        """
        关闭zookeeper连接
        :return: 
        """
        self.zk_operate.zk_stop()

    def join_path(self, user_name):
        if user_name == "":
            node_path = self.user_info_path
        else:
            node_path = self.user_info_path + "/" + user_name
        return node_path

    def check_user_exists(self, user_name):
        node_path = self.join_path(user_name)
        dict_res = self.zk_operate.check_node_exists(node_path)
        return dict_res

    def create_user_info(self, user_name, user_info, cover=False):
        node_path = self.join_path(user_name)
        node_info = json.dumps(user_info)
        dict_res = self.zk_operate.create_node_info(node_path, node_info, cover)
        return dict_res

    def update_user_info(self, user_name, user_info):
        return self.create_user_info(user_name, user_info, cover=True)

    def get_user_info(self, user_name):
        node_path = self.join_path(user_name)
        dict_res = self.zk_operate.get_node_info(node_path)
        if dict_res["status"] == 0:
            dict_res["result"] = json.loads(dict_res["result"])
        return dict_res

    def delete_user_info(self, user_name):
        node_path = self.join_path(user_name)
        dict_res = self.zk_operate.delete_node_info(node_path)
        return dict_res

    def list_user_name(self):
        node_path = self.join_path("")
        dict_res = self.zk_operate.list_node_name(node_path)
        return dict_res

    def list_user_info(self):
        dict_res = self.list_user_name()
        user_name_list = dict_res['result']
        user_info_list = []
        for user_name in user_name_list:
            user_info = self.get_user_info(user_name)
            user_info = user_info['result']
            user_info_list.append(user_info)
        dict_res['result'] = user_info_list
        return dict_res
