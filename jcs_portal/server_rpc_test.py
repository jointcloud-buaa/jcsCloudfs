# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/1/17 20:53'

import os
from xmlrpc.client import ServerProxy
if __name__ == '__main__':
    print("server rpc test")
    server_rpc = ServerProxy("http://your-ip-address-here:8889")
    user_name = "liuyf"  # 用户名

    dir_path = "dir"
    cloud_file_path = "/"
    local_file_path = ""

    print("manager put file")
    print(os.path.exists(local_file_path))
    #res = server_rpc.put_file(user_name, cloud_file_path, local_file_path)  # put file, 正常
    #print(res)
    #res = server_rpc.put_file(user_name, cloud_file_path, local_file_path)  # put file, 文件已经存在，操作失败
    # print(res)
    # res = server_rpc.put_file(user_name, cloud_file_path, local_file_path, True)  # put file , 文件已经存在，覆盖文件
    # print(res)
    res = server_rpc.put_file(user_name, cloud_file_path, "wrong")  # put file，本地文件路径错误，操作失败
    print(res)
    #
    print("manager get url")
    res = server_rpc.get_url(user_name, cloud_file_path)  # get url, 正常
    print(res)
    res = server_rpc.get_url(user_name, "wrong")  # get url, 云端文件不存在
    print(res)

    print("manager get file")
    res = server_rpc.get_file(user_name, cloud_file_path, local_file_path)  # get file, 正常
    print(res)
    res = server_rpc.get_file(user_name, "wrong", local_file_path)  # get file, 云端文件不存在
    print(res)

    print("manager list dir")
    res = server_rpc.list_dir(user_name, "")  # list, 此用户的根目录下所有文件
    print(res)
    res = server_rpc.list_dir(user_name, "wrong")  # 路径不存在
    print(res)

    # print("manage delete file")
    # res = server_rpc.delete_file(user_name, cloud_file_path)  # delete file, 正常
    # print(res)
    res = server_rpc.delete_file(user_name, cloud_file_path)  # delete file, 云端文件不存在，操作失败
    print(res)
    #
    # print("manage create dir")
    res = server_rpc.create_dir(user_name, dir_path + "/new/dir1/1")  # create dir, 正常
    print(res)
    res = server_rpc.create_dir(user_name, dir_path + "/new/dir1/1")  # create dir, 文件夹已存在
    print(res)
    #
    # print("manage delete dir")
    # res = server_rpc.delete_dir(user_name, dir_path + "/new/dir1")  # delete dir, 文件夹不为空，操作失败
    # print(res)
    # res = server_rpc.delete_dir(user_name, dir_path + "/new/dir1", True)  # delete dir, 文件夹不为空，递归删除
    # print(res)
    res = server_rpc.delete_dir(user_name, dir_path + "/new")  # delete dir, 正常
    print(res)
    res = server_rpc.delete_dir(user_name, dir_path + "/new")  # delete dir, 文件夹不存在
    print(res)
    #
    # res = server_rpc.delete_dir(user_name, "", True)  # 删除用户所有目录
    # print(res)

