# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/5/16 20:10'

from optimizer_init import OptimizerInit
import copy
from placement_nk_interface import PlacementNkInterface
from myprint import MyPrint

class ReplacementLatencyTimeMinmax(object):
    def __init__(self):
        pass

    def replacement_test(self, optimizer_init):
        # 测试结果
        loop_num = 1000
        test_list = []
        for i in range(loop_num):
            test_one = self.replacement_latency_time_minmax(optimizer_init, False)
            test_list.append(test_one['best_latency_time'])
        # MyPrint().myprintlist(test_list, "test list:")
        min_latency_time = min(test_list)
        wrong_num = 0
        for one in test_list:
            if one - min_latency_time > 0.0000001:
                wrong_num += 1
                print one
        print wrong_num
        print min_latency_time

    ########################################################################################

    def replacement_latency_time_minmax(self, optimizer_init, is_random_placement=False):
        # 最小最大值结果
        replacement_latency_time_minmax_list = self.replacement_latency_time_minmax_list(optimizer_init, is_random_placement)
        latency_time_minmax_info = replacement_latency_time_minmax_list[len(replacement_latency_time_minmax_list)-1]
        minmax_res = {}
        minmax_res['best_latency_time'] = latency_time_minmax_info['latency_time_min']
        minmax_res['worst_latency_time'] = latency_time_minmax_info['latency_time_max']
        # print minmax_res
        return minmax_res

    def replacement_latency_time_minmax_list(self, optimizer_init, is_random_placement=False):
        # 替换节点过程，寻找最小最大值
        N = len(optimizer_init.cloud_bucket_list)
        n = optimizer_init.fault_tolerance_features['erasure_code_n']
        # placement = [4, 2, 9, 17, 5]
        if is_random_placement == True:
            placement = PlacementNkInterface().get_placement_random(N, n)
        else:
            jcsproxy_latency_time_weights_sum_sort = optimizer_init.jcsproxy_latency_time_weights_sum_sort
            placement = []
            for i in range(n):
                placement.append(jcsproxy_latency_time_weights_sum_sort[i]['cloud_bucket_index'])  # 取最小的latency_time开始

        placement_latency_time = self.placement_latency_time(placement, optimizer_init)
        replacement_latency_time_minmax_list = self.replacement_placement_latency_time(placement_latency_time, optimizer_init)  # 替换节点，寻找最优延迟

        # print 'replacement_latency_time_minmax_list', replacement_latency_time_minmax_list
        # print 'replacement_latency_time_minmax_list len', len(replacement_latency_time_minmax_list)
        return replacement_latency_time_minmax_list


    ############################################################################################

    def placement_latency_time(self, placement, optimizer_init):
        # 计算placement_latency_time的属性值
        placement_nk_operate = PlacementNkInterface()
        placement_latency_time = {}
        placement_latency_time['placement'] = placement
        placement_latency_time['jcsproxy_placement_min_nk'] = self.placement_latency_time_jcsproxy_placement_min_nk(
            placement, optimizer_init)
        jcsproxy_latency_time_min_nk = placement_nk_operate.jcsproxy_latency_time_nk(
            placement, placement_latency_time['jcsproxy_placement_min_nk'], optimizer_init)   ########
        placement_latency_time['latency_time_min'] = placement_nk_operate.jcsproxy_latency_time_value(
            jcsproxy_latency_time_min_nk, optimizer_init)
        placement_latency_time['latency_time_max'] = self.placement_latency_time_max(optimizer_init)

        # 与latency对应的cost值（为了画图）
        jcsproxy_storage_cost_min_nk = placement_nk_operate.jcsproxy_storage_cost_nk(
            placement_latency_time['placement'], placement_latency_time['jcsproxy_placement_min_nk'], optimizer_init)
        placement_latency_time['storage_cost_min'] = placement_nk_operate.jcsproxy_storage_cost_value(
            jcsproxy_storage_cost_min_nk, optimizer_init)
        placement_latency_time['storage_cost_max'] = placement_latency_time['storage_cost_min']

        return placement_latency_time


    def placement_latency_time_jcsproxy_placement_min_nk(self, placement, optimizer_init):
        # 每个jcsproxy_area选择latency_time最小的k个节点下载
        jcsproxy_placement_min_nk = {}
        for jcsproxy_area in optimizer_init.jcsproxy_area_list:
            area_list = optimizer_init.jcsproxy_latency_time_list[jcsproxy_area]
            placement_min_nk = []
            new_placement = copy.deepcopy(placement)
            for i in range(optimizer_init.fault_tolerance_features['erasure_code_k']):
                # n中前k个最小值
                min_nk_value = 100000000
                min_nk_i = -1
                for placement_i in new_placement:
                    if area_list[placement_i]['latency_time'] < min_nk_value:
                        min_nk_value = area_list[placement_i]['latency_time']
                        min_nk_i = placement_i
                new_placement.remove(min_nk_i)
                placement_min_nk.append(min_nk_i)
            jcsproxy_placement_min_nk[jcsproxy_area] = placement_min_nk
        return jcsproxy_placement_min_nk


    def placement_latency_time_max(self, optimizer_init):
        # 计算latency_time的最大值
        N = len(optimizer_init.cloud_bucket_list)
        latency_time_max = 0.0
        for jcsproxy_area in optimizer_init.jcsproxy_area_list:
            latency_time_max += optimizer_init.jcsproxy_latency_time_sort[jcsproxy_area][N-1]['latency_time'] * \
                                 optimizer_init.jcsproxy_request_weights[jcsproxy_area]
        return latency_time_max

    ##############################################################################################

    def replacement_placement_latency_time(self, placement_latency_time, optimizer_init):
        # 替换初始方案中的节点，找最小延迟
        # 替换规格，按latency的权值和 从大到小，不是替换效益最大的节点(效果不好)
        # 替换规则，按latency的权值和 从小到大，替换效益最大的节点
        N = len(optimizer_init.cloud_bucket_list)
        new_placement_latency_time = copy.deepcopy(placement_latency_time)
        replacement_res_list = []
        replacement_res_list.append(new_placement_latency_time)

        for i in range(N):
            # latency_time_weights_sum_info = optimizer_init.jcsproxy_latency_time_weights_sum_sort[N-1-i]
            latency_time_weights_sum_info = optimizer_init.jcsproxy_latency_time_weights_sum_sort[i]
            placement_remaining_i = latency_time_weights_sum_info['cloud_bucket_index']
            if placement_remaining_i in new_placement_latency_time['placement']:  # 替换new_placement中不存在的
                continue

            cal_placement = copy.deepcopy(new_placement_latency_time['placement'])
            judge = False
            for placement_i in cal_placement:
                placement_index = cal_placement.index(placement_i)
                cal_placement[placement_index] = placement_remaining_i  # 替换
                cal_placement_latency_time = self.placement_latency_time(cal_placement, optimizer_init)
                if cal_placement_latency_time['latency_time_min'] < new_placement_latency_time['latency_time_min']:
                    # replacement_res_list.append(cal_placement_latency_time)
                    new_placement_latency_time = copy.deepcopy(cal_placement_latency_time)
                    judge = True
                    # break
                cal_placement[placement_index] = placement_i  # 返回替换之前的状态
            if judge == True:
                replacement_res_list.append(new_placement_latency_time)
        return replacement_res_list



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

    replacement_latency_time_minmax = ReplacementLatencyTimeMinmax()
    # replacement_latency_time_minmax.replacement_latency_time_minmax_list(optimizer_init)
    # replacement_latency_time_minmax.replacement_latency_time_minmax(optimizer_init)

    # for i in range(10):
    replacement_latency_time_minmax.replacement_test(optimizer_init)


