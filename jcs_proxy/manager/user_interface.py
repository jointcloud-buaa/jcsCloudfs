# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/5/29 21:16'

from metadata.user_info import MetadataUserInfo
from metadata.file_info import MetadataFileInfo

class UserInterface(object):
    """
    用户信息存取接口
    """

    def check_user_exists(self, user_name):
        """
        用户是否存在
        :param user_name:
        :return:
        """
        return MetadataUserInfo().check_user_exists(user_name)

    def create_user(self, user_name, password, others=""):
        user_info = {}
        user_info['user_name'] = user_name
        user_info['password'] = password
        user_info['others'] = others
        MetadataFileInfo().create_file_info(user_name,"","")
        return MetadataUserInfo().create_user_info(user_name, user_info)

    def update_user(self, user_name, password, others=""):
        user_info = {}
        user_info['user_name'] = user_name
        user_info['password'] = password
        user_info['others'] = others
        return MetadataUserInfo().update_user_info(user_name, user_info)

    def get_user(self, user_name):
        return MetadataUserInfo().get_user_info(user_name)

    def delete_user(self, user_name):
        return MetadataUserInfo().delete_user_info(user_name)