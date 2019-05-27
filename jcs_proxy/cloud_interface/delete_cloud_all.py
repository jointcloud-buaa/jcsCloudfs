# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/5/9 16:50'

from config.cloud_information import CloudInformation
from cloud_interface import CloudInterface
import copy

def delete_cloud_all():
    # print "删除云上所有存储文件"
    cloud_info = CloudInformation()
    cloud_account_list = cloud_info.get_cloud_account_list()
    delete_account_list = copy.deepcopy(cloud_account_list)  # cloud_account_list做修改，需要复制

    cloud_bucket_list = cloud_info.get_cloud_bucket_list()
    for cloud_bucket in cloud_bucket_list:
        bucket_name = cloud_bucket['bucket_name']
        cloud_account = cloud_info.get_cloud_account_from_bucket_name(bucket_name)
        delete_account_list.append(copy.deepcopy(cloud_account))

    for cloud_account in delete_account_list:
        print "cloud_name", cloud_account['cloud_name'], "bucket_name", cloud_account['bucket_name']
        cloud_operate = CloudInterface(cloud_account)
        for i in range(20):  # 每次获取列表只是一部分，需要多次删除
            cloud_key_list = cloud_operate.list_file()['result']
            for cloud_key in cloud_key_list:
                print "delete file res:", cloud_operate.delete_file(cloud_key)
                print "cloud_name", cloud_account['cloud_name'], "bucket_name", cloud_account['bucket_name'], "delete", cloud_key

if __name__ == '__main__':
    delete_cloud_all()