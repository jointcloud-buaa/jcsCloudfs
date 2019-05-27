# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/1/17 20:46'

from metadata.cloud_bucket_info import MetadataCloudBucketInfo
from config.configuration import SERVER
from manager.manager_interface import ManagerInterface
from manager.user_interface import UserInterface
from manager.statistics_interface import StatisticsInterface
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SocketServer import ThreadingMixIn
class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

class ServerRpc(object):
    def __init__(self):
        pass

    def server_start(self):
        server = ThreadXMLRPCServer((SERVER["host"], SERVER["port"]), allow_none=True)
        # server.register_instance(ManagerInterface())
        # 文件操作
        server.register_function(ManagerInterface().put_file)
        server.register_function(ManagerInterface().get_file)
        server.register_function(ManagerInterface().delete_file)
        server.register_function(ManagerInterface().list_dir)
        server.register_function(ManagerInterface().create_dir)
        server.register_function(ManagerInterface().delete_dir)

        # 用户账号操作
        server.register_function(UserInterface().check_user_exists)
        server.register_function(UserInterface().create_user)
        server.register_function(UserInterface().update_user)
        server.register_function(UserInterface().get_user)
        server.register_function(UserInterface().delete_user)

        # 可用云，临时故障云，永久故障云操作
        # server.register_function(MetadataCloudBucketInfo().get_avalible_bucket_list)
        # server.register_function(MetadataCloudBucketInfo().get_temporary_fault_bucket_list)
        # server.register_function(MetadataCloudBucketInfo().get_permanent_fault_bucket_list)
        # server.register_function(MetadataCloudBucketInfo().set_avalible_from_temporary_fault)
        # server.register_function(MetadataCloudBucketInfo().set_temporary_fault_from_avalible)
        # server.register_function(MetadataCloudBucketInfo().set_temporary_fault_from_permanent_fault)
        # server.register_function(MetadataCloudBucketInfo().set_permanent_fault_from_temporary_fault)

        # 文件查询，使用量统计
        server.register_function(StatisticsInterface().search_file)  # 查询文件
        server.register_function(StatisticsInterface().list_cloud_region)  # 返回所有的云地域名

        server.register_function(StatisticsInterface().get_file_info)  # 文件存储使用量信息
        server.register_function(StatisticsInterface().user_used_storage)  # 用户存储使用量信息
        server.register_function(StatisticsInterface().cloud_used_storage)  # 云地域存储使用量信息

        server.register_function(StatisticsInterface().file_used_traffic)  # 一个文件的上传下载使用流量(在每个jcsproxy中)
        server.register_function(StatisticsInterface().file_used_traffic_jcsproxy_cloud)  # 一个文件的上传下载使用流量(在每个jcsproxy上传下载到哪些云地域中)
        server.register_function(StatisticsInterface().user_used_traffic)
        server.register_function(StatisticsInterface().user_multicloud_traffic)
        server.register_function(StatisticsInterface().jcsproxy_used_traffic)
        server.register_function(StatisticsInterface().jcsproxy_multicloud_traffic)


        server.serve_forever()

