# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/5/24 16:23'

from optimizer_init import OptimizerInit
from optimizer_placement import OptimizerPlacement
from optimizer_distance import OptimizerDistance
from replacement_latency_time_minmax import ReplacementLatencyTimeMinmax
from replacement_storage_cost_minmax import ReplacementStorageCostMinmax
from placement_nk_interface import PlacementNkInterface
import copy
from myprint import MyPrint
from config.cloud_information import CloudInformation

# 求解所有placement的情况
# 遍历效率比置换要差
# (5,3)的时候差20多倍
class OptimizerReplacement(object):
    def __init__(self):
        self.best_worst_node = None

    def get_best_worst_node(self, optimizer_init):
        best_worst_node = {}
        best_worst_latency_time = ReplacementLatencyTimeMinmax().replacement_latency_time_minmax(optimizer_init)
        best_worst_storage_cost = ReplacementStorageCostMinmax().replacement_storage_cost_minmax(optimizer_init)
        best_worst_node.update(best_worst_latency_time)
        best_worst_node.update(best_worst_storage_cost)
        self.best_worst_node = best_worst_node
        return best_worst_node

    ##############################################################################

    def optimizer_replacement2(self, optimizer_init):
        self.get_best_worst_node(optimizer_init)

        N = len(optimizer_init.cloud_bucket_list)
        n = optimizer_init.fault_tolerance_features['erasure_code_n']
        k = optimizer_init.fault_tolerance_features['erasure_code_k']

        placement = PlacementNkInterface().get_placement_random(N, n)
        res_placement_info = self.get_placement_min_info(placement, optimizer_init)

        placement_list = OptimizerPlacement().get_placement_list(N, n)
        print "len", len(placement_list)
        placement_info_list = []
        for placement_one in placement_list:
            placement_info = self.get_placement_min_info(placement_one['placement'], optimizer_init)
            # placement_info_list.append(placement_info)
            if res_placement_info['distance'] > placement_info['distance']:
                 res_placement_info = placement_info
        return placement_info_list, res_placement_info






    ##############################################################################################


    def get_placement_min_info(self, placement, optimizer_init):
        # 根据置换，求解当前placement下，的最小目标值
        N = len(optimizer_init.cloud_bucket_list)
        n = optimizer_init.fault_tolerance_features['erasure_code_n']
        k = optimizer_init.fault_tolerance_features['erasure_code_k']

        # latency最小的placement_nk
        jcsproxy_placement_nk= ReplacementLatencyTimeMinmax().\
            placement_latency_time_jcsproxy_placement_min_nk(placement, optimizer_init)
        placement_info = self.get_placement_info(placement, jcsproxy_placement_nk, optimizer_init)
        # 置换能否使 目标函数值最小
        replacement_res_list = self.get_replacement_info(placement_info, optimizer_init)
        placement_min_info = replacement_res_list[len(replacement_res_list)-1]

        # print "get_placement_min_info"
        # print replacement_res_list
        # print len(replacement_res_list)
        return placement_min_info

    def get_replacement_info(self, placement_info, optimizer_init):
        # 根据置换成本，求解当前placement下，的最小目标值
        new_placement_info = copy.deepcopy(placement_info)
        replacement_res_list = []
        replacement_res_list.append(new_placement_info)

        placement = new_placement_info['placement']
        jcsproxy_placement_nk = new_placement_info['jcsproxy_placement_nk']
        jcsproxy_placement_remaining_nk = self.get_jcsproxy_placement_remaining_nk(placement, jcsproxy_placement_nk)

        for jcsproxy_area in optimizer_init.jcsproxy_area_list:
            for placement_remaining_i in jcsproxy_placement_remaining_nk[jcsproxy_area]:

                cal_jcsproxy_placement_nk = copy.deepcopy(new_placement_info['jcsproxy_placement_nk'])
                for placement_nk_i in cal_jcsproxy_placement_nk[jcsproxy_area]:
                    placement_nk_index = cal_jcsproxy_placement_nk[jcsproxy_area].index(placement_nk_i)
                    cal_jcsproxy_placement_nk[jcsproxy_area][placement_nk_index] = placement_remaining_i  # 替换
                    cal_placement_info = self.get_placement_info(placement, cal_jcsproxy_placement_nk, optimizer_init)
                    if cal_placement_info['distance'] < new_placement_info['distance']:
                        replacement_res_list.append(cal_placement_info)
                        new_placement_info = copy.deepcopy(cal_placement_info)
                        break
                    cal_jcsproxy_placement_nk[jcsproxy_area][placement_nk_index] = placement_nk_i  # 返回替换之前的状态
        return replacement_res_list

    def get_placement_info(self, placement, jcsproxy_placement_nk, optimizer_init):
        # 根据placement，placement_nk，计算当前方案下的状态值
        placement_nk_operate = PlacementNkInterface()
        jcsproxy_latency_time = placement_nk_operate.jcsproxy_latency_time_nk(placement, jcsproxy_placement_nk, optimizer_init)
        jcsproxy_storage_cost = placement_nk_operate.jcsproxy_storage_cost_nk(placement, jcsproxy_placement_nk, optimizer_init)
        latency_time = placement_nk_operate.jcsproxy_latency_time_value(jcsproxy_latency_time, optimizer_init)
        storage_cost = placement_nk_operate.jcsproxy_storage_cost_value(jcsproxy_storage_cost, optimizer_init)
        distance = self.get_placement_distance(storage_cost, latency_time, optimizer_init.target_weights)

        jcsproxy_placement_nk_info = {}
        jcsproxy_placement_nk_info['placement'] = placement
        jcsproxy_placement_nk_info['jcsproxy_placement_nk'] = jcsproxy_placement_nk
        jcsproxy_placement_nk_info['jcsproxy_storage_cost'] = jcsproxy_storage_cost
        jcsproxy_placement_nk_info['jcsproxy_latency_time'] = jcsproxy_latency_time
        jcsproxy_placement_nk_info['storage_cost'] = storage_cost
        jcsproxy_placement_nk_info['latency_time'] = latency_time
        jcsproxy_placement_nk_info['distance'] = distance
        return jcsproxy_placement_nk_info


    def get_placement_distance(self, storage_cost, latency_time, target_weights):
        best_worst_node = self.best_worst_node
        if (best_worst_node['worst_storage_cost'] - best_worst_node['best_storage_cost']) == 0:
            storage_cost_distance = 0.0
        else:
            storage_cost_distance = (storage_cost - best_worst_node['best_storage_cost']) \
                                    / (best_worst_node['worst_storage_cost'] - best_worst_node['best_storage_cost'])
        storage_cost_distance = storage_cost_distance * target_weights['storage_cost_weight']
        latency_time_distance = (latency_time - best_worst_node['best_latency_time']) \
                                / (best_worst_node['worst_latency_time'] - best_worst_node['best_latency_time'])
        latency_time_distance = latency_time_distance * target_weights['latency_time_weight']
        # distance = math.sqrt(storage_cost_distance * storage_cost_distance +
        #                      latency_time_distance * latency_time_distance)
        distance = storage_cost_distance * storage_cost_distance + \
                   latency_time_distance * latency_time_distance
        return distance



    def get_jcsproxy_placement_remaining_nk(self, placement, jcsproxy_placement_nk):
        jcsproxy_placement_remaining_nk = {}
        for jcsproxy_area in jcsproxy_placement_nk:
            placement_nk = jcsproxy_placement_nk[jcsproxy_area]
            new_placement = copy.deepcopy(placement)
            for placement_i in placement_nk:
                new_placement.remove(placement_i)
            jcsproxy_placement_remaining_nk[jcsproxy_area] = new_placement
        return jcsproxy_placement_remaining_nk



    #################################################################################################





if __name__ == '__main__':
    # 输入参数
    jcsproxy_request_features = {
        'aliyun-beijing': 10,
        'aliyun-shanghai': 0,
        'aliyun-shenzhen': 10,
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

    print "optimizer replacement"
    optimizer_replacement = OptimizerReplacement()
    replacement_res_list, opt_result = optimizer_replacement.optimizer_replacement2(optimizer_init)

    print ""
    # print 'replacement_res_list', replacement_res_list
    print 'replacement_res_list len', len(replacement_res_list)

    print ""
    MyPrint().myprintdict(opt_result, 'opt_result')



