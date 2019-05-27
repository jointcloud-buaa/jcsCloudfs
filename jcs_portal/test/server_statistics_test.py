# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/5/29 22:18'

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))
from xmlrpclib import ServerProxy
from config.configuration import SERVER, CONFIG
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


if __name__ == '__main__':
    print "测试，查询文件，文件使用量/上传下载流量统计信息"
    print("连接RPC服务器")
    server_rpc = ServerProxy("http://your-ip-address-here:8889")
    # server_rpc = ServerProxy("http://"+SERVER["host"]+":"+str(SERVER["port"]))
    statistics_operate = server_rpc

    # 设置测试参数
    # user1 = 'liuyftest1'
    # user2 = 'liuyftest2'
    # cloud_file_name = 'checkfile'
    # # local_file_path = "/storage/liuyf_test/jcsProxyDir/datatest/test.txt"  # liuyf账户测试
    # local_file_path = "/storage/ivic/liuyf/jcsProxyDir/datatest/test.txt"  # ivic账户测试

    user1 = '刘1'
    user2 = '刘2'
    cloud_file_name = 'check文件'
    # local_file_path = "/storage/liuyf_test/jcsProxyDir/datatest/文件.txt"
    local_file_path = "/storage/ivic/liuyf/jcsProxyDir/datatest/文件.txt"

    print "建立测试用户"
    print server_rpc.create_user(user1, 'liuyftestpassword')
    print server_rpc.create_user(user2, 'liuyftestpassword')
    print "上传测试文件"
    print server_rpc.put_file(user1, cloud_file_name, local_file_path)
    print server_rpc.put_file(user1, "dir/" + cloud_file_name, local_file_path)
    print server_rpc.put_file(user2, cloud_file_name, local_file_path)
    print "下载测试文件"
    print server_rpc.get_file(user1, cloud_file_name, local_file_path)


    print ""
    print "search file"
    res = statistics_operate.search_file(user1, cloud_file_name)
    print "查找用户1中的某个文件", res
    res = statistics_operate.search_file(user2, cloud_file_name)
    print "查找用户2中的某个文件", res
    res = statistics_operate.search_file("wrong", cloud_file_name)
    print "用户不存在", res
    res = statistics_operate.search_file(user1, "wrong")
    print "查找的文件不存在", res


    print ""
    print "存储量"
    print "get file info"
    res = statistics_operate.get_file_info(user1, cloud_file_name)
    print "获取某个文件信息", res
    res = statistics_operate.get_file_info("wrong", cloud_file_name)
    print "用户不存在", res
    res = statistics_operate.get_file_info(user1, "wrong")
    print "文件不存在", res

    print "user used storage"
    res = statistics_operate.user_used_storage(user1)
    print "用户1的存储量使用", res
    res = statistics_operate.user_used_storage(user2)
    print "用户2的存储量使用", res
    res = statistics_operate.user_used_storage('wrong')
    print "用户不存在", res

    print "cloud used storage"
    res = statistics_operate.cloud_used_storage()
    print "云地域的存储量使用", res



    print ""
    print "流量"
    print "file used traffic"
    res = statistics_operate.file_used_traffic(user1, cloud_file_name)
    print "一个文件的上传下载使用流量(在每个jcsproxy中)", res
    res = statistics_operate.file_used_traffic_jcsproxy_cloud(user1, cloud_file_name)
    print "一个文件的上传下载使用流量(在每个jcsproxy上传下载到哪些云地域中)", res
    res = statistics_operate.file_used_traffic("wrong", cloud_file_name)
    print "用户不存在", res
    res = statistics_operate.file_used_traffic(user1, "wrong")
    print "文件不存在", res

    print "user used traffic"
    res = statistics_operate.user_used_traffic(user1)
    print "一个用户的上传下载使用流量(在每个jcsproxy中)", res
    res = statistics_operate.user_used_traffic_jcsproxy_cloud(user1)
    print "一个用户的上传下载使用流量(在每个jcsproxy上传下载到哪些云地域中)", res
    res = statistics_operate.user_used_traffic("wrong")
    print "用户不存在", res

    print "jcsproxy used traffic"
    res = statistics_operate.jcsproxy_used_traffic()
    print "每个jcsproxy的上传下载使用流量", res
    res = statistics_operate.jcsproxy_used_traffic_jcsproxy_cloud()
    print "每个jcsproxy用户的上传下载使用流量(在每个jcsproxy上传下载到哪些云地域中)", res





    # print "删除测试用户和测试文件"