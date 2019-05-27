# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/10/7 22:34'

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))
from manager.manager_interface import ManagerInterface
from metadata.cloud_bucket_info import MetadataCloudBucketInfo
from manager.cloud_fault_handler import CloudFaultHandler
from config.configuration import CONFIG
from tools.get_func_time import GetFuncTime


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
    # 文件路径
    file_size = 16
    user_name = "liuyf_test"
    cloud_file_path = "dir/test_" + str(file_size)
    local_file_path = os.path.join(CONFIG["test_file_path"], "test_" + str(file_size))

    # 配置参数
    storage_time = 1
    jcsproxy_request_features = {
        'aliyun-beijing': 1000,
        'aliyun-shanghai': 0,
        'aliyun-shenzhen': 1000,
    }
    fault_tolerance_features = None
    target_weights = {}
    target_weights['storage_cost_weight'] = 0.5
    target_weights['latency_time_weight'] = 0.5


    manager_operate = ManagerInterface()
    cloud_bucket_operate = MetadataCloudBucketInfo()
    cloud_fault_handler = CloudFaultHandler()

    print ""
    print "测试，可用云->临时故障云，下载过程"
    # res = manager_operate.put_file(user_name, cloud_file_path, local_file_path, True)
    res, func_time = GetFuncTime().get_func_time(manager_operate.put_file,
                                                 (user_name, cloud_file_path, local_file_path, True,
                                                  storage_time, jcsproxy_request_features, fault_tolerance_features,
                                                  target_weights,))
    print "正常上传文件，覆盖", res
    print res['result']['file_info']['cloud_block_path_dict'].keys()
    print func_time


    # res = manager_operate.get_file(user_name, cloud_file_path, local_file_path)
    res, func_time = GetFuncTime().get_func_time(manager_operate.get_file,
                                                 (user_name, cloud_file_path, local_file_path))
    print "正常下载文件", res
    print res['result']['download_bucket_name_list']
    print func_time


    cloud_bucket_operate.exchange_bucket(1, 2, "jcsproxy-aliyun-beijing")
    print "可用云->临时故障云, bucket_name: jcsproxy-aliyun-beijing"
    print_cloud_bucket_lists(cloud_bucket_operate)

    # res = manager_operate.get_file(user_name, cloud_file_path, local_file_path)
    res, func_time = GetFuncTime().get_func_time(manager_operate.get_file,
                                                 (user_name, cloud_file_path, local_file_path))
    print "下载文件", res
    print res['result']['download_bucket_name_list']
    print func_time

    print ""
    cloud_bucket_operate.exchange_bucket(2, 1, "jcsproxy-aliyun-beijing")
    print "临时故障云->可用云, bucket_name: jcsproxy-aliyun-beijing"
    print_cloud_bucket_lists(cloud_bucket_operate)

    # res = manager_operate.get_file(user_name, cloud_file_path, local_file_path)
    res, func_time = GetFuncTime().get_func_time(manager_operate.get_file,
                                                 (user_name, cloud_file_path, local_file_path))
    print "下载文件", res
    print res['result']['download_bucket_name_list']
    print func_time

    print "测试完毕，删除测试用户的所有目录"
    res = manager_operate.delete_dir(user_name, "", True)
    print(res)

