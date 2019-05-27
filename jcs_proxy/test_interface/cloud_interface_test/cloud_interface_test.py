# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/1/15 15:34'

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))
from cloud_interface.cloud_interface import CloudInterface
from config.cloud_information import CloudInformation
import datetime
from config.configuration import CONFIG
import logging
logging.basicConfig(level=logging.INFO)

class CloudInterfaceTest(object):
    def __init__(self, auth_info):
        logging.info("start")
        print ""
        print("auth_info: ", auth_info)
        self.cloud_operate = CloudInterface(auth_info)

    def check_auth_info_test(self):
        print "check_auth_info test"
        cloud_info = CloudInformation()
        aliyun_account = cloud_info.get_cloud_account_from_cloud_name('aliyun')
        print(CloudInterface(aliyun_account).check_auth_info())
        aliyun_account['accesskey_id'] = "wrong"
        print(CloudInterface(aliyun_account).check_auth_info())

        baidu_account = cloud_info.get_cloud_account_from_cloud_name('baidu')
        print(CloudInterface(baidu_account).check_auth_info())
        baidu_account['accesskey_secret'] = "wrong"
        print(CloudInterface(baidu_account).check_auth_info())

        ksyun_account = cloud_info.get_cloud_account_from_cloud_name('ksyun')
        print(CloudInterface(ksyun_account).check_auth_info())
        ksyun_account['endpoint'] = "wrong"
        print(CloudInterface(ksyun_account).check_auth_info())



    # def check_auth_info_test(self):
    #     print("check_auth_info test: aliyun: ")
    #     aliyun_info = auth_origin["aliyun_origin"]
    #     print(CloudInterface(aliyun_info).check_auth_info())
    #     aliyun_info = auth_ak_error["aliyun_AK_error"]
    #     print(CloudInterface(aliyun_info).check_auth_info())
    #     aliyun_info = auth_endpoint_error["aliyun_endpoint_error"]
    #     print(CloudInterface(aliyun_info).check_auth_info())
    #     aliyun_info = auth_bucker_error["aliyun_bucket_error"]
    #     print(CloudInterface(aliyun_info).check_auth_info())
    #
    #     print("check_auth_info test: baidu: ")
    #     baidu_info = auth_origin["baidu_origin"]
    #     print(CloudInterface(baidu_info).check_auth_info())
    #     baidu_info = auth_ak_error["baidu_AK_error"]
    #     print(CloudInterface(baidu_info).check_auth_info())
    #     baidu_info = auth_endpoint_error["baidu_endpoint_error"]
    #     print(CloudInterface(baidu_info).check_auth_info())
    #     baidu_info = auth_bucker_error["baidu_bucket_error"]
    #     print(CloudInterface(baidu_info).check_auth_info())
    #
    #     print("check_auth_info test: ksyun: ")
    #     ksyun_info = auth_origin["ksyun_origin"]
    #     print(CloudInterface(ksyun_info).check_auth_info())
    #     ksyun_info = auth_ak_error["ksyun_AK_error"]
    #     print(CloudInterface(ksyun_info).check_auth_info())
    #     ksyun_info = auth_endpoint_error["ksyun_endpoint_error"]
    #     print(CloudInterface(ksyun_info).check_auth_info())
    #     ksyun_info = auth_bucker_error["ksyun_bucket_error"]
    #     print(CloudInterface(ksyun_info).check_auth_info())

    def check_file_exists_test(self, cloud_path):
        print("cloud_file_exists test")
        # 1.云端文件存在
        print(self.cloud_operate.check_file_exists(cloud_path))
        # 2.云端文件不存在
        print(self.cloud_operate.check_file_exists("wrong"))

    def cloud_put_file_test(self, cloud_path, file_path):
        print("cloud_put_file test")
        # 1.上传文件
        print(self.cloud_operate.put_file(cloud_path, file_path))
        # 2.上传文件，本地文件路径错误，操作失败
        print(self.cloud_operate.put_file(cloud_path, "wrong"))
        # 3.上传文件，云端存在此文件，则覆盖
        print(self.cloud_operate.put_file(cloud_path, file_path))

    def cloud_get_file_test(self, cloud_path, file_path):
        print("cloud_get_file test")
        # 1.下载文件
        print(self.cloud_operate.get_file(cloud_path, file_path))
        # 2.下载文件，云端不存在此文件，操作失败
        print(self.cloud_operate.get_file("wrong", file_path))

    # def cloud_get_url_test(self, cloud_path, file_path):
    #     print("cloud_get_url test")
    #     # 1.获取文件url
    #     print(self.cloud_operate.get_url(cloud_path))
    #     # 2.获取文件url，云端不存在此文件，操作失败
    #     print(self.cloud_operate.get_url("wrong"))
    #     # 3.获取文件url，修改url连接的文件名
    #     print(self.cloud_operate.get_url(cloud_path, file_path))

    def cloud_delete_file_test(self, cloud_path):
        print("cloud_delete_file test")
        # 1.删除文件
        print(self.cloud_operate.delete_file(cloud_path))
        # 2.删除文件，云端不存在此文件
        print(self.cloud_operate.delete_file("wrong"))

    def cloud_list_file_test(self):
        print("cloud_list_file test")
        # 列表
        print(self.cloud_operate.list_file())


    def run_test(self):
        cloud_path = "cloud_interface_test/remote.txt"
        file_path = os.path.join(CONFIG["test_file_path"], "文件.txt")

        # cloud_path = "liuyf/remote.txt"
        # file_path = "../test_file/test.txt"
        # cloud_path = "刘/目录"
        # file_path = "../test_file/文件.txt"
        self.cloud_put_file_test(cloud_path, file_path)
        self.check_file_exists_test(cloud_path)

        self.cloud_get_file_test(cloud_path, file_path)
        # self.cloud_get_url_test(cloud_path, file_path)
        self.cloud_list_file_test()
        #self.cloud_delete_file_test(cloud_path)


if __name__ == '__main__':
    print(datetime.datetime.now())
    cloud_info = CloudInformation()
    aliyun_account = cloud_info.get_cloud_account_from_cloud_name('aliyun')
    # baidu_account = cloud_info.get_cloud_account_from_cloud_name('baidu')
    # ksyun_account = cloud_info.get_cloud_account_from_cloud_name('ksyun')
    CloudInterfaceTest(aliyun_account).run_test()
    # CloudInterfaceTest(baidu_account).run_test()
    # CloudInterfaceTest(ksyun_account).run_test()

    # CloudInterfaceTest(aliyun_account).check_auth_info_test()



