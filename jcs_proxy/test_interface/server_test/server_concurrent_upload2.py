# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/6/13 17:27'

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))
from xmlrpclib import ServerProxy
from config.configuration import SERVER, CONFIG
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

"""
并发上传测试
1和2同时执行
"""


if __name__ == '__main__':
    print "测试，文件操作接口"
    print "连接RPC服务器"
    server_rpc = ServerProxy("http://your-ip-address-here:8889")
    # server_rpc = ServerProxy("http://"+SERVER["host"]+":"+str(SERVER["port"]))
    manager_operate = server_rpc

    user_name = "刘_测试"
    dir_path = "目录"
    cloud_file_path = dir_path+"/云文件2.txt"
    # local_file_path = "/storage/liuyf_test/jcsProxyDir/datatest/test_128"
    local_file_path = "/storage/ivic/liuyf/jcsProxyDir/datatest/test_16"

    print "测试文件操作接口"
    print("manager put file")
    res = manager_operate.put_file(user_name, cloud_file_path, local_file_path, True)
    print "正常上传文件", res