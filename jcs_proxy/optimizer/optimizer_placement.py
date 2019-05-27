# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/5/14 16:09'

from optimizer_init import OptimizerInit
import copy

class OptimizerPlacement(object):
    # 计算所有方案，及对应的成本和延迟
    def __init__(self):
        self.plan_nk_list = None
        self.plan_power_list = None

    def get_optimizer_placement(self, optimizer_init):
        # 遍历计算所有可能情况
        N = len(optimizer_init.cloud_bucket_list)
        n = optimizer_init.fault_tolerance_features['erasure_code_n']
        k = optimizer_init.fault_tolerance_features['erasure_code_k']
        plan_nk_list = self.get_combination_list(n, k)
        plan_power_list = self.get_power_list(len(plan_nk_list), len(optimizer_init.jcsproxy_area_list))
        self.plan_nk_list = plan_nk_list
        self.plan_power_list = plan_power_list

        placement_list = self.get_placement_list(N, n)
        placement_list = self.get_storage_cost_nk(placement_list, plan_nk_list, optimizer_init.jcsproxy_storage_cost_list)
        placement_list = self.get_latency_time_nk(placement_list, plan_nk_list, optimizer_init.jcsproxy_latency_time_list)

        placement_list = self.get_storage_cost_list(placement_list, plan_power_list, optimizer_init.jcsproxy_area_list)
        placement_list = self.get_latency_time_list(placement_list, plan_power_list, optimizer_init.jcsproxy_area_list,
                                                    optimizer_init.jcsproxy_request_features)


        # print ""
        # print "placement_list len", len(placement_list)
        # print "plan_nk_list len", len(plan_nk_list)
        # print "plan_lsit_power len", len(plan_power_list)


        # print_index = 0
        # print "print index", print_index
        # print "placement_list[] placement", placement_list[print_index]['placement']
        # print "placement_list[] storage_cost_nk", placement_list[print_index]['storage_cost_nk']
        # print "placement_list[] latency_time_nk", placement_list[print_index]['latency_time_nk']
        # print "placement_list[] storage_cost_list", placement_list[print_index]['storage_cost_list']
        # print "placement_list[] latency_time_list", placement_list[print_index]['latency_time_list']
        #
        # print_index = 253
        # print "print index", print_index
        # print "placement_list[] placement", placement_list[print_index]['placement']
        # print "placement_list[] storage_cost_nk", placement_list[print_index]['storage_cost_nk']
        # print "placement_list[] latency_time_nk", placement_list[print_index]['latency_time_nk']
        # print "placement_list[] storage_cost_list", placement_list[print_index]['storage_cost_list']
        # print "placement_list[] latency_time_list", placement_list[print_index]['latency_time_list']

        return placement_list

    ############################################################################################

    def cal_combination_list(self, combination_list, combination, start, level, N, n):
        if level == n:
            combination_list.append(copy.deepcopy(combination))
            return 0
        for i in range(start, N - (n - level) + 1):
            combination.append(i)
            self.cal_combination_list(combination_list, combination, i + 1, level + 1, N, n)
            combination.remove(i)

    def get_combination_list(self, cloud_bucket_len, erasure_code_n):
        combination_list = []
        combination = []
        self.cal_combination_list(combination_list, combination, 0, 0, cloud_bucket_len, erasure_code_n)
        return combination_list

    ##############################################################################################

    def get_placement_list(self, cloud_bucket_len, erasure_code_n):
        # 所有可能的placement情况
        combination_list = self.get_combination_list(cloud_bucket_len, erasure_code_n)
        placement_list = []
        for combination_one in combination_list:
            placement_info = {}
            placement_info['placement'] = combination_one
            placement_list.append(placement_info)
        return placement_list

    def get_storage_cost_nk(self, placement_list, plan_nk_list, jcsproxy_storage_cost):
        for placement_info in placement_list:
            placement_storage_cost_nk = self.get_placement_storage_cost_nk(placement_info['placement'],
                                                                           plan_nk_list, jcsproxy_storage_cost)
            placement_info['storage_cost_nk'] = placement_storage_cost_nk
        return placement_list

    def get_placement_storage_cost_nk(self, placement, plan_nk_list, jcsproxy_storage_cost):
        # 前k个，download和request成本
        # 前n个，sotrage成本
        placement_storage_cost_nk = {}
        for jcsproxy_area in jcsproxy_storage_cost:
            area_cost_nk = []
            storage_expense = 0
            for placement_i in placement:
                storage_expense += jcsproxy_storage_cost[jcsproxy_area][placement_i]['storage_expense']
            for plan in plan_nk_list:
                download_expense = 0
                request_expense = 0
                for plan_i in plan:
                    download_expense += jcsproxy_storage_cost[jcsproxy_area][placement[plan_i]]['download_expense']
                    request_expense += jcsproxy_storage_cost[jcsproxy_area][placement[plan_i]]['request_expense']

                plan_res = {}
                plan_res['storage_expense'] = storage_expense
                plan_res['download_expense'] = download_expense
                plan_res['request_expense'] = request_expense
                area_cost_nk.append(plan_res)
            placement_storage_cost_nk[jcsproxy_area] = area_cost_nk
        return placement_storage_cost_nk

    def get_latency_time_nk(self, placement_list, plan_nk_list, jcsproxy_latency_time):
        for placement_info in placement_list:
            placement_latency_time_nk = self.get_placement_latency_time_nk(placement_info['placement'],
                                                                           plan_nk_list, jcsproxy_latency_time)
            placement_info['latency_time_nk'] = placement_latency_time_nk
        return placement_list

    def get_placement_latency_time_nk(self, placement, plan_nk_list, jcsproxy_latency_time):
        # 前k个latency最大值
        placement_latency_time_nk = {}
        for jcsproxy_area in jcsproxy_latency_time:
            area_latency_nk = []
            for plan in plan_nk_list:
                max_latency = 0.0
                for plan_i in plan:
                    if max_latency <= jcsproxy_latency_time[jcsproxy_area][placement[plan_i]]['latency_time']:
                        max_latency = jcsproxy_latency_time[jcsproxy_area][placement[plan_i]]['latency_time']
                # latency_time = {}
                # latency_time['latency_time'] = max_latency
                area_latency_nk.append(max_latency)
            placement_latency_time_nk[jcsproxy_area] = area_latency_nk
        return placement_latency_time_nk

    ######################################################################################

    def get_power_list(self, plan_nk_list_len, jcsproxy_area_len):
        power_list = []
        power = []
        self.cal_power_list(power_list, power, 0, 0, plan_nk_list_len, jcsproxy_area_len)
        return power_list

    def cal_power_list(self, power_list, power, start, level, N, n):  # N^n种
        if level == n:
            power_list.append(copy.deepcopy(power))
            return 0
        for i in range(start, N):
            power.append(i)
            self.cal_combination_list(power_list, power, start, level + 1, N, n)
            power.remove(i)


    def get_storage_cost_list(self, placement_list, plan_power_list, jcsproxy_area_list):
        for placement_info in placement_list:
            placement_storage_cost_list = self.get_placement_storage_cost_list(plan_power_list,
                                                                    placement_info['storage_cost_nk'], jcsproxy_area_list)
            placement_info['storage_cost_list'] = placement_storage_cost_list
        return placement_list

    def get_placement_storage_cost_list(self, plan_power_list, storage_cost_nk, jcsproxy_area_list):
        # 几个jcsproxy，download和request成本相加，storage只加一次
        storage_cost_list = []
        for plan in plan_power_list:
            storage_cost = storage_cost_nk[jcsproxy_area_list[0]][0]['storage_expense']
            for i in range(len(plan)):
                jcsproxy_area = jcsproxy_area_list[i]
                plan_i = plan[i]
                storage_cost += storage_cost_nk[jcsproxy_area][plan_i]['download_expense'] + storage_cost_nk[jcsproxy_area][plan_i]['request_expense']
            storage_cost_list.append(storage_cost)
        return storage_cost_list

    def get_latency_time_list(self, placement_list, plan_power_list, jcsproxy_area_list, jcsproxy_request_features):
        jcsproxy_request_weights = {}
        sum_request = 0
        for jcsproxy_area in jcsproxy_area_list:   # 下载量权重
            sum_request += jcsproxy_request_features[jcsproxy_area]
        for jcsproxy_area in jcsproxy_area_list:
            jcsproxy_request_weights[jcsproxy_area] = jcsproxy_request_features[jcsproxy_area]/(float)(sum_request)

        for placement_info in placement_list:
            placement_latency_time_list = self.get_placement_latency_time_list(plan_power_list,
                                    placement_info['latency_time_nk'], jcsproxy_area_list, jcsproxy_request_weights)
            placement_info['latency_time_list'] = placement_latency_time_list
        return placement_list

    def get_placement_latency_time_list(self, plan_power_list, latency_time_nk, jcsproxy_area_list, jcsproxy_request_weights):
        # latency 按下载量权重值相加
        latency_time_list = []
        for plan in plan_power_list:
            latency_time = 0
            for i in range(len(plan)):
                jcsproxy_area = jcsproxy_area_list[i]
                plan_i = plan[i]
                latency_time += latency_time_nk[jcsproxy_area][plan_i]* jcsproxy_request_weights[jcsproxy_area]
            latency_time_list.append(latency_time)
        return latency_time_list




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

    optimizer_placement = OptimizerPlacement()
    optimizer_placement.get_optimizer_placement(optimizer_init)