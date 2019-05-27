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
    # user信息存取相关接口测试
    # proxy提供user接口，portal将用户名和密码存入proxy，
    # 用户登录时，portal向portal请求用户信息，portal端得到用户信息后进行验证匹配是否正确

    print "测试，用户账号接口"
    print "连接RPC服务器"
    # server_rpc = ServerProxy("http://your-ip-address-here:8889")
    server_rpc = ServerProxy("http://"+SERVER["host"]+":"+str(SERVER["port"]))
    user_operate = server_rpc

    # 设置测试参数
    user_name = 'actuser43'
    password = 'actuser'
    others = {'mail':"sldkfjowiej@163.com", 'phone': "1128471982"}
    # user_name = '刘'
    # password = '密码'
    # others = {'mail': "飞云@163.com", 'phone': "1128471982"}

    print "测试用户账号接口"
    print("create cloud info")
    res = user_operate.create_user(user_name, password, others)
    # print "插入用户账号信息", res
    # res = user_operate.create_user(user_name, password, others)
    # print "用户已经存在，操作失败", res

    # print("update user info")
    # res = user_operate.update_user(user_name, password, others)
    # print "更新用户账号信息", res

    # print("check user exists")
    # res = user_operate.check_user_exists(user_name)
    # print "检查用户是否存在，已经存在", res
    # res = user_operate.check_user_exists("wrong")
    # print "检查用户是否存在，不存在", res

    # print("get user info")
    # res = user_operate.get_user(user_name)
    # print "获取用户账号信息", res
    # res = user_operate.get_user("wrong")
    # print "用户不存在，操作失败", res

    # print("delete user info")  # 删除用户账户信息
    # res = user_operate.delete_user(user_name)
    # print "删除用户账号信息", res
    # res = user_operate.delete_user(user_name)  # user不存在
    # print "用户不存在，操作失败", res

    # print("check user exists")
    # print "测试完毕，查看测试账号是否存在"
    # res = user_operate.check_user_exists(user_name)
    # print res