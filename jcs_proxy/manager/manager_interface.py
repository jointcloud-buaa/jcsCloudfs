# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/1/15 16:58'

import os
from put_file import PutFile
from get_file import GetFile
from delete_file import DeleteFile
from directory import Directory
from metadata.file_info import MetadataFileInfo
from tools.get_dict_res import GetDictRes
from config.configuration import CONFIG
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ManagerInterface(object):
    """
    文件操作管理接口定义
    """
    def __init__(self):
        self.jcsproxy_area = CONFIG['jcsproxy_area']

    def check_local_file_exists(self, local_file_path):
        dict_res = GetDictRes().get_dict_res()
        if os.path.exists(local_file_path):
            dict_res['status'] = 0
            dict_res['result'] = local_file_path+" exists."
        else:
            dict_res['status'] = 1
            dict_res['result'] = local_file_path+" not exists."
        return dict_res

    def put_file(self,  user_name, cloud_file_path, local_file_path, cover=False,
                 storage_time=None, jcsproxy_request_features=None,
                 fault_tolerance_features=None, target_weights=None):
        """
        上传文件（本地到云端）
        :param user_name: str, 用户名
        :param cloud_file_path: str, 云端文件路径
        :param local_file_path: str, 本地文件路径
        :param cover: bool, 是否覆盖文件
        :return: dict_res
        """
        dict_res = self.check_local_file_exists(local_file_path)
        if dict_res["status"] == 0:
            cloud_file_key = user_name + "/" + cloud_file_path
            dict_res = MetadataFileInfo().check_file_exists(cloud_file_key)
            if dict_res["status"] == 0 and cover == False:
                dict_res["status"] = 1
                dict_res["result"] = cloud_file_key + " already exists."
            else:
                # if dict_res["status"] == 0 and cover == True:
                    # 需要考虑先删除原文件，再重新上传，因为可能新策略不一样
                    # del_res = DeleteFile().delete_file(user_name, cloud_file_path)
                dict_res = PutFile().put_file( user_name, cloud_file_path, local_file_path, cover,
                 storage_time, jcsproxy_request_features, fault_tolerance_features, target_weights)
        return dict_res

    # def get_url(self, user_name, cloud_file_path):
    #     """
    #     下载文件（得到云端文件url链接）
    #     :param user_name: str, 用户名
    #     :param cloud_file_path: str, 云端文件路径
    #     :return: dict_res
    #     """
    #     cloud_file_key = user_name + "/" + cloud_file_path
    #     dict_res = MetadataFileInfo().check_file_exists(cloud_file_key)
    #     if dict_res["status"] == 0:
    #         dict_res = GetFileManager().get_url(user_name, cloud_file_path)
    #     return dict_res

    def get_file(self, user_name, cloud_file_path, local_file_path):
        """
        下载文件（云端到本地）
        :param user_name: str, 用户名
        :param cloud_file_path: str, 云端文件路径
        :param local_file_path: str, 本地文件路径
        :return: dict_res
        """
        cloud_file_key = user_name + "/" + cloud_file_path
        dict_res = MetadataFileInfo().check_file_exists(cloud_file_key)
        if dict_res["status"] == 0:
            dict_res = GetFile().get_file(user_name, cloud_file_path, local_file_path)
        print 'get file'
        print dict_res
        print 'download_bucket_name_list'
        print dict_res['result']['download_bucket_name_list']
        return dict_res

    def delete_file(self, user_name, cloud_file_path, check_insert_waiting_delete_file=True):
        """
        删除文件
        :param user_name: str, 用户名
        :param cloud_file_path: str, 云端文件路径
        :return: dict_res
        """
        cloud_file_key = user_name + "/" + cloud_file_path
        dict_res = MetadataFileInfo().get_file_info(cloud_file_key)
        if dict_res["status"] == 0:
            if dict_res["result"]["isdir"] == True:
                dict_res["status"] = 1
                dict_res["result"] = cloud_file_key+" is dir."
            else:
                dict_res = DeleteFile().delete_file(user_name, cloud_file_path, check_insert_waiting_delete_file)
        return dict_res

    def list_dir(self, user_name, cloud_file_path):
        """
        目录列表
        :param user_name:
        :param cloud_file_path:
        :return:
        """
        return Directory().list_dir(user_name, cloud_file_path)

    def create_dir(self, user_name, cloud_file_path):
        """
        新建文件夹
        :param user_name:
        :param cloud_file_path:
        :return:
        """
        return Directory().create_dir(user_name, cloud_file_path)

    def delete_dir(self, user_name, cloud_file_path, recursive=False):
        """
        删除文件夹
        :param user_name:
        :param cloud_file_path:
        :param recursive:   是否递归删除
        :return:
        """
        return Directory().delete_dir(user_name, cloud_file_path, recursive)

