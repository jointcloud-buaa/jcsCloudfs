# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/10/7 22:03'

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))
from xmlrpclib import ServerProxy
from config.configuration import SERVER, CONFIG
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

"""
移除几个云，上传下载删除接口测试
"""

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
    # res = cloud_bucket_operate.get_avalible_bucket_list()
    # print_cloud_bucket_list_one(res['result'], "get_avalible_bucket_list")
    res = cloud_bucket_operate.get_temporary_fault_bucket_list()
    print_cloud_bucket_list_one(res['result'], "get_temporary_fault_bucket_list")
    res = cloud_bucket_operate.get_permanent_fault_bucket_list()
    print_cloud_bucket_list_one(res['result'], "get_permanent_fault_bucket_list")


if __name__ == '__main__':
    # server_rpc = ServerProxy("http://your-ip-address-here:8889")
    server_rpc = ServerProxy("http://"+SERVER["host"]+":"+str(SERVER["port"]))
    manager_operate = server_rpc

    # 设置测试参数(英文)
    # user_name = "liuyf_test"  # 用户名
    # dir_path = "dir"
    # cloud_file_path = dir_path+"/remote.txt"
    # local_file_path = "/storage/liuyf_test/jcsProxyDir/datatest/test.txt"  # liuyf账户测试
    # local_file_path = "/storage/ivic/liuyf/jcsProxyDir/datatest/test.txt"  # ivic账户测试

    # 设置测试参数(中文)
    user_name = "刘_测试"
    dir_path = "目录"
    cloud_file_path = dir_path+"/云文件.txt"
    local_file_path = "/storage/liuyf_test/jcsProxyDir/datatest/test_4"        # liuyf账户测试
    # local_file_path = "/storage/ivic/liuyf/jcsProxyDir/datatest/文件.txt"    # ivic账户测试


    print "所有云可用时，正常情况对照组:"
    res = manager_operate.put_file(user_name, cloud_file_path, local_file_path, True)
    print "正常上传文件，覆盖", res
    print res['result']['file_info']['cloud_block_path_dict'].keys()
    res = manager_operate.get_file(user_name, cloud_file_path, local_file_path)
    print "正常下载文件", res
    print res['result']['download_bucket_name_list']
    res = manager_operate.delete_file(user_name, cloud_file_path)
    print "正常删除文件", res
    print res['result']['file_info']['cloud_block_path_dict'].keys()
    res = manager_operate.put_file(user_name, cloud_file_path, local_file_path, True)
    print "再次正常上传文件, 覆盖", res
    print res['result']['file_info']['cloud_block_path_dict'].keys()


    cloud_bucket_operate = server_rpc
    print ""
    print "某个上传个过程中使用的云不可用时:"
    # res = cloud_bucket_operate.set_temporary_fault_from_avalible("jcsproxy-aliyun-zhangjiakou")
    # print "jcsproxy-aliyun-zhangjiakou云不可用", res
    res = cloud_bucket_operate.set_temporary_fault_from_avalible("jcsproxy-aliyun-beijing")
    print "jcsproxy-aliyun-beijing云不可用", res

    res = cloud_bucket_operate.set_avalible_from_temporary_fault("jcsproxy-aliyun-zhangjiakou")
    print "临时故障云到可用云，第一个jcsproxy-aliyun-zhangjiakou", res
    print_cloud_bucket_lists(cloud_bucket_operate)
    print ""


    print "云故障下载文件测试:"
    res = manager_operate.get_file(user_name, cloud_file_path, local_file_path)
    print "正常下载文件", res
    print res['result']['download_bucket_name_list']

    print "云故障删除文件测试: 注意故障云中的文件块没有正常删除"
    res = manager_operate.delete_file(user_name, cloud_file_path)
    print "正常删除文件", res
    print res['result']['file_info']['cloud_block_path_dict'].keys()

    print "云故障上传文件测试:"
    res = manager_operate.put_file(user_name, cloud_file_path, local_file_path, True)
    print "正常上传文件，覆盖", res
    print res['result']['file_info']['cloud_block_path_dict'].keys()

    print "测试完毕，删除测试用户的所有目录"
    res = manager_operate.delete_dir(user_name, "", True)
    print(res)