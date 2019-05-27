# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/10/7 21:57'

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))
from xmlrpclib import ServerProxy
from config.configuration import SERVER, CONFIG
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def print_cloud_bucket_list_one(cloud_bucket_list, cloud_bucket_name_str=""):
    print cloud_bucket_name_str, len(cloud_bucket_list), ":"
    if len(cloud_bucket_list) == 0:
        return
    for bucket_one in cloud_bucket_list:
        print bucket_one['bucket_name'], " "

def print_cloud_bucket_lists(cloud_bucket_operate):
    """
    输出三个云列表，len, buclet_names
    :return:
    """
    res = cloud_bucket_operate.get_avalible_bucket_list()
    # print_cloud_bucket_list_one(res['result'], "get_avalible_bucket_list")
    res = cloud_bucket_operate.get_temporary_fault_bucket_list()
    print_cloud_bucket_list_one(res['result'], "get_temporary_fault_bucket_list")
    res = cloud_bucket_operate.get_permanent_fault_bucket_list()
    print_cloud_bucket_list_one(res['result'], "get_permanent_fault_bucket_list")


if __name__ == '__main__':
    # cloud_bucket_info相关接口测试
    # 可用云，临时故障云，永久故障云。三种云列表的存储和相互转换
    
    # server_rpc = ServerProxy("http://your-ip-address-here:8889")
    server_rpc = ServerProxy("http://"+SERVER["host"]+":"+str(SERVER["port"]))
    cloud_bucket_operate = server_rpc

    print "get cloud bucket list:"
    res = cloud_bucket_operate.get_avalible_bucket_list()
    print "获取可用云列表", res
    res = cloud_bucket_operate.get_temporary_fault_bucket_list()
    print "获取临时故障云列表", res
    res = cloud_bucket_operate.get_permanent_fault_bucket_list()
    print "获取永久故障云列表", res

    print "print cloud bucket lists:"
    print_cloud_bucket_lists(cloud_bucket_operate)

    print "exchange cloud bucket list:"
    res = cloud_bucket_operate.set_temporary_fault_from_avalible("jcsproxy-aliyun-beijing")
    print "可用云到临时故障云，第一个jcsproxy-aliyun-beijing", res
    print_cloud_bucket_lists(cloud_bucket_operate)
    res = cloud_bucket_operate.set_temporary_fault_from_avalible("jcsproxy-aliyun-beijing")
    print "可用云到临时故障云，jcsproxy-aliyun-beijing不在可用云中，操作失败", res
    print_cloud_bucket_lists(cloud_bucket_operate)
    res = cloud_bucket_operate.set_temporary_fault_from_avalible("bucket name wrong")
    print "可用云到临时故障云，bucket_name错误，操作失败", res
    print_cloud_bucket_lists(cloud_bucket_operate)
    res = cloud_bucket_operate.set_temporary_fault_from_avalible("jcsproxy-ksyun-shanghai")
    print "可用云到临时故障云，第二个jcsproxy-ksyun-shanghai", res
    print_cloud_bucket_lists(cloud_bucket_operate)

    res = cloud_bucket_operate.set_permanent_fault_from_temporary_fault("jcsproxy-aliyun-beijing")
    print "临时故障云到永久故障云，第一个jcsproxy-aliyun-beijing", res
    print_cloud_bucket_lists(cloud_bucket_operate)
    res = cloud_bucket_operate.set_permanent_fault_from_temporary_fault("jcsproxy-aliyun-beijing")
    print "临时故障云到永久故障云，jcsproxy-aliyun-beijing不在临时故障云中，操作失败", res
    print_cloud_bucket_lists(cloud_bucket_operate)
    res = cloud_bucket_operate.set_permanent_fault_from_temporary_fault("jcsproxy-ksyun-shanghai")
    print "临时故障云到永久故障云，第二个jcsproxy-ksyun-shanghai", res
    print_cloud_bucket_lists(cloud_bucket_operate)

    res = cloud_bucket_operate.set_temporary_fault_from_permanent_fault("jcsproxy-aliyun-beijing")
    print "永久故障云到临时故障云，第一个jcsproxy-aliyun-beijing", res
    print_cloud_bucket_lists(cloud_bucket_operate)
    res = cloud_bucket_operate.set_temporary_fault_from_permanent_fault("jcsproxy-aliyun-beijing")
    print "永久故障云到临时故障云，jcsproxy-aliyun-beijing不在永久故障云中，操作失败", res
    print_cloud_bucket_lists(cloud_bucket_operate)
    res = cloud_bucket_operate.set_temporary_fault_from_permanent_fault("jcsproxy-ksyun-shanghai")
    print "永久故障云到临时故障云，第二个jcsproxy-ksyun-shanghai", res
    print_cloud_bucket_lists(cloud_bucket_operate)

    res = cloud_bucket_operate.set_avalible_from_temporary_fault("jcsproxy-aliyun-beijing")
    print "临时故障云到可用云，第一个jcsproxy-aliyun-beijing", res
    print_cloud_bucket_lists(cloud_bucket_operate)
    res = cloud_bucket_operate.set_avalible_from_temporary_fault("jcsproxy-aliyun-beijing")
    print "临时故障云到可用云，jcsproxy-aliyun-beijing不在临时故障云中，操作失败", res
    print_cloud_bucket_lists(cloud_bucket_operate)
    res = cloud_bucket_operate.set_avalible_from_temporary_fault("jcsproxy-ksyun-shanghai")
    print "临时故障云到可用云，第二个jcsproxy-ksyun-shanghai", res
    print_cloud_bucket_lists(cloud_bucket_operate)


