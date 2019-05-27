# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/5/29 21:33'

from search_file import SearchFile
from used_storage import UsedStorge
from datalog_operation.datalog_used_traffic import DatalogUsedTraffic
from tools.get_dict_res import GetDictRes
from config.cloud_information import CloudInformation


class StatisticsInterface(object):
    """
    查询，存储量统计，的操作接口
    """
    def search_file(self, user_name, file_name):
        """
        查找用户下的某个文件
        返回包含文件名的所有路径列表
        :param user_name:
        :param file_name:
        :return:
        """
        return SearchFile().search_file(user_name, file_name)

    #######################################################################

    def get_file_info(self, user_name, file_name):
        """
        获取用户信息
        :param user_name:
        :param file_name:
        :return:
        """
        return UsedStorge().get_file_info(user_name, file_name)

    def user_used_storage(self, user_name):
        """
        用户在每个云地域上的存储量，和总存储量
        :param user_name:
        :return:
        """
        return UsedStorge().user_used_storage(user_name)

    def cloud_used_storage(self):
        """
        所有云地域的存储量
        :return:
        """
        return UsedStorge().refresh_cloud_used_storage()

    #################################################################

    def file_used_traffic(self, user_name, cloud_file_path):
        """
        一个文件的上传下载使用流量(在每个jcsproxy中)
        :param user_name:
        :param cloud_file_path:
        :return:
        """
        cloud_file_key = user_name + "/" + cloud_file_path
        res = DatalogUsedTraffic().count_jcsproxy_used_traffic_file(cloud_file_key)
        dict_res = GetDictRes().get_dict_res()
        dict_res['result'] = res
        return dict_res

    def file_used_traffic_jcsproxy_cloud(self, user_name, cloud_file_path):
        """
        一个文件的上传下载使用流量(在每个jcsproxy上传下载到哪些云地域中)
        :param user_name:
        :param cloud_file_path:
        :return:
        """
        cloud_file_key = user_name + "/" + cloud_file_path
        res = DatalogUsedTraffic().count_jcsproxy_bucket_used_traffic_file(cloud_file_key)
        dict_res = GetDictRes().get_dict_res()
        dict_res['result'] = res
        return dict_res


    def user_used_traffic(self, user_name):
        """
        一个用户的上传下载使用流量(在每个jcsproxy中)
        :param user_name:
        :param cloud_file_path:
        :return:
        """
        res = DatalogUsedTraffic().count_jcsproxy_used_traffic_user(user_name)
        dict_res = GetDictRes().get_dict_res()
        dict_res['result'] = res
        return dict_res

    def user_multicloud_traffic(self, user_name):
        """
        一个用户的上传下载使用流量(在每个jcsproxy上传下载到哪些云地域中)
        :param user_name:
        :param cloud_file_path:
        :return:
        """
        res = DatalogUsedTraffic().count_jcsproxy_bucket_used_traffic_user(user_name)
        dict_res = GetDictRes().get_dict_res()
        dict_res['result'] = res
        return dict_res


    def jcsproxy_used_traffic(self):
        """
        一个jcsproxy的上传下载使用流量(在每个jcsproxy中)
        :param user_name:
        :param cloud_file_path:
        :return:
        """
        res = DatalogUsedTraffic().count_jcsproxy_used_traffic()
        dict_res = GetDictRes().get_dict_res()
        dict_res['result'] = res
        return dict_res

    def jcsproxy_multicloud_traffic(self):
        """
        一个文件的上传下载使用流量(在每个jcsproxy上传下载到哪些云地域中)
        :param user_name:
        :param cloud_file_path:
        :return:
        """
        res = DatalogUsedTraffic().count_jcsproxy_bucket_used_traffic()
        dict_res = GetDictRes().get_dict_res()
        dict_res['result'] = res
        return dict_res

    ##############################################################

    def list_cloud_region(self):
        """
        返回所有云地域名
        :return:
        """
        cloud_region_list = []
        cloud_bucket_list = CloudInformation().get_cloud_bucket_list()
        for cloud_bucket in cloud_bucket_list:
            bucket_name = cloud_bucket['bucket_name']
            cloud_region_list.append(bucket_name)
        dict_res = GetDictRes().get_dict_res()
        dict_res['result'] = cloud_region_list
        return dict_res