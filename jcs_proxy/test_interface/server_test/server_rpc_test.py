# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/1/17 20:53'

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))
from xmlrpclib import ServerProxy
from config.configuration import SERVER, CONFIG
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


if __name__ == '__main__':
    print "测试，文件操作接口"
    print "连接RPC服务器"
    # server_rpc = ServerProxy("http://your-ip-address-here:8889")
    server_rpc = ServerProxy("http://"+SERVER["host"]+":"+str(SERVER["port"]))
    manager_operate = server_rpc

    # 设置测试参数(英文)
    # user_name = "liuyf_test"  # 用户名
    # dir_path = "dir"
    # cloud_file_path = os.path.join(dir_path, "remote.txt")
    # local_file_path = os.path.join(CONFIG["test_file_path"], "test.txt")

    user_name = "actuser"  # 用户名
    dir_path = "dir"
    cloud_file_path = os.path.join(dir_path, "文件.txt")
    local_file_path = os.path.join(CONFIG["test_file_path"], "文件.txt")

    print "测试文件操作接口"
    print("manager put file")
    res = manager_operate.put_file(user_name, cloud_file_path, local_file_path)
    print "正常上传文件", res
    print res['result']['cloud_operate_time_res']
    res = manager_operate.put_file(user_name, cloud_file_path, local_file_path)
    print "文件已经存在，操作失败",res
    res = manager_operate.put_file(user_name, cloud_file_path, local_file_path, True)
    print "文件已经存在，覆盖上传文件", res
    print res['result']['cloud_operate_time_res']
    res = manager_operate.put_file(user_name, cloud_file_path, "wrong")
    print "本地上传文件路径错误，操作失败", res

    print("manager get file")
    res = manager_operate.get_file(user_name, cloud_file_path, local_file_path)
    print "正常下载文件", res
    print res['result']['cloud_operate_time_res']
    res = manager_operate.get_file(user_name, "wrong", local_file_path)
    print "云上文件不存在，下载失败", res

    print("manager list dir")
    res = manager_operate.list_dir(user_name, "")
    print "列出用户根目录下所有文件", res
    res = manager_operate.list_dir(user_name, dir_path)
    print "列出用户dir_path目录下所有文件", res
    res = manager_operate.list_dir(user_name, "wrong")
    print "用户目录不存在，操作失败", res

    print("manage delete file")
    res = manager_operate.delete_file(user_name, cloud_file_path)
    print "正常删除文件", res
    res = manager_operate.delete_file(user_name, cloud_file_path)
    print "云上文件不存在，删除失败", res

    print("manage create dir")
    res = manager_operate.create_dir(user_name, dir_path + "/new/dir1/1")
    print "正常新建文件夹", res
    res = manager_operate.create_dir(user_name, dir_path + "/new/dir1/1")
    print "文件夹已经存在，操作失败", res

    print("manage delete dir")
    res = manager_operate.delete_dir(user_name, dir_path + "/new/dir1")
    print "文件夹不为空，操作失败", res
    res = manager_operate.delete_dir(user_name, dir_path + "/new/dir1", True)
    print "文件夹不为空，递归删除", res
    res = manager_operate.delete_dir(user_name, dir_path + "/new")
    print "文件夹为空，正常删除文件夹", res
    res = manager_operate.delete_dir(user_name, dir_path + "/new")
    print "文件夹不存在，删除失败", res

    print "测试完毕，删除测试用户的所有目录"
    res = manager_operate.delete_dir(user_name, "", True)
    print(res)
