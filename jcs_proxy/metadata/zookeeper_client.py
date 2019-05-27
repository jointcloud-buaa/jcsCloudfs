# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/1/15 18:33'

from config.singleton import Singleton
from kazoo.client import KazooClient
from tools.get_dict_res import GetDictRes
from config.configuration import CONFIG

class ZookeeperClient(Singleton):  # 继承单例模式
    """
    zookeeper数据模型接口操作 
    """
    def __init__(self):
        if self._first_init:
            self.zk_start()
            self._first_init = False

    # def __init__(self):
    #     self.zk_start()

    def zk_start(self):
        """
        与zookeeper建立连接
        """
        self.zk = KazooClient(hosts=CONFIG["zk_host"]+":"+CONFIG["zk_port"])
        self.zk.start()

    def get_zk_client(self):
        return self.zk

    def zk_stop(self):
        """
        关闭zookeeper连接
        :return:
        """
        self.zk.stop()

    def check_node_exists(self, node_path):
        """
        判断node是否存在
        :param node_path: str 
        :return: dict_res
        """
        dict_res = GetDictRes().get_dict_res()
        if self.zk.exists(node_path):
            dict_res['status'] = 0
            dict_res['result'] = node_path+" exists."
        else:
            dict_res['status'] = 1
            dict_res['result'] = node_path+" not exists."
        return dict_res

    def create_node_info(self, node_path, node_info, cover=False):
        """
        新建node，写入node_info
        :param node_path: str
        :param node_info: str
        :param cover: bool, 是否覆盖 
        :return: dict_res
        """
        dict_res = self.check_node_exists(node_path)
        if dict_res['status'] == 0 and cover == False:  # 是否覆盖
            dict_res['status'] = 1
            dict_res['result'] = node_path + " already exists."
            return dict_res
        self.zk.ensure_path(node_path)
        self.zk.set(node_path, node_info)
        dict_res = GetDictRes().get_dict_res()
        dict_res['result'] = "create node info, node path: "+node_path+\
                                     ", node_info: "+node_info
        return dict_res

    def get_node_info(self, node_path):
        """
        获取node信息
        :param node_path: str
        :return: dict_res
        """
        dict_res = self.check_node_exists(node_path)
        if dict_res['status'] == 0:
            node_info, stat = self.zk.get(node_path)
            dict_res['result'] = node_info
        return dict_res

    def delete_node_info(self, node_path, recursive=False):
        """
        删除node
        :param node_path: str
        :param recursive: bool
        :return: dict_res
        """
        dict_res = self.check_node_exists(node_path)
        if dict_res['status'] == 0:
            try:
                self.zk.delete(node_path, recursive=recursive)
                dict_res['result'] = "delete "+node_path
            except:  # 是否递归删除文件夹
                dict_res['status'] = 1
                dict_res['result'] = node_path+" not empty."
        return dict_res

    def list_node_name(self, node_path):
        """
        node名列表
        :param node_path: str
        :return: dict_res
        """
        dict_res = self.check_node_exists(node_path)
        if dict_res['status'] == 0:
            node_name_list = self.zk.get_children(node_path)
            dict_res['result'] = node_name_list
        return dict_res

    def list_node_info(self, node_path):
        """
        node信息列表
        :param node_path: str
        :return: dict_res
        """
        dict_res = self.list_node_name(node_path)
        if dict_res['status'] == 0:
            file_name_list = dict_res['result']
            file_info_list = []
            for file_name in file_name_list:
                file_info = self.get_node_info(node_path+"/"+file_name)
                file_info = file_info['result']
                file_info_list.append(file_info)
            dict_res['result'] = file_info_list
        return dict_res

    # (list 递归列表)

