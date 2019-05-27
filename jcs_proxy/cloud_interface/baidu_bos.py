# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/1/15 12:38'

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.bos.bos_client import BosClient

class BaiduBOS(object):
    """
    百度云操作接口，baidu
    """
    def __init__(self, auth_info):
        """
         传入云端账户信息auth_info
        :param auth_info: dict, 云端账户信息
        """
        # unicode编码会出现错误，都转化成utf-8
        for auth_i in auth_info:
            auth_info[auth_i] = self.change_to_utf8(auth_info[auth_i])
        self.auth_info = auth_info
        credentials = BceCredentials(self.auth_info['accesskey_id'], self.auth_info['accesskey_secret'])
        config = BceClientConfiguration(credentials, self.auth_info['endpoint'])
        self.auth = BosClient(config)

    def change_to_utf8(self, my_str):  # baidu unicode编码会报错
        if isinstance(my_str, unicode):
            return my_str.encode('utf-8')
        return my_str

    def check_auth_info(self):
        """
        判断云端账户信息auth_info是否正确（通过调用云端提供的接口验证）
        :return: bool
        """
        try:
            self.auth.list_objects(self.auth_info['bucket_name'], max_keys=1)
            return True
        except:
            return False

    def check_file_exists(self, cloud_file_path):
        """
        判断云端文件cloud_file_path是否存在
        :param cloud_file_path: str, 云端文件路径
        :return: bool
        """
        cloud_file_path = self.change_to_utf8(cloud_file_path)
        try:
            self.auth.get_object_meta_data(self.auth_info['bucket_name'], cloud_file_path)
            return True
        except :
            return False

    def put_file(self, cloud_file_path, local_file_path):
        """
        上传文件（本地到云端）
        :param cloud_file_path: str, 云端文件路径
        :param local_file_path: str, 本地文件路径
        :return: res
        """
        cloud_file_path = self.change_to_utf8(cloud_file_path)
        local_file_path = self.change_to_utf8(local_file_path)
        return self.auth.put_object_from_file(self.auth_info['bucket_name'], cloud_file_path, local_file_path)

    def get_file(self, cloud_file_path, local_file_path):
        """
        下载文件（云端到本地）
        :param cloud_file_path: str, 云端文件路径
        :param local_file_path: str, 本地文件路径
        :return: res
        """
        cloud_file_path = self.change_to_utf8(cloud_file_path)
        local_file_path = self.change_to_utf8(local_file_path)
        return self.auth.get_object_to_file(self.auth_info['bucket_name'], cloud_file_path, local_file_path)

    def get_url(self, cloud_file_path, file_name, expiration_in_seconds=60 * 60):
        """
        下载文件（得到云端文件url链接）
        :param cloud_file_path: str, 云端文件路径
        :param file_name: str, url链接文件名重置
        :param expiration_in_seconds: int, url链接的有效时间（默认60*60，有效时间为1小时）
        :return: res
        """
        cloud_file_path = self.change_to_utf8(cloud_file_path)
        file_name = self.change_to_utf8(file_name)
        param = {'responseContentDisposition': 'attachment; filename=' + file_name}
        return self.auth.generate_pre_signed_url(self.auth_info['bucket_name'],
                    cloud_file_path, expiration_in_seconds=expiration_in_seconds, params=param)

    def delete_file(self, cloud_file_path):
        """
        删除文件
        :param cloud_file_path: str, 云端文件路径
        :return: res
        """
        cloud_file_path = self.change_to_utf8(cloud_file_path)
        return self.auth.delete_object(self.auth_info['bucket_name'], cloud_file_path)

    def list_file(self):
        """
        获取云端bucket中文件列表（默认数量是一部分而不是全部）
        :return: list
        """
        objects_list = self.auth.list_all_objects(self.auth_info['bucket_name'])
        key_list = []
        for o in objects_list:
            key_list.append(o.key)
        return key_list
