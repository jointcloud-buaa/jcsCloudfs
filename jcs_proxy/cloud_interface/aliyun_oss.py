# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/1/15 12:38'

import oss2
import logging
logging.basicConfig(level=logging.ERROR)

class AliyunOSS(object):
    """
    阿里云操作接口，aliyun
    """
    def __init__(self, auth_info):
        """
         传入云端账户信息auth_info
        :param auth_info: dict, 云端账户信息
        """
        self.auth_info = auth_info
        self.auth = oss2.Auth(self.auth_info['accesskey_id'], self.auth_info['accesskey_secret'])
        self.bucket = oss2.Bucket(self.auth, self.auth_info['endpoint'], self.auth_info['bucket_name'])

    def check_auth_info(self):
        """
        判断云端账户信息auth_info是否正确（通过调用云端提供的接口验证）
        :return: bool
        """
        try:
            self.bucket.object_exists('check_file')
            return True
        except:
            return False

    def check_file_exists(self, cloud_file_path):
        """
        判断云端文件cloud_file_path是否存在
        :param cloud_file_path: str, 云端文件路径
        :return: bool
        """
        return self.bucket.object_exists(cloud_file_path)

    def put_file(self, cloud_file_path, local_file_path):
        """
        上传文件（本地到云端）
        :param cloud_file_path: str, 云端文件路径
        :param local_file_path: str, 本地文件路径
        :return: res
        """
        return self.bucket.put_object_from_file(cloud_file_path, local_file_path)

    def get_file(self, cloud_file_path, local_file_path):
        """
        下载文件（云端到本地）
        :param cloud_file_path: str, 云端文件路径
        :param local_file_path: str, 本地文件路径
        :return: res
        """
        return self.bucket.get_object_to_file(cloud_file_path,  local_file_path)

    def get_url(self, cloud_file_path, file_name, expiration_in_seconds=60 * 60):
        """
        下载文件（得到云端文件url链接）
        :param cloud_file_path: str, 云端文件路径
        :param file_name: str, url链接文件名重置
        :param expiration_in_seconds: int, url链接的有效时间（默认60*60，有效时间为1小时）
        :return: res
        """
        param = {'response-content-disposition': 'attachment; filename=' + file_name}
        return self.bucket.sign_url('GET', cloud_file_path, expiration_in_seconds, params=param)

    def delete_file(self, cloud_file_path):
        """
        删除文件
        :param cloud_file_path: str, 云端文件路径
        :return: res
        """
        return self.bucket.delete_object(cloud_file_path)

    def list_file(self):
        """
        获取云端bucket中文件列表（默认数量是一部分而不是全部）
        :return: list
        """
        objects_list = oss2.ObjectIterator(self.bucket)
        key_list = []
        for o in objects_list:
            key_list.append(o.key)
        return key_list