##########################################################################################
# 输出结果：
# server rpc test
# manage put file
# {'status': 0, 'result': {'cloud_res_list': [{'status': 0, 'result': {}}, {'status': 0, 'result': {}}, {'status': 0, 'result': {}}], 'file_info': {'file_ctime': '2018-01-24 19:02:44', 'file_size': 21, 'file_key': 'liuyf/remote.txt', 'cloud_bucket_list': [{'cloud_name': 'baidu', 'bucket_name': 'g504bos'}, {'cloud_name': 'ksyun', 'bucket_name': 'g504ks3'}, {'cloud_name': 'aliyun', 'bucket_name': 'g504oss'}], 'file_md5': 'bb329056bb175a2df73ca641e998b65a'}, 'operdata_info': {'proxy_name': 'aliyun-beijing', 'file_operate': 'put_file', 'file_key': 'liuyf/remote.txt', 'cloud_trans_time_list': [{'trans_time': 0.294071, 'cloud_name': 'baidu', 'bucket_name': 'g504bos'}, {'trans_time': 0.052952, 'cloud_name': 'ksyun', 'bucket_name': 'g504ks3'}, {'trans_time': 0.30891, 'cloud_name': 'aliyun', 'bucket_name': 'g504oss'}], 'file_atime': '2018-01-24 19:02:45'}, 'file_operate': 'put_file'}}
# {'status': 1, 'result': 'liuyf/remote.txt already exists.'}
# {'status': 0, 'result': {'cloud_res_list': [{'status': 0, 'result': {}}, {'status': 0, 'result': {}}, {'status': 0, 'result': {}}], 'file_info': {'file_ctime': '2018-01-24 19:02:45', 'file_size': 21, 'file_key': 'liuyf/remote.txt', 'cloud_bucket_list': [{'cloud_name': 'baidu', 'bucket_name': 'g504bos'}, {'cloud_name': 'ksyun', 'bucket_name': 'g504ks3'}, {'cloud_name': 'aliyun', 'bucket_name': 'g504oss'}], 'file_md5': 'bb329056bb175a2df73ca641e998b65a'}, 'operdata_info': {'proxy_name': 'aliyun-beijing', 'file_operate': 'put_file', 'file_key': 'liuyf/remote.txt', 'cloud_trans_time_list': [{'trans_time': 0.171126, 'cloud_name': 'baidu', 'bucket_name': 'g504bos'}, {'trans_time': 0.073224, 'cloud_name': 'ksyun', 'bucket_name': 'g504ks3'}, {'trans_time': 0.177633, 'cloud_name': 'aliyun', 'bucket_name': 'g504oss'}], 'file_atime': '2018-01-24 19:02:45'}, 'file_operate': 'put_file'}}
# {'status': 1, 'result': 'wrong not exists.'}
# manage get url
# {'status': 0, 'result': {'file_operate': 'get_url', 'file_info': {'isdir': False, 'file_ctime': '2018-01-24 19:02:45', 'file_name': 'remote.txt', 'file_key': 'liuyf/remote.txt', 'file_md5': 'bb329056bb175a2df73ca641e998b65a', 'cloud_bucket_list': [{'cloud_name': 'baidu', 'bucket_name': 'g504bos'}, {'cloud_name': 'ksyun', 'bucket_name': 'g504ks3'}, {'cloud_name': 'aliyun', 'bucket_name': 'g504oss'}], 'file_size': 21}, 'userdata_info': {'proxy_name': 'aliyun-beijing', 'file_operate': 'get_url', 'file_key': 'liuyf/remote.txt', 'cloud_trans_time_list': [{'trans_time': 0.162736, 'cloud_name': 'aliyun', 'bucket_name': 'g504oss'}], 'file_atime': '2018-01-24 19:02:45'}, 'cloud_res': {'status': 0, 'result': 'http://g504oss.oss-cn-beijing.aliyuncs.com/liuyf%2Fremote.txt?OSSAccessKeyId=LTAIysnuCPnqOJWJ&response-content-disposition=attachment%3B%20filename%3Dliuyf%2Fremote.txt&Expires=1516795365&Signature=eInr7NOPq49wTS5S5l1Yt%2FtxTrs%3D'}}}
# {'status': 1, 'result': '/JCS-Proxy/metadata/file_info/liuyf/wrong not exists.'}
# manage get file
# {'status': 0, 'result': {'file_operate': 'get_file', 'file_info': {'isdir': False, 'file_ctime': '2018-01-24 19:02:45', 'file_name': 'remote.txt', 'file_key': 'liuyf/remote.txt', 'file_md5': 'bb329056bb175a2df73ca641e998b65a', 'cloud_bucket_list': [{'cloud_name': 'baidu', 'bucket_name': 'g504bos'}, {'cloud_name': 'ksyun', 'bucket_name': 'g504ks3'}, {'cloud_name': 'aliyun', 'bucket_name': 'g504oss'}], 'file_size': 21}, 'userdata_info': {'proxy_name': 'aliyun-beijing', 'file_operate': 'get_file', 'file_key': 'liuyf/remote.txt', 'cloud_trans_time_list': [{'trans_time': 0.33118, 'cloud_name': 'aliyun', 'bucket_name': 'g504oss'}], 'file_atime': '2018-01-24 19:02:46'}, 'cloud_res': {'status': 0, 'result': 'liuyf/remote.txt exists.'}}}
# {'status': 1, 'result': '/JCS-Proxy/metadata/file_info/liuyf/wrong not exists.'}
# manage list file
# {'status': 0, 'result': [{'isdir': False, 'file_ctime': '2018-01-24 19:02:45', 'file_name': 'remote.txt', 'file_key': 'liuyf/remote.txt', 'file_md5': 'bb329056bb175a2df73ca641e998b65a', 'cloud_bucket_list': [{'cloud_name': 'baidu', 'bucket_name': 'g504bos'}, {'cloud_name': 'ksyun', 'bucket_name': 'g504ks3'}, {'cloud_name': 'aliyun', 'bucket_name': 'g504oss'}], 'file_size': 21}]}
# {'status': 1, 'result': '/JCS-Proxy/metadata/file_info/liuyf/wrong not exists.'}
# manage delete file
# {'status': 0, 'result': {'cloud_res_list': [{'status': 0, 'result': 'liuyf/remote.txt exists.'}, {'status': 0, 'result': 'liuyf/remote.txt exists.'}, {'status': 0, 'result': 'liuyf/remote.txt exists.'}], 'file_info': {'isdir': False, 'file_ctime': '2018-01-24 19:02:45', 'file_name': 'remote.txt', 'file_key': 'liuyf/remote.txt', 'file_md5': 'bb329056bb175a2df73ca641e998b65a', 'cloud_bucket_list': [{'cloud_name': 'baidu', 'bucket_name': 'g504bos'}, {'cloud_name': 'ksyun', 'bucket_name': 'g504ks3'}, {'cloud_name': 'aliyun', 'bucket_name': 'g504oss'}], 'file_size': 21}, 'operdata_info': {'proxy_name': 'aliyun-beijing', 'file_operate': 'delete_file', 'file_key': 'liuyf/remote.txt', 'cloud_trans_time_list': [{'trans_time': 0.299667, 'cloud_name': 'baidu', 'bucket_name': 'g504bos'}, {'trans_time': 0.115188, 'cloud_name': 'ksyun', 'bucket_name': 'g504ks3'}, {'trans_time': 0.407439, 'cloud_name': 'aliyun', 'bucket_name': 'g504oss'}], 'file_atime': '2018-01-24 19:02:47'}, 'file_operate': 'delete_file'}}
# {'status': 1, 'result': '/JCS-Proxy/metadata/file_info/liuyf/remote.txt not exists.'}
# manage create dir
# {'status': 0, 'result': 'create node info, node path: /JCS-Proxy/metadata/file_info/liuyf/dir/new/dir1/1, node_info: '}
# {'status': 1, 'result': '/JCS-Proxy/metadata/file_info/liuyf/dir/new/dir1/1 already exists.'}
# manage delete dir
# {'status': 1, 'result': '/JCS-Proxy/metadata/file_info/liuyf/dir/new/dir1 not empty.'}
# {'status': 0, 'result': 'delete /JCS-Proxy/metadata/file_info/liuyf/dir/new/dir1'}
# {'status': 0, 'result': 'delete /JCS-Proxy/metadata/file_info/liuyf/dir/new'}
# {'status': 1, 'result': '/JCS-Proxy/metadata/file_info/liuyf/dir/new not exists.'}
# {'status': 0, 'result': 'delete /JCS-Proxy/metadata/file_info/liuyf/'}