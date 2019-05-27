# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/1/19 12:13'

from metadata.user_info import MetadataUserInfo
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    print("matedata user info")
    metadata_user_info = MetadataUserInfo()

    # user_name = "liuyf"
    # user_info = {"user_name": "liuyf", "user_password": "wjeq2r023lk"}
    user_name = "刘用户"
    user_info = {"user_name": "刘用户", "user_password": "刘用户的密码"}

    print("check user exists")
    res = metadata_user_info.check_user_exists(user_name)
    print(res)

    print("create cloud info")
    res = metadata_user_info.create_user_info(user_name, user_info)
    print(res)
    res = metadata_user_info.create_user_info(user_name, user_info)  # 已存在，操作失败
    print(res)
    print("update user info")
    res = metadata_user_info.update_user_info(user_name, user_info)
    print(res)

    print("check user exists")
    res = metadata_user_info.check_user_exists(user_name)
    print(res)


    print("get user info")
    res = metadata_user_info.get_user_info(user_name)
    print(res)
    res = metadata_user_info.get_user_info("wrong")  # 不存在，操作失败
    print(res)

    print("list user name")
    res = metadata_user_info.list_user_name()
    print(res)
    print("list user info")
    res = metadata_user_info.list_user_info()
    print(res)

    print("delete user info")
    res = metadata_user_info.delete_user_info(user_name)
    print(res)
    res = metadata_user_info.delete_user_info(user_name)  # 不存在，操作失败
    print(res)

    metadata_user_info.zk_stop()  # 关闭连接

