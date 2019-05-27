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

# 求解一个placement中，距离best_worst_node最近的方案，采用遍历，
# 纠删码参数以及jcsproxy个数会影响效率，
# 但(5,3)，2个proxy影响很少
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

    def optimizer_replacement(self, optimizer_init):
        # 获取最后结果
        self.get_best_worst_node(optimizer_init)
        N = len(optimizer_init.cloud_bucket_list)
        n = optimizer_init.fault_tolerance_features['erasure_code_n']
        placement = PlacementNkInterface().get_placement_random(N, n)
        placement_info = self.get_placement_min_info(placement, optimizer_init)
        replacement_res_list = self.replacement_placement(placement_info, optimizer_init)  # 置换节点，求解最优

        opt_result = replacement_res_list[len(replacement_res_list)-1]
        opt_result['jcsproxy_storage_features'] = optimizer_init.jcsproxy_storage_features
        opt_result['fault_tolerance_features'] = optimizer_init.fault_tolerance_features
        opt_result['target_weights'] = optimizer_init.target_weights
        placement_bucket_name_list = self.get_placement_bucket_name_list(opt_result['placement'], optimizer_init.cloud_bucket_list)
        jcsproxy_placement_nk_bucket_name_list = self.get_jcsproxy_placement_nk_bucket_name_list(opt_result['jcsproxy_placement_nk'], optimizer_init.cloud_bucket_list)
        opt_result['bucket_name_list'] = placement_bucket_name_list
        opt_result['jcsproxy_bucket_name_list'] = jcsproxy_placement_nk_bucket_name_list

        # print ""
        # print 'replacement_res_list', replacement_res_list
        # print 'replacement_res_list len', len(replacement_res_list)

        # print ""
        # MyPrint().myprintdict(opt_result, 'opt_result')

        return replacement_res_list, opt_result

    def get_placement_bucket_name_list(self, placement, cloud_bucket_list):
        # 根据placement，输出bucket名
        bucket_name_list = []
        for bucket_index in placement:
            bucket_name = cloud_bucket_list[bucket_index]['bucket_name']
            bucket_name_list.append(bucket_name)
        return bucket_name_list

    def get_jcsproxy_placement_nk_bucket_name_list(self, jcsproxy_placement_nk, cloud_bucket_list):
        jcsproxy_placement_nk_bucket_name_list = {}
        for jcsproxy_area in jcsproxy_placement_nk:
            placement_nk = jcsproxy_placement_nk[jcsproxy_area]
            placement_nk_bucket_name_list = self.get_placement_bucket_name_list(placement_nk, cloud_bucket_list)
            jcsproxy_placement_nk_bucket_name_list[jcsproxy_area] = placement_nk_bucket_name_list
        return jcsproxy_placement_nk_bucket_name_list




    ##############################################################################################


    def get_placement_min_info(self, placement,optimizer_init):
        # 计算此个placement的所有可能情况的最小值
        N = len(optimizer_init.cloud_bucket_list)
        n = optimizer_init.fault_tolerance_features['erasure_code_n']
        k = optimizer_init.fault_tolerance_features['erasure_code_k']
        best_worst_node = self.best_worst_node

        optimizer_placement = OptimizerPlacement()
        plan_nk_list = optimizer_placement.get_combination_list(n, k)
        plan_power_list = optimizer_placement.get_power_list(len(plan_nk_list), len(optimizer_init.jcsproxy_area_list))
        placement_storage_cost_nk = optimizer_placement.get_placement_storage_cost_nk(
            placement, plan_nk_list, optimizer_init.jcsproxy_storage_cost_list)
        placement_latency_time_nk = optimizer_placement.get_placement_latency_time_nk(
            placement, plan_nk_list, optimizer_init.jcsproxy_latency_time_list)
        # storage_cost
        placement_storage_cost_power = optimizer_placement.get_placement_storage_cost_list(
            plan_power_list, placement_storage_cost_nk, optimizer_init.jcsproxy_area_list)
        # latency_time
        placement_latency_time_power = optimizer_placement.get_placement_latency_time_list(
            plan_power_list, placement_latency_time_nk, optimizer_init.jcsproxy_area_list, optimizer_init.jcsproxy_request_weights)
        optimizer_distance = OptimizerDistance()
        # distance
        placement_distance_power = optimizer_distance.get_placement_distance_list(
            placement_storage_cost_power, placement_latency_time_power, best_worst_node,optimizer_init.target_weights)

        min_distance_value = min(placement_distance_power)
        min_distance_index = placement_distance_power.index(min_distance_value)
        jcsproxy_placement_nk = optimizer_distance.get_jcsproxy_placement_nk_from_power(
            placement, min_distance_index, optimizer_init.jcsproxy_area_list, plan_nk_list, plan_power_list)

        replacement_min = {}
        replacement_min['placement'] = placement
        replacement_min['jcsproxy_placement_nk'] = jcsproxy_placement_nk
        replacement_min['storage_cost'] = placement_storage_cost_power[min_distance_index]
        replacement_min['latency_time'] = placement_latency_time_power[min_distance_index]
        replacement_min['distance'] = min_distance_value
        replacement_min.update(optimizer_distance.get_jcsproxy_placement_nk_info(placement, jcsproxy_placement_nk, optimizer_init))
        return replacement_min


    # def get_placement_min_info(self, placement, optimizer_init):
    #     # 根据置换，求解当前placement下，的最小目标值
    #     N = len(optimizer_init.cloud_bucket_list)
    #     n = optimizer_init.fault_tolerance_features['erasure_code_n']
    #     k = optimizer_init.fault_tolerance_features['erasure_code_k']
    #
    #     # latency最小的placement_nk
    #     jcsproxy_placement_nk= ReplacementLatencyTimeMinmax().\
    #         placement_latency_time_jcsproxy_placement_min_nk(placement, optimizer_init)
    #     placement_info = self.get_placement_info(placement, jcsproxy_placement_nk, optimizer_init)
    #     # 置换能否使 目标函数值最小
    #     replacement_res_list = self.get_replacement_info(placement_info, optimizer_init)
    #     placement_min_info = replacement_res_list[len(replacement_res_list)-1]
    #
    #     # print "get_placement_min_info"
    #     # print replacement_res_list
    #     # print len(replacement_res_list)
    #     return placement_min_info

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

    # 替换节点，找最优值 （结果不一定是全局最优值）
    # 替换规则，（或先latency再cost）
    #   先cost替换，使目标值更小
    #   再latency替换，使目标值更小
    # 需要多次迭代

    # 考虑置换哪个节点
    # a.置换一个节点的所有情况，剩余N-n个节点分别置换n个节点，选使目标函数最小的，复杂度 n*(N-n)  *迭代次数
    # b.启发式置换，每次选剩余N-n个节点的其中一个来 分别置换n个节点，选使目标海曙最小的，复杂度  a * n  *迭代次数
    # 先按b，效率高，最后按a检查

    def replacement_placement(self, placement_info, optimizer_init):
        # iter_num = 3  # 默认迭代次数
        replacement_res_list = []
        replacement_res_list.append(placement_info)
        new_min_info = placement_info
        # for i in range(iter_num):
            # print "替换节点求最优，迭代次数", i
            # old_min_info = copy.deepcopy(new_min_info)
            # replacement_res_list += self.replacement_storage_cost(new_min_info, optimizer_init)
            # new_min_info = replacement_res_list[len(replacement_res_list)-1]
            # replacement_res_list += self.replacement_latency_time(new_min_info, optimizer_init)
            # new_min_info = replacement_res_list[len(replacement_res_list) - 1]
            # if old_min_info['distance'] - new_min_info['distance'] < 0.00000001:
            #     break

        # replacement_res_list += self.replacement_latency_time(new_min_info, optimizer_init)
        # print "latency time, replacement_res_list len", len(replacement_res_list)
        # new_min_info = replacement_res_list[len(replacement_res_list) - 1]
        #
        # replacement_res_list += self.replacement_storage_cost(new_min_info, optimizer_init)
        # print "storage cost, replacement_res_list len", len(replacement_res_list)
        # new_min_info = replacement_res_list[len(replacement_res_list)-1]


        replacement_res_list += self.replacement_neighbor_placement(new_min_info, optimizer_init)
        print "neighbor placement, replacement_res_list len", len(replacement_res_list)
        return replacement_res_list


    def replacement_neighbor_placement(self, placement_info, optimizer_init):
        # 多次替换，直到下一次替换和当前值相同，说明找到（局部）最优
        replacement_res_list = []
        while True:
            new_placement_info = self.replacement_neighbor_node(placement_info, optimizer_init)
            if placement_info['distance'] - new_placement_info['distance'] < 0.00000001:
                break
            replacement_res_list.append(new_placement_info)
            placement_info = copy.deepcopy(new_placement_info)
        return replacement_res_list

    def replacement_neighbor_node(self, placement_info, optimizer_init):
        # 替换此方案下，任意替换一个云地域的邻近方案，使目标函数最小
        # 一次替换
        N = len(optimizer_init.cloud_bucket_list)
        new_placement_storage_cost = copy.deepcopy(placement_info)
        for placement_remaining_i in range(N):
            if placement_remaining_i in placement_info['placement']:
                continue

            cal_placement = placement_info['placement']
            for placement_i in cal_placement:
                placement_index = cal_placement.index(placement_i)
                cal_placement[placement_index] = placement_remaining_i  # 替换

                cal_placement_storage_cost = self.get_placement_min_info(cal_placement, optimizer_init)
                if cal_placement_storage_cost['distance'] < new_placement_storage_cost['distance']:
                    new_placement_storage_cost = copy.deepcopy(cal_placement_storage_cost)
                cal_placement[placement_index] = placement_i
        return new_placement_storage_cost

    # def replacement_neighbor_node(self, placement_info, optimizer_init):
    #     # 替换此方案下，任意替换一个云地域的邻近方案，使目标函数最小
    #     # 一次替换
    #     N = len(optimizer_init.cloud_bucket_list)
    #     new_placement_storage_cost = copy.deepcopy(placement_info)
    #     for placement_remaining_i in range(N):
    #         if placement_remaining_i in new_placement_storage_cost['placement']:
    #             continue
    #
    #         cal_placement = copy.deepcopy(new_placement_storage_cost['placement'])
    #         for placement_i in cal_placement:
    #             placement_index = cal_placement.index(placement_i)
    #             cal_placement[placement_index] = placement_remaining_i  # 替换
    #
    #             cal_placement_storage_cost = self.get_placement_min_info(cal_placement, optimizer_init)
    #             if cal_placement_storage_cost['distance'] < new_placement_storage_cost['distance']:
    #                 new_placement_storage_cost = copy.deepcopy(cal_placement_storage_cost)
    #             cal_placement[placement_index] = placement_i
    #     return new_placement_storage_cost



    def replacement_storage_cost(self, placement_info, optimizer_init):
        # 根据成本，替换节点
        N = len(optimizer_init.cloud_bucket_list)
        new_placement_storage_cost = copy.deepcopy(placement_info)
        replacement_res_list = []

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
                        cal_placement_storage_cost = self.get_placement_min_info(cal_placement, optimizer_init)
                        if cal_placement_storage_cost['distance'] < new_placement_storage_cost['distance']:
                            replacement_res_list.append(cal_placement_storage_cost)
                            new_placement_storage_cost = copy.deepcopy(cal_placement_storage_cost)
                            break
                        cal_placement[placement_index] = placement_i  # 返回替换之前的状态
        return replacement_res_list

    def replacement_latency_time(self, placement_info, optimizer_init):
        # 替换初始方案中的节点，找最小延迟
        # 替换规格，按latency的权值和 从大到小，不是替换效益最大的节点(效果不好)
        # 替换规则，按latency的权值和 从小到大，替换效益最大的节点
        N = len(optimizer_init.cloud_bucket_list)
        new_placement_latency_time = copy.deepcopy(placement_info)
        replacement_res_list = []

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
                cal_placement_latency_time = self.get_placement_min_info(cal_placement, optimizer_init)
                if cal_placement_latency_time['distance'] < new_placement_latency_time['distance']:
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
        'aliyun-beijing': 10,
        'aliyun-shanghai': 0,
        'aliyun-shenzhen': 10,
    }
    file_size = 1024
    storage_time = 1

    fault_tolerance_features = {  # 容错特性
        'fault_tolerance_level': 3,
        'erasure_code_k': 4,
        'erasure_code_n': 7,  # erasure_code_n = erasure_code_k + fault_tolerance_level
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
    replacement_res_list, opt_result = optimizer_replacement.optimizer_replacement(optimizer_init)

    print ""
    print 'replacement_res_list', replacement_res_list
    print 'replacement_res_list len', len(replacement_res_list)

    print ""
    MyPrint().myprintdict(opt_result, 'opt_result')



