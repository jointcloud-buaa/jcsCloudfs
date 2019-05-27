# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/5/29 21:46'

from manager.statistics_interface import StatisticsInterface
from manager.manager_interface import ManagerInterface
from manager.user_interface import UserInterface
import os
from config.configuration import CONFIG

if __name__ == '__main__':
    print "测试，查询文件，文件使用量/上传下载流量统计信息"
    statistics_operate = StatisticsInterface()
    manager_operate = ManagerInterface()
    user_operate = UserInterface()

    # 设置测试参数
    user1 = 'liuyftest1'
    user2 = 'liuyftest2'
    cloud_file_name = 'checkfile1'
    local_file_path = os.path.join(CONFIG["test_file_path"], "test_4")


    print "建立测试用户"
    print user_operate.create_user(user1, 'liuyftestpassword')
    print user_operate.create_user(user2, 'liuyftestpassword')
    print "上传测试文件"
    print manager_operate.put_file(user1, cloud_file_name, local_file_path)
    print manager_operate.put_file(user1, "dir/" + cloud_file_name, local_file_path)
    print manager_operate.put_file(user2, cloud_file_name, local_file_path)
    print "下载测试文件"
    print manager_operate.get_file(user1, cloud_file_name, local_file_path+'_new')
    print manager_operate.get_file(user2, cloud_file_name, local_file_path + '_new')
    #
    # print ""
    # print "search file"
    # res = statistics_operate.search_file(user1, cloud_file_name)
    # print "查找用户1中的某个文件", res
    # res = statistics_operate.search_file(user2, cloud_file_name)
    # print "查找用户2中的某个文件", res
    # res = statistics_operate.search_file(user1, "checkfile")
    # print "正则匹配文件查找", res
    # res = statistics_operate.search_file(user1, "dir")
    # print "正则匹配文件夹查找", res
    # res = statistics_operate.search_file("wrong", cloud_file_name)
    # print "用户不存在", res
    # res = statistics_operate.search_file(user1, "wrong")
    # print "查找的文件不存在", res

    print ""
    print "list cloud region"
    res = statistics_operate.list_cloud_region()
    print "列出所有的云地域名", res

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
    res = statistics_operate.user_multicloud_traffic(user1)
    print "一个用户的上传下载使用流量(在每个jcsproxy上传下载到哪些云地域中)", res
    res = statistics_operate.user_used_traffic("wrong")
    print "用户不存在", res

    print "jcsproxy used traffic"
    res = statistics_operate.jcsproxy_used_traffic()
    print "每个jcsproxy的上传下载使用流量", res
    res = statistics_operate.jcsproxy_multicloud_traffic()
    print "每个jcsproxy用户的上传下载使用流量(在每个jcsproxy上传下载到哪些云地域中)", res




    # print "删除测试用户和测试文件"