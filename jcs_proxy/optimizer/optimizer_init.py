# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/5/14 16:13'

import matplotlib
matplotlib.use('Agg')

from config.cloud_information import CloudInformation
from jcsproxy_latency_time import JcsproxyLatencyTime
from jcsproxy_storage_cost import JcsproxyStorageCost

class OptimizerInit(object):
    def __init__(self, file_size, storage_time, jcsproxy_request_features,
                 fault_tolerance_features, target_weights):
        self.fault_tolerance_features = fault_tolerance_features
        self.target_weights = target_weights
        self.storage_time = storage_time

        jcsproxy_request_features = self.jcsproxy_request_features_delete0(jcsproxy_request_features)
        self.jcsproxy_request_features = jcsproxy_request_features
        self.jcsproxy_request_weights = self.get_jcsproxy_request_weights(jcsproxy_request_features)
        self.jcsproxy_area_list = jcsproxy_request_features.keys()
        self.jcsproxy_storage_features = self.get_jcsproxy_storage_features(file_size, storage_time, jcsproxy_request_features)

        self.cloud_bucket_list = CloudInformation().get_cloud_bucket_list()
        self.jcsproxy_latency_time_list = JcsproxyLatencyTime().get_jcsproxy_latency_time_list(self.jcsproxy_area_list)
        self.jcsproxy_latency_time_sort = JcsproxyLatencyTime().get_jcsproxy_latency_time_sort(self.jcsproxy_area_list)
        self.jcsproxy_latency_time_weights_sum_list = JcsproxyLatencyTime().get_latency_time_weights_sum_list(self.jcsproxy_area_list, self.jcsproxy_request_weights)
        self.jcsproxy_latency_time_weights_sum_sort = JcsproxyLatencyTime().get_latency_time_weights_sum_sort(self.jcsproxy_area_list, self.jcsproxy_request_weights)
        self.jcsproxy_storage_cost_list = JcsproxyStorageCost().get_jcsproxy_storage_cost_list(self.jcsproxy_storage_features, self.fault_tolerance_features)
        self.jcsproxy_storage_cost_sort = JcsproxyStorageCost().get_jcsproxy_storage_cost_sort(self.jcsproxy_storage_features, self.fault_tolerance_features)

        # print "输入参数"
        # print 'self.fault_tolerance_features', self.fault_tolerance_features
        # print 'self.target_weights', self.target_weights
        #
        # print 'self.jcsproxy_request_features', self.jcsproxy_request_features
        # print 'self.jcsproxy_area_list', self.jcsproxy_area_list
        # print 'self.jcsproxy_request_weights', self.jcsproxy_request_weights
        # print 'self.jcsproxy_storage_features', self.jcsproxy_storage_features
        #
        # print 'self.cloud_bucket_list', self.cloud_bucket_list
        # print 'self.jcsproxy_latency_time_list', self.jcsproxy_latency_time_list
        # print 'self.jcsproxy_latency_time_sort', self.jcsproxy_latency_time_sort
        # print 'self.jcsproxy_latency_time_weights_sum_list' , self.jcsproxy_latency_time_weights_sum_list
        # print 'self.jcsproxy_latency_time_weights_sum_sort' , self.jcsproxy_latency_time_weights_sum_sort
        # print 'self.jcsproxy_storage_cost_list', self.jcsproxy_storage_cost_list
        # print 'self.jcsproxy_storage_cost_sort', self.jcsproxy_storage_cost_sort


    def jcsproxy_request_features_delete0(self, jcsproxy_request_features):
        # 删除jcsproxy_request_features中的request==0的项
        request_area_list = []
        for jcsproxy_area in jcsproxy_request_features:
            if jcsproxy_request_features[jcsproxy_area] == 0:
                request_area_list.append(jcsproxy_area)
        for jcsproxy_area in request_area_list:
            jcsproxy_request_features.pop(jcsproxy_area)
        return jcsproxy_request_features

    def get_jcsproxy_request_weights(self, jcsproxy_request_features):
        # 下载量权重
        jcsproxy_request_weights = {}
        sum_request = 0
        for jcsproxy_area in jcsproxy_request_features:
            sum_request += jcsproxy_request_features[jcsproxy_area]
        for jcsproxy_area in jcsproxy_request_features:
            jcsproxy_request_weights[jcsproxy_area] = jcsproxy_request_features[jcsproxy_area]/(float)(sum_request)
        return jcsproxy_request_weights

    def get_jcsproxy_storage_features(self, file_size, storage_time, jcsproxy_request_features):
        jcsproxy_storage_features = {}
        for jcsproxy_area in jcsproxy_request_features:
            storage_features = {   # 存储特性
                'storage_size': file_size,
                'storage_time': storage_time,
                'download_size': None,  # download_size = storage_size * storage_time * request_frequency
                'request_frequency': jcsproxy_request_features[jcsproxy_area],
            }
            storage_features['download_size'] = storage_features['storage_size'] * storage_features['storage_time'] * \
                                                storage_features['request_frequency']
            jcsproxy_storage_features[jcsproxy_area] = storage_features
        return jcsproxy_storage_features



if __name__ == '__main__':
    # 输入参数
    jcsproxy_request_features = {
        'aliyun-beijing': 3,
        'aliyun-shanghai': 0,
        'aliyun-shenzhen': 3,
    }
    file_size = 1024
    storage_time = 1

    fault_tolerance_features = {  # 容错特性
        'fault_tolerance_level': 1,
        'erasure_code_k': 4,
        'erasure_code_n': 5,  # erasure_code_n = erasure_code_k + fault_tolerance_level
    }
    # fault_tolerance_features['erasure_code_n'] = fault_tolerance_features['fault_tolerance_level'] + \
    #                                              fault_tolerance_features['erasure_code_k']

    target_weights = {}  # 优化目标权重
    target_weights['storage_cost_weight'] = 0.5
    target_weights['latency_time_weight'] = 1 - target_weights['storage_cost_weight']

    print "optimizer init"
    optimizer_init = OptimizerInit(file_size, storage_time, jcsproxy_request_features,
                 fault_tolerance_features, target_weights)
