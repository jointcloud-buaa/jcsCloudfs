# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/10/7 21:00'

from metadata.cloud_bucket_info import MetadataCloudBucketInfo
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

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
    print("metadata cloud bucket info test")
    metadata_cloud_bucket_info = MetadataCloudBucketInfo()

    res = metadata_cloud_bucket_info.get_bucket_list_from_num(1)
    print "可用云列表", res
    res = metadata_cloud_bucket_info.get_bucket_list_from_num(2)
    print "临时故障云列表", res
    res = metadata_cloud_bucket_info.get_bucket_list_from_num(3)
    print "超时故障云列表", res
    res = metadata_cloud_bucket_info.get_bucket_list_from_num(4)
    print "待删除云列表", res

    print "云列表bucket_name:"
    print_cloud_bucket_lists(metadata_cloud_bucket_info)


    print ""
    metadata_cloud_bucket_info.exchange_bucket(1, 2, "jcsproxy-aliyun-beijing")
    print "可用云->临时故障云，bucket_name: jcsproxy-aliyun-beijing"
    print_cloud_bucket_lists(metadata_cloud_bucket_info)
    metadata_cloud_bucket_info.exchange_bucket(1, 2, "jcsproxy-aliyun-shanghai")
    print "可用云->临时故障云，bucket_name: jcsproxy-aliyun-shanghai"
    print_cloud_bucket_lists(metadata_cloud_bucket_info)
    metadata_cloud_bucket_info.exchange_bucket(2, 1, "jcsproxy-aliyun-beijing")
    print "临时故障云->可用云，bucket_name: jcsproxy-aliyun-beijing"
    print_cloud_bucket_lists(metadata_cloud_bucket_info)
    metadata_cloud_bucket_info.exchange_bucket(2, 3, "jcsproxy-aliyun-shanghai")
    print "临时故障云->超时故障云，bucket_name: jcsproxy-aliyun-shanghai"
    print_cloud_bucket_lists(metadata_cloud_bucket_info)
    metadata_cloud_bucket_info.exchange_bucket(3, 1, "jcsproxy-aliyun-shanghai")
    print "超时故障云->可用云，bucket_name: jcsproxy-aliyun-shanghai"
    print_cloud_bucket_lists(metadata_cloud_bucket_info)


    print ""
    bucket_info = {'cloud_name': 'aliyun', 'area_name': 'qingdao', 'storage_type': 'standard',
     'bucket_name': 'jcsproxy-aliyun-qingdao-test', 'endpoint': 'http://oss-cn-qingdao.aliyuncs.com'}
    metadata_cloud_bucket_info.insert_cloud_bucket(bucket_info)
    print "可用云，插入新的云信息, bucket_name: ", bucket_info['bucket_name']
    print_cloud_bucket_lists(metadata_cloud_bucket_info)

    metadata_cloud_bucket_info.exchange_bucket(1, 4, bucket_info['bucket_name'])
    print "可用云->待删除云，bucket_name: ", bucket_info['bucket_name']
    print_cloud_bucket_lists(metadata_cloud_bucket_info)

    metadata_cloud_bucket_info.remove_cloud_bucket(bucket_info['bucket_name'])
    print "待删除云，删除云信息, bucket_name: ", bucket_info['bucket_name']
    print_cloud_bucket_lists(metadata_cloud_bucket_info)



    print ""
    res = metadata_cloud_bucket_info.get_waiting_delete_file_list()
    print "待删除文件列表", res

    bucket_file_list = [{u'jcsproxy-aliyun-qingdao-low': 'liuyf_test/liuyf/remote.txt.2_5.fec'}, {u'jcsproxy-aliyun-huhehaote-low': 'liuyf_test/liuyf/remote.txt.1_5.fec'}, {u'jcsproxy-aliyun-zhangjiakou': 'liuyf_test/liuyf/remote.txt.3_5.fec'}]
    metadata_cloud_bucket_info.insert_waiting_delete_file(bucket_file_list)
    res = metadata_cloud_bucket_info.get_waiting_delete_file_list()
    print "插入由于云故障不可删除的文件"
    print "待删除文件列表", len(res), res

    res = metadata_cloud_bucket_info.get_waiting_delete_file_by_bucket_name("jcsproxy-aliyun-qingdao-low")
    print "得到某个bucket_name中未删除的文件", len(res), res

    metadata_cloud_bucket_info.remove_waiting_delete_file(bucket_file_list)
    res = metadata_cloud_bucket_info.get_waiting_delete_file_list()
    print "某些待删除的文件已经被删除"
    print "待删除文件列表", res


