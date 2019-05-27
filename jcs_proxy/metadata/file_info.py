# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/1/15 22:55'

import json
from config.configuration import CONFIG
from zookeeper_client import ZookeeperClient
import copy

class MetadataFileInfo(object):
    """
    文件元信息管理
    """
    def __init__(self):
        self.zk_operate = ZookeeperClient()
        self.file_info_path = CONFIG["zk_file_info_path"]

    def zk_stop(self):
        """
        关闭zookeeper连接
        :return: 
        """
        self.zk_operate.zk_stop()

    def join_path(self, file_path):
        """
        将file_path添加前缀self.file_info_path
        :param file_path: str
        :return: str
        """
        if file_path == "":
            node_path = self.file_info_path
        else:
            node_path = self.file_info_path + "/" + file_path
        return node_path

    def check_file_exists(self, file_path):
        """
        判断文件是否存在
        :param file_path: str
        :return: dict_res
        """
        node_path = self.join_path(file_path)
        dict_res = self.zk_operate.check_node_exists(node_path)
        return dict_res

    def create_file_info(self, file_path, file_info, cover=False):
        """
        新建文件，写入文件属性值file_info
        :param file_path: str
        :param file_info: dict
        :param cover: bool, 是否覆盖 
        :return: dict_res
        """
        if file_info == "":  # 是否为文件夹
            node_info = ""
        else:
            node_info = json.dumps(file_info)
        node_path = self.join_path(file_path)
        dict_res = self.zk_operate.create_node_info(node_path, node_info, cover)
        return dict_res

    def get_file_info(self, file_path):
        """
        获取文件元信息file_info
        :param file_path: str
        :return: dict_res
        """
        node_path = self.join_path(file_path)
        dict_res = self.zk_operate.get_node_info(node_path)
        if dict_res['status'] == 0:
            file_info = dict_res["result"]
            # 返回结果添加信息，isdir, file_name
            if file_info == "":
                file_info = {}
                file_info['isdir'] = True
            else:
                file_info = json.loads(file_info)
                file_info['isdir'] = False
            # print isinstance(file_path, unicode) == True
            file_path_split = str.split(file_path.encode('utf-8'), "/")
            file_info['file_name'] = file_path_split[len(file_path_split)-1]
            dict_res['result'] = file_info
        return dict_res

    def delete_file_info(self, file_path, recursive=False):
        """
        删除文件元信息
        :param file_path: str
        :param recursive: bool, 是否递归删除
        :return: dict_res
        """
        node_path = self.join_path(file_path)
        dict_res = self.zk_operate.delete_node_info(node_path, recursive)
        return dict_res

    def list_dir_name(self, file_path):
        """
        文件名列表（单层）
        :param file_path: str
        :return: dict_res
        """
        node_path = self.join_path(file_path)
        dict_res = self.zk_operate.list_node_name(node_path)
        return dict_res

    def list_dir_info(self, file_path):
        """
        文件元信息列表
        :param file_path: str
        :return: dict_res
        """
        dict_res = self.list_dir_name(file_path)
        if dict_res['status'] == 0:
            file_name_list = dict_res['result']
            file_info_list = []
            for file_name in file_name_list:
                file_info = self.get_file_info(file_path + "/" + file_name)
                file_info = file_info['result']
                file_info_list.append(file_info)
            dict_res['result'] = file_info_list
        return dict_res


    def list_all_dir_info(self, dir_path):
        """
        列出所有的文件，（递归，深度遍历）
        :param file_path:
        :return:
        """
        dir_info_res = self.get_file_info(dir_path)
        if dir_info_res['status'] == 1:
            return dir_info_res
        dir_info = dir_info_res['result']
        if dir_info['isdir'] == True:
            self.deep_list_file_info(dir_info, dir_path)
        dir_info_res['result'] = dir_info['children']
        return dir_info_res

    def deep_list_file_info(self, dir_info, now_dir_path):
        dir_info['children'] = []
        dict_res = self.list_dir_info(now_dir_path)
        if dict_res['status'] == 0:
            file_info_list = dict_res['result']
            for file_info in file_info_list:
                if file_info['isdir'] == True:
                    self.deep_list_file_info(file_info, now_dir_path+'/'+file_info['file_name'])
                dir_info['children'].append(file_info)

    def list_all_dir_name(self, dir_path):
        """
        列出所有的文件，（递归，深度遍历）
        :param file_path:
        :return:
        """
        dir_info_res = self.get_file_info(dir_path)
        if dir_info_res['status'] == 1:
            return dir_info_res
        dir_info = dir_info_res['result']
        if dir_info['isdir'] == True:
            self.deep_list_file_name(dir_info, dir_path)
        dir_info_res['result'] = dir_info['children']
        return dir_info_res

    def deep_list_file_name(self, dir_info, now_dir_path):
        dir_info['children'] = []
        dict_res = self.list_dir_info(now_dir_path)
        if dict_res['status'] == 0:
            file_info_list = dict_res['result']
            for file_info_one in file_info_list:
                file_info = {}
                file_info['isdir'] = file_info_one['isdir']
                file_info['file_name'] = file_info_one['file_name']
                if file_info['isdir'] == True:
                    self.deep_list_file_name(file_info, now_dir_path + '/' + file_info['file_name'])
                dir_info['children'].append(file_info)

    def create_dir_info(self, dir_path):
        """
        新建文件夹
        :param file_path: str
        :return: dict_res
        """
        return self.create_file_info(dir_path, "")

    def delete_dir_info(self, dir_path, recursive=False):
        """
        删除文件夹
        :param file_path: str
        :param recursive: bool
        :return: dict_res
        """
        return self.delete_file_info(dir_path, recursive)

