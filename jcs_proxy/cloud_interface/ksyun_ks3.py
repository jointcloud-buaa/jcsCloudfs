# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/1/15 13:55'

from ks3.connection import Connection

class KsyunKS3(object):
    """
    金山云操作接口，ksyun
    """
    def __init__(self, auth_info):
        """
         传入云端账户信息auth_info
        :param auth_info: dict, 云端账户信息
        """
        self.auth_info = auth_info
        self.auth = Connection(self.auth_info['accesskey_id'],self.auth_info['accesskey_secret'],
                               host = self.auth_info['endpoint'])
        self.bucket = self.auth.get_bucket(self.auth_info['bucket_name'])

    def check_auth_info(self):
        """
        判断云端账户信息auth_info是否正确（通过调用云端提供的接口验证）
        :return: bool
        """
        try:
            self.bucket.get_acl()
            return True
        except:
            return False

    def check_file_exists(self, cloud_file_path):
        """
        判断云端文件cloud_file_path是否存在
        :param cloud_file_path: str, 云端文件路径
        :return: bool
        """
        print cloud_file_path
        if self.bucket.get_key(cloud_file_path):
            return True
        else:
            return False

    def put_file(self, cloud_file_path, local_file_path):
        """
        上传文件（本地到云端）
        :param cloud_file_path: str, 云端文件路径
        :param local_file_path: str, 本地文件路径
        :return: res
        """
        upload_key = self.bucket.new_key(cloud_file_path)
        return upload_key.set_contents_from_filename(local_file_path)

    def get_file(self, cloud_file_path, local_file_path):
        """
        下载文件（云端到本地）
        :param cloud_file_path: str, 云端文件路径
        :param local_file_path: str, 本地文件路径
        :return: res
        """
        download_key = self.bucket.get_key(cloud_file_path)
        return download_key.get_contents_to_filename(local_file_path)

    def get_url(self, cloud_file_path, file_name, expiration_in_seconds=60 * 60):
        """
        下载文件（得到云端文件url链接）
        :param cloud_file_path: str, 云端文件路径
        :param file_name: str, url链接文件名重置
        :param expiration_in_seconds: int, url链接的有效时间（默认60*60，有效时间为1小时）
        :return: res
        """
        # 金山云接口暂不支持file_name重新设置
        url_key = self.bucket.get_key(cloud_file_path)
        return url_key.generate_url(expires_in=expiration_in_seconds)

    def delete_file(self, cloud_file_path):
        """
        删除文件
        :param cloud_file_path: str, 云端文件路径
        :return: res
        """
        return self.bucket.delete_key(cloud_file_path)

    def list_file(self):
        """
        获取云端bucket中文件列表（默认数量是一部分而不是全部）
        :return: list
        """
        objects_list = self.bucket.get_all_keys()
        key_list = []
        for o in objects_list:
            key_list.append(o.name)
        return key_list



