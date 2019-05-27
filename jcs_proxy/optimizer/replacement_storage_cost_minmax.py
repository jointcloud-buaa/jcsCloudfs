# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/5/17 17:43'

from optimizer_init import OptimizerInit
import copy
from placement_nk_interface import PlacementNkInterface
from myprint import MyPrint

class ReplacementStorageCostMinmax(object):
    def __init__(self):
        pass

    def replacement_test(self, optimizer_init):
        # 测试结果
        loop_num = 10
        test_list = []
        for i in range(loop_num):
            test_one = self.replacement_storage_cost_minmax(optimizer_init)
            test_list.append(test_one)
        # MyPrint().myprintlist(test_list, "test list:")

    ########################################################################################

    def replacement_storage_cost_minmax(self, optimizer_init):
        replacement_storage_cost_min_list, replacement_storage_cost_max_list = self.replacement_storage_cost_minmax_list(optimizer_init)
        storage_cost_min_info = replacement_storage_cost_min_list[len(replacement_storage_cost_min_list)-1]
        storage_cost_max_info = replacement_storage_cost_max_list[len(replacement_storage_cost_max_list)-1]
        minmax_res = {}
        minmax_res['best_storage_cost'] = storage_cost_min_info['storage_cost_min']
        minmax_res['worst_storage_cost'] = storage_cost_max_info['storage_cost_max']
        # print minmax_res
        return minmax_res


    def replacement_storage_cost_minmax_list(self, optimizer_init):
        N = len(optimizer_init.cloud_bucket_list)
        n = optimizer_init.fault_tolerance_features['erasure_code_n']
        placement = PlacementNkInterface().get_placement_random(N, n)
        placement_storage_cost = self.placement_storage_cost(placement, optimizer_init)
        replacement_storage_cost_min_list = self.replacement_placement_storage_cost_min(placement_storage_cost, optimizer_init)
        replacement_storage_cost_max_list = self.replacement_placement_storage_cost_max(placement_storage_cost, optimizer_init)

        # print "replacement_storage_cost_min_list", replacement_storage_cost_min_list
        # print "replacement_storage_cost_min_list len", len(replacement_storage_cost_min_list)

        # print "replacement_storage_cost_max_list", replacement_storage_cost_max_list
        # print "replacement_storage_cost_max_list len", len(replacement_storage_cost_max_list)
        return replacement_storage_cost_min_list, replacement_storage_cost_max_list


    ##########################################################################################


    def placement_storage_cost(self, placement, optimizer_init):
        # 计算placement_storage_cost的属性值
        placement_nk_operate = PlacementNkInterface()
        placement_storage_cost = {}
        placement_storage_cost['placement'] = placement
        placement_storage_cost['jcsproxy_placement_min_nk'] = self.placement_storage_cost_jcsproxy_placement_min_nk(
            placement_storage_cost['placement'], optimizer_init)
        jcsproxy_storage_cost_min_nk = placement_nk_operate.jcsproxy_storage_cost_nk(
            placement_storage_cost['placement'], placement_storage_cost['jcsproxy_placement_min_nk'], optimizer_init)
        placement_storage_cost['storage_cost_min'] = placement_nk_operate.jcsproxy_storage_cost_value(
            jcsproxy_storage_cost_min_nk, optimizer_init)

        placement_storage_cost['jcsproxy_placement_max_nk'] = self.placement_storage_cost_jcsproxy_placement_max_nk(
            placement_storage_cost['placement'], optimizer_init)
        jcsproxy_storage_cost_max_nk = placement_nk_operate.jcsproxy_storage_cost_nk(
            placement_storage_cost['placement'], placement_storage_cost['jcsproxy_placement_max_nk'], optimizer_init)
        placement_storage_cost['storage_cost_max'] = placement_nk_operate.jcsproxy_storage_cost_value(
            jcsproxy_storage_cost_max_nk, optimizer_init)

        # 与cost对应的latency值（为了画图）
        jcsproxy_latency_time_min_nk = placement_nk_operate.jcsproxy_latency_time_nk(
            placement, placement_storage_cost['jcsproxy_placement_min_nk'], optimizer_init)    ############
        placement_storage_cost['latency_time_min'] = placement_nk_operate.jcsproxy_latency_time_value(
            jcsproxy_latency_time_min_nk, optimizer_init)
        jcsproxy_latency_time_max_nk = placement_nk_operate.jcsproxy_latency_time_nk(
            placement, placement_storage_cost['jcsproxy_placement_max_nk'], optimizer_init)
        placement_storage_cost['latency_time_max'] = placement_nk_operate.jcsproxy_latency_time_value(
            jcsproxy_latency_time_max_nk, optimizer_init)
        return placement_storage_cost


    def placement_storage_cost_jcsproxy_placement_min_nk(self, placement, optimizer_init):
        # 每个jcsproxy_area选择storage_cost最小的k个节点下载
        jcsproxy_placement_min_nk = {}
        for jcsproxy_area in optimizer_init.jcsproxy_area_list:
            area_list = optimizer_init.jcsproxy_storage_cost_list[jcsproxy_area]
            placement_min_nk = []
            new_placement = copy.deepcopy(placement)
            for i in range(optimizer_init.fault_tolerance_features['erasure_code_k']):
                # n中前k个最小值,storage_expense相同，按照download_expense
                min_nk_expense = 100000000
                min_nk_i = -1
                for placement_i in new_placement:
                    if area_list[placement_i]['download_expense'] < min_nk_expense:
                        min_nk_expense = area_list[placement_i]['download_expense']
                        min_nk_i = placement_i
                new_placement.remove(min_nk_i)
                placement_min_nk.append(min_nk_i)
            jcsproxy_placement_min_nk[jcsproxy_area] = placement_min_nk
        return jcsproxy_placement_min_nk

    def placement_storage_cost_jcsproxy_placement_max_nk(self, placement, optimizer_init):
        # 每个jcsproxy_area选择storage_cost最大的k个节点下载
        jcsproxy_placement_min_nk = {}
        for jcsproxy_area in optimizer_init.jcsproxy_area_list:
            area_list = optimizer_init.jcsproxy_storage_cost_list[jcsproxy_area]
            placement_min_nk = []
            new_placement = copy.deepcopy(placement)
            for i in range(optimizer_init.fault_tolerance_features['erasure_code_k']):
                # n中前k个最小值,storage_expense相同，按照download_expense
                max_nk_expense = -1
                max_nk_i = -1
                for placement_i in new_placement:
                    if area_list[placement_i]['download_expense'] > max_nk_expense:
                        max_nk_expense = area_list[placement_i]['download_expense']
                        max_nk_i = placement_i
                new_placement.remove(max_nk_i)
                placement_min_nk.append(max_nk_i)
            jcsproxy_placement_min_nk[jcsproxy_area] = placement_min_nk
        return jcsproxy_placement_min_nk


    ##################################################################################################

    def replacement_placement_storage_cost_min(self, placement_storage_cost, optimizer_init):
        # 替换初始方案中的节点，找最小成本
        # 替换规则，从剩下 节点中替换
        N = len(optimizer_init.cloud_bucket_list)
        new_placement_storage_cost = copy.deepcopy(placement_storage_cost)
        replacement_res_list = []
        replacement_res_list.append(new_placement_storage_cost)

        storage_features_list = ['storage_expense', 'download_expense']
        for jcsproxy_area in optimizer_init.jcsproxy_area_list:
            for storage_features in storage_features_list:
                area_sort = optimizer_init.jcsproxy_storage_cost_sort[jcsproxy_area][storage_features]
                for i in range(N):
                    storage_cost_info = area_sort[N-1-i]
                    placement_remaining_i = storage_cost_info["cloud_bucket_index"]
                    if placement_remaining_i in new_placement_storage_cost['placement']:
                        continue

                    cal_placement = copy.deepcopy(new_placement_storage_cost['placement'])
                    for placement_i in cal_placement:
                        placement_index = cal_placement.index(placement_i)
                        cal_placement[placement_index] = placement_remaining_i  # 替换
                        cal_placement_storage_cost = self.placement_storage_cost(cal_placement, optimizer_init)
                        if cal_placement_storage_cost['storage_cost_min'] < new_placement_storage_cost['storage_cost_min']:
                            replacement_res_list.append(cal_placement_storage_cost)
                            new_placement_storage_cost = copy.deepcopy(cal_placement_storage_cost)
                            break
                        cal_placement[placement_index] = placement_i  # 返回替换之前的状态
        return replacement_res_list

    def replacement_placement_storage_cost_max(self, placement_storage_cost, optimizer_init):
        # 替换初始方案中的节点，找最小成本
        # 替换规则，从剩下 节点中替换
        N = len(optimizer_init.cloud_bucket_list)
        new_placement_storage_cost = copy.deepcopy(placement_storage_cost)
        replacement_res_list = []
        replacement_res_list.append(new_placement_storage_cost)

        storage_features_list = ['storage_expense', 'download_expense']
        for jcsproxy_area in optimizer_init.jcsproxy_area_list:
            for storage_features in storage_features_list:
                area_sort = optimizer_init.jcsproxy_storage_cost_sort[jcsproxy_area][storage_features]
                for i in range(N):
                    storage_cost_info = area_sort[N - 1 - i]
                    placement_remaining_i = storage_cost_info["cloud_bucket_index"]
                    if placement_remaining_i in new_placement_storage_cost['placement']:
                        continue

                    cal_placement = copy.deepcopy(new_placement_storage_cost['placement'])
                    for placement_i in cal_placement:
                        placement_index = cal_placement.index(placement_i)
                        cal_placement[placement_index] = placement_remaining_i  # 替换
                        cal_placement_storage_cost = self.placement_storage_cost(cal_placement, optimizer_init)
                        if cal_placement_storage_cost['storage_cost_max'] > new_placement_storage_cost['storage_cost_max']:
                            replacement_res_list.append(cal_placement_storage_cost)
                            new_placement_storage_cost = copy.deepcopy(cal_placement_storage_cost)
                            break
                        cal_placement[placement_index] = placement_i  # 返回替换之前的状态
        return replacement_res_list






if __name__ == '__main__':
    # 输入参数
    jcsproxy_request_features = {
        'aliyun-beijing': 3,
        'aliyun-shanghai': 0,
        'aliyun-shenzhen': 0,
    }
    file_size = 1024
    storage_time = 1

    fault_tolerance_features = {  # 容错特性
        'fault_tolerance_level': 2,
        'erasure_code_k': 3,
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

    replacement_storage_cost_minmax = ReplacementStorageCostMinmax()
    replacement_storage_cost_minmax.replacement_storage_cost_minmax_list(optimizer_init)
    replacement_storage_cost_minmax.replacement_storage_cost_minmax(optimizer_init)
    replacement_storage_cost_minmax.replacement_test(optimizer_init)
