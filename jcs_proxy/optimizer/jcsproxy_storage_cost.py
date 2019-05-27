# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/5/22 16:10'

import copy
from storage_cost import StorageCost
from config.cloud_information import CloudInformation

class JcsproxyStorageCost(object):
    def __init__(self):
        pass

    def get_jcsproxy_block_storage_features(self, jcsproxy_storage_features, fault_tolerance_features):
        jcsproxy_block_storage_features = {}
        for jcsproxy_area in jcsproxy_storage_features:
            block_storage_features = copy.deepcopy(jcsproxy_storage_features[jcsproxy_area])
            block_storage_features['storage_size'] /= (float)(fault_tolerance_features['erasure_code_k'])
            block_storage_features['download_size'] /= (float)(fault_tolerance_features['erasure_code_k'])
            jcsproxy_block_storage_features[jcsproxy_area] = block_storage_features
        return jcsproxy_block_storage_features

    def get_jcsproxy_storage_cost_list(self, jcsproxy_storage_features, fault_tolerance_features):
        jcsproxy_block_storage_features = self.get_jcsproxy_block_storage_features(jcsproxy_storage_features, fault_tolerance_features)
        jcsproxy_storage_cost_list = {}
        for jcsproxy_area in jcsproxy_block_storage_features:
            block_storage_features = jcsproxy_block_storage_features[jcsproxy_area]
            block_storage_cost_list = StorageCost().get_storage_cost_list(block_storage_features)  # 分块存储成本
            jcsproxy_storage_cost_list[jcsproxy_area] = block_storage_cost_list
        return jcsproxy_storage_cost_list

    def get_jcsproxy_storage_cost_sort(self, jcsproxy_storage_features, fault_tolerance_features):
        jcsproxy_block_storage_features = self.get_jcsproxy_block_storage_features(jcsproxy_storage_features, fault_tolerance_features)
        jcsproxy_storage_cost_sort = {}
        for jcsproxy_area in jcsproxy_block_storage_features:
            block_storage_features = jcsproxy_block_storage_features[jcsproxy_area]
            jcsproxy_storage_cost_sort[jcsproxy_area] = {}
            storage_expense_list = ["storage_expense", "download_expense", "request_expense", "sum_expense"]
            for storage_expense_name in storage_expense_list:
                block_expense_sort = StorageCost().get_storage_cost_sort(block_storage_features, storage_expense_name)
                block_expense_sort = self.get_cloud_bucket_index(block_expense_sort)
                jcsproxy_storage_cost_sort[jcsproxy_area][storage_expense_name] = block_expense_sort
        return jcsproxy_storage_cost_sort

    ####################################################################################################

    def get_cloud_bucket_index(self, area_sort):
        # 根据area_sort中的bucket_name，添加对应的cloud_bucket_index
        cloud_bucket_list = CloudInformation().get_cloud_bucket_list()
        for area_sort_one in area_sort:
            for cloud_bucket in cloud_bucket_list:
                if cloud_bucket['bucket_name'] == area_sort_one['bucket_name']:
                    cloud_bucket_index = cloud_bucket_list.index(cloud_bucket)
                    area_sort_one['cloud_bucket_index'] = cloud_bucket_index
                    break
        return area_sort

    def myprintdict(self, mydict, mydict_name):
        print mydict_name
        for key in mydict:
            print key, mydict[key]

    def myprintlist(self, mylist, mylist_name):
        print mylist_name
        for one in mylist:
            print one

if __name__ == '__main__':
    jcsproxy_storage_features = \
        {'aliyun-shenzhen': {'download_size': 4028, 'request_frequency': 4, 'storage_size': 1024, 'storage_time': 1},
         'aliyun-beijing': {'download_size': 3072, 'request_frequency': 3, 'storage_size': 1024, 'storage_time': 1}}
    fault_tolerance_features = \
        {'erasure_code_k': 3, 'erasure_code_n': 5, 'fault_tolerance_level': 2}

    jcsproxy_storage_cost = JcsproxyStorageCost()
    jcsproxy_block_storage_features = jcsproxy_storage_cost.get_jcsproxy_block_storage_features(jcsproxy_storage_features, fault_tolerance_features)
    jcsproxy_storage_cost.myprintdict(jcsproxy_block_storage_features, "jcsproxy_block_storage_features")
    jcsproxy_storage_cost_list = jcsproxy_storage_cost.get_jcsproxy_storage_cost_list(jcsproxy_storage_features, fault_tolerance_features)
    jcsproxy_storage_cost.myprintdict(jcsproxy_storage_cost_list, "jcsproxy_storage_cost_list")
    jcsproxy_storage_cost_sort = jcsproxy_storage_cost.get_jcsproxy_storage_cost_sort(jcsproxy_storage_features, fault_tolerance_features)
    jcsproxy_storage_cost.myprintdict(jcsproxy_storage_cost_sort, "jcsproxy_storage_cost_sort")

    jcsproxy_storage_cost.myprintlist(jcsproxy_storage_cost_list['aliyun-shenzhen'], "jcsproxy_storage_cost_list['aliyun-shenzhen']")
    jcsproxy_storage_cost.myprintlist(jcsproxy_storage_cost_sort['aliyun-beijing']['download_expense'], "jcsproxy_storage_cost_sort['aliyun-beijing']['download_expense']")

    print ""
    jcsproxy_area = "aliyun-beijing"
    print jcsproxy_area
    for storage_cost in jcsproxy_storage_cost_list[jcsproxy_area]:
        print round(storage_cost['download_expense'], 4)

    print ""
    jcsproxy_area = "aliyun-shenzhen"
    print jcsproxy_area
    for storage_cost in jcsproxy_storage_cost_list[jcsproxy_area]:
        print round(storage_cost['download_expense'], 4)