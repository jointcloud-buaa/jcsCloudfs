# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/1/15 13:55'

from aliyun_oss import AliyunOSS
from baidu_bos import BaiduBOS
from ksyun_ks3 import KsyunKS3
from tools.get_dict_res import GetDictRes

class CloudInterface(object):
    """
    多云存储统一操作接口
    """
    def __init__(self, auth_info):
        """
        根据云端账户信息auth_info，选择云端接口
        :param auth_info: dict, 云端账户信息
        """
        self.auth_info = auth_info
        self.cloud_operate = None
        # 根据auth_info选择云存储端的接口
        if auth_info['cloud_name'] == 'aliyun':
            self.cloud_operate = AliyunOSS(auth_info)
        elif auth_info['cloud_name'] == 'baidu':
            self.cloud_operate = BaiduBOS(auth_info)
        elif auth_info['cloud_name'] == 'ksyun':
            self.cloud_operate = KsyunKS3(auth_info)


    def check_auth_info(self):
        """
        判断存储端账户信息auth_info是否正确（通过调用云存储端提供的接口验证）
        :return: dict_res
        """
        dict_res = GetDictRes().get_dict_res()
        if self.cloud_operate.check_auth_info():
            dict_res['status'] = 0
            dict_res['result'] = "auth_info correct."
        else:
            dict_res['status'] = 1
            dict_res['result'] = "auth_info error."
        return dict_res

    def check_file_exists(self, cloud_file_path):
        """
        判断云端文件cloud_file_path是否存在
        :param cloud_file_path: str, 云端文件路径
        :return: bool
        """
        dict_res = GetDictRes().get_dict_res()
        if self.cloud_operate.check_file_exists(cloud_file_path):
            dict_res['status'] = 0
            dict_res['result'] = cloud_file_path+" exists."
        else:
            dict_res['status'] = 1
            dict_res['result'] = cloud_file_path+" not exists"
        return dict_res

    def put_file(self, cloud_file_path, local_file_path):
        """
        上传文件（本地到云端）
        :param cloud_file_path: str, 云端文件路径
        :param local_file_path: str, 本地文件路径
        :return: res
        """
        dict_res = GetDictRes().get_dict_res()
        try:
            self.cloud_operate.put_file(cloud_file_path, local_file_path)
        except IOError:
            dict_res['status'] = 1
            dict_res['result'] = "IOError: no such file: " + local_file_path
        except:
            dict_res['status'] = 1
            dict_res['result'] = "cloud_put_file error!"
        return dict_res


    def get_file(self, cloud_file_path, local_file_path):
        """
        下载文件（云端到本地）
        :param cloud_file_path: str, 云端文件路径
        :param local_file_path: str, 本地文件路径
        :return: res
        """
        dict_res = self.check_file_exists(cloud_file_path)
        if dict_res['status'] == 0:
            self.cloud_operate.get_file(cloud_file_path, local_file_path)
        return dict_res

    def get_url(self, cloud_file_path, file_name=None, expiration_in_seconds=60 * 60):
        """
        下载文件（得到云端文件url链接）
        :param cloud_file_path: str, 云端文件路径
        :param file_name: str, url链接文件名重置
        :param expiration_in_seconds: int, url链接的有效时间（默认60*60，有效时间为1小时）
        :return: res
        """
        if file_name == None:
            file_name = cloud_file_path
        dict_res = self.check_file_exists(cloud_file_path)
        if dict_res['status'] == 0:
            url = self.cloud_operate.get_url(cloud_file_path, file_name, expiration_in_seconds)
            dict_res['result'] = url
        return dict_res

    def delete_file(self, cloud_file_path):
        """
        删除文件
        :param cloud_file_path: str, 云端文件路径
        :return: res
        """
        dict_res = self.check_file_exists(cloud_file_path)
        if dict_res['status'] == 0:
            self.cloud_operate.delete_file(cloud_file_path)
        return dict_res

    def list_file(self):
        """
        获取云端bucket中文件列表（默认数量是一部分而不是全部）
        :return: dict_res
        """
        dict_res = GetDictRes().get_dict_res()
        dict_res['result'] = self.cloud_operate.list_file()
        return dict_res


