# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/12/13 11:51'

from metadata.cloud_bucket_info import MetadataCloudBucketInfo
from manager.cloud_fault_handler import CloudFaultHandler

def print_cloud_bucket_list_one(cloud_bucket_list, cloud_bucket_name_str=""):
    print cloud_bucket_name_str, len(cloud_bucket_list), ":"
    if len(cloud_bucket_list) == 0:
        return
    for bucket_one in cloud_bucket_list:
        print bucket_one['bucket_name'], " "

def print_cloud_bucket_lists(cloud_bucket_operate):
    """
    输出云列表中云地域名，len, buclet_names
    :return:
    """
    res = cloud_bucket_operate.get_bucket_list_from_num(1)
    print "get_avalible_fault_bucket_list", len(res)
    res = cloud_bucket_operate.get_bucket_list_from_num(2)
    print_cloud_bucket_list_one(res, "get_temporary_fault_bucket_list")
    res = cloud_bucket_operate.get_bucket_list_from_num(3)
    print_cloud_bucket_list_one(res, "get_permanent_fault_bucket_list")
    res = cloud_bucket_operate.get_bucket_list_from_num(4)
    print_cloud_bucket_list_one(res, "get_remove_bucket_list")

if __name__ == '__main__':
    cloud_fault_handler = CloudFaultHandler()
    cloud_bucket_operate = MetadataCloudBucketInfo()

    bucket_name = "jcsproxy-aliyun-beijing"

    # 云故障，从其他云存储下载
    cloud_bucket_operate.exchange_bucket(1, 2, bucket_name)
    print "可用云->临时故障云, bucket_name:", bucket_name
    print_cloud_bucket_lists(cloud_bucket_operate)

    # 云故障恢复，按原来的下载
    cloud_bucket_operate.exchange_bucket(2, 1, bucket_name)
    print "临时故障云->可用云, bucket_name:", bucket_name
    print_cloud_bucket_lists(cloud_bucket_operate)