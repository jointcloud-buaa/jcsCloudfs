# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/5/22 15:54'

from optimizer_init import OptimizerInit
import random

class PlacementNkInterface(object):
    def __int__(self):
        pass


    def get_placement_random(self, N, n):
        # N中随机选择n个
        N_list = range(N)
        n_list = []
        for i in range(n):
            random_index = random.randint(0, len(N_list)-1)
            n_list.append(N_list[random_index])
            N_list.pop(random_index)
        return n_list

    def get_placement_remaining(self, placement, N):
        # 哪些节点没有被选
        placement_check = [0]*N
        for placement_i in placement:
            placement_check[placement_i] = 1
        placement_remaining = []
        for i in range(N):
            if placement_check[i] == 0:
                placement_remaining.append(i)
        return placement_remaining


    ###############################################################################################

    def jcsproxy_latency_time_nk(self, placement, jcsproxy_placement_nk, optimizer_init):
        # 每一个jcsproxy_area，对应的placement_nk，的latency_time
        jcsproxy_latency_time_nk = {}
        for jcsproxy_area in optimizer_init.jcsproxy_area_list:
            if len(optimizer_init.jcsproxy_area_list) == 1:
                placement_nk = placement  # 只有一个地区，上传的延迟按n个计算
            else:
                placement_nk = jcsproxy_placement_nk[jcsproxy_area]
            max_latency = -1
            for placement_i in placement_nk:
                if optimizer_init.jcsproxy_latency_time_list[jcsproxy_area][placement_i]['latency_time'] > max_latency:
                    max_latency = optimizer_init.jcsproxy_latency_time_list[jcsproxy_area][placement_i]['latency_time']
            jcsproxy_latency_time_nk[jcsproxy_area] = max_latency
        return jcsproxy_latency_time_nk

    def jcsproxy_latency_time_value(self, jcsproxy_latency_time_nk, optimizer_init):
        # 所有jcsproxy_area的latecny_time加权和
        latency_time = 0
        for jcsproxy_area in optimizer_init.jcsproxy_area_list:
            latency_time += jcsproxy_latency_time_nk[jcsproxy_area] * optimizer_init.jcsproxy_request_weights[jcsproxy_area]
        return latency_time


    def jcsproxy_storage_cost_nk(self, placement, jcsproxy_placement_nk, optimizer_init):
        # 每一个jcsproxy_area，对应的placement_nk，的storage_cost
        jcsproxy_storage_cost_nk = {}
        for jcsproxy_area in optimizer_init.jcsproxy_area_list:
            placement_nk = jcsproxy_placement_nk[jcsproxy_area]
            storage_expense = 0
            download_expense = 0
            request_expense = 0
            for placement_i in placement:
                storage_expense += optimizer_init.jcsproxy_storage_cost_list[jcsproxy_area][placement_i]['storage_expense']
            for placement_i in placement_nk:
                download_expense += optimizer_init.jcsproxy_storage_cost_list[jcsproxy_area][placement_i]['download_expense']
                request_expense += optimizer_init.jcsproxy_storage_cost_list[jcsproxy_area][placement_i]['request_expense']
            cost_nk_res = {}
            cost_nk_res['storage_expense'] = storage_expense
            cost_nk_res['download_expense'] = download_expense
            cost_nk_res['request_expense'] = request_expense
            jcsproxy_storage_cost_nk[jcsproxy_area] = cost_nk_res
        return jcsproxy_storage_cost_nk


    def jcsproxy_storage_cost_value(self, jcsproxy_sotrage_cost_nk, optimizer_init):
        # 所有jcsproxy_area的storage_cost和
        storage_cost = jcsproxy_sotrage_cost_nk[optimizer_init.jcsproxy_area_list[0]]['storage_expense']
        for jcsproxy_area in optimizer_init.jcsproxy_area_list:
            storage_cost += jcsproxy_sotrage_cost_nk[jcsproxy_area]['download_expense']
            storage_cost += jcsproxy_sotrage_cost_nk[jcsproxy_area]['request_expense']
        return storage_cost







    ##########################################################################################








    def jcsproxy_placement_nk_remaining(self, placement, jcsproxy_placement_nk, jcsproxy_area_list):
        remaining_nk = []
        remaining_check = [0] * len(placement)
        for jcsproxy_area in jcsproxy_area_list:
            placement_nk = jcsproxy_placement_nk[jcsproxy_area]
            for placement_i in placement_nk:
                placement_index = placement.index(placement_i)
                remaining_check[placement_index] = 1
        for i in range(len(placement)):
            if remaining_check[i] == 0:
                remaining_nk.append(placement[i])
        return remaining_nk



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

    print ""
    placement_nk_operate = PlacementNkInterface()
    placement = [3,7,2,9,1]
    res = placement_nk_operate.get_placement_bucket_name_list(placement, optimizer_init.cloud_bucket_list)
    print res
    res = placement_nk_operate.get_placement_remaining(placement, len(optimizer_init.cloud_bucket_list))
    print res