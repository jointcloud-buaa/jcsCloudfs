# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/5/24 18:30'

from config.cloud_information import CloudInformation
from myprint import MyPrint
from optimizer_init import OptimizerInit
from optimizer_distance import OptimizerDistance
from optimizer_replacement import OptimizerReplacement
from tools.get_func_time import GetFuncTime
from optimizer import Optimizer

class OptimizerAvailability(object):
    # 满足可用性条件的最优结果，即纠删码参数可变
    def __init__(self):
        pass

    def optimizer_availability(self):
        # 计算多种纠删码参数结果，再取最优

        # 参数
        file_size = 128
        storage_time = 1
        jcsproxy_request_features = {
            'aliyun-beijing': 0,
            'aliyun-shanghai': 0,
            'aliyun-shenzhen': 10,
        }
        target_weights = {}  # 优化目标权重
        target_weights['storage_cost_weight'] = 0.5
        target_weights['latency_time_weight'] = 1 - target_weights['storage_cost_weight']

        # 所有可能纠删码配置参数
        fault_tolerance_features_list = self.get_fault_tolerance_features_list()

        # 计算最优结果
        opt_result_list = []
        best_worst_node_list = []
        func_time_list = []
        for fault_tolerance_features in fault_tolerance_features_list:
            print '\n 正在执行，fault_tolerance_features', fault_tolerance_features
            optimizer_init = OptimizerInit(file_size, storage_time, jcsproxy_request_features,
                                       fault_tolerance_features, target_weights)

            # optimizer_distance = OptimizerDistance()
            # placement_list, opt_result = optimizer_distance.optimzer_distance(optimizer_init)
            # best_worst_node = optimizer_distance.get_best_worst_node(placement_list)
            # 遍历算法，时间测试
            # opt_result, best_worst_node, func_time = self.traversal_cal(optimizer_init)

            # optimizer_replacement = OptimizerReplacement()
            # replacement_res_list, opt_result = optimizer_replacement.optimizer_replacement(optimizer_init)
            # best_worst_node = optimizer_replacement.best_worst_node
            # 启发式算法，时间测试
            opt_result, best_worst_node, func_time = self.replacement_cal(optimizer_init)

            opt_result_list.append(opt_result)
            best_worst_node_list.append(best_worst_node)
            func_time_list.append(func_time)

        print "\n 相关信息"
        print "cloud bucket list len:", len(CloudInformation().get_cloud_bucket_list())
        MyPrint().myprintlist(fault_tolerance_features_list, 'fault_tolerance_features_list')
        print "\n 时间开销"
        MyPrint().myprintlist(func_time_list, 'func_time_list')
        print "sum func time:", sum(func_time_list)
        # 纠删码参数可变的最终结果
        self.get_optimizer_result(opt_result_list, best_worst_node_list, target_weights)



    def traversal_cal(self, optimizer_init):
        optimizer_distance = OptimizerDistance()
        # placement_list, opt_result = optimizer_distance.optimzer_distance(optimizer_init)
        res, func_time = GetFuncTime().get_func_time(optimizer_distance.optimzer_distance, (optimizer_init, ))
        placement_list = res[0]
        best_worst_node = optimizer_distance.get_best_worst_node(placement_list)
        opt_result = res[1]
        return opt_result, best_worst_node, func_time

    def replacement_cal(self, optimizer_init):
        # optimizer_replacement = OptimizerReplacement()
        # replacement_res_list, opt_result = optimizer_replacement.optimizer_replacement(optimizer_init)
        # res, func_time = GetFuncTime().get_func_time(optimizer_replacement.optimizer_replacement, (optimizer_init, ))
        res, func_time = GetFuncTime().get_func_time(Optimizer().get_optimizer_placement, (optimizer_init,))
        best_worst_node = Optimizer().get_best_worst_node(optimizer_init)
        # replacement_res_list = res[0]
        # opt_result = res[1]
        opt_result = res
        return opt_result, best_worst_node, func_time



    def get_optimizer_result(self, opt_result_list, best_worst_node_list, target_weights):
        # 计算不同纠删码参数下的最小值
        opt_result_storage_cost_list = []
        opt_result_latency_time_list = []
        for opt_result in opt_result_list:
            opt_result_storage_cost_list.append(opt_result['storage_cost'])
            opt_result_latency_time_list.append(opt_result['latency_time'])

        min_latency_time_list = []
        min_storage_cost_list = []
        max_latency_time_list = []
        max_storage_cost_list = []
        for best_worst_node in best_worst_node_list:
            min_latency_time_list.append(best_worst_node['best_latency_time'])
            min_storage_cost_list.append(best_worst_node['best_storage_cost'])
            max_latency_time_list.append(best_worst_node['worst_latency_time'])
            max_storage_cost_list.append(best_worst_node['worst_storage_cost'])
        optimizer_best_worst_node = {}
        optimizer_best_worst_node['best_storage_cost'] = min(min_storage_cost_list)
        optimizer_best_worst_node['worst_storage_cost'] = min(max_storage_cost_list)
        optimizer_best_worst_node['best_latency_time'] = max(min_latency_time_list)
        optimizer_best_worst_node['worst_latency_time'] = max(max_latency_time_list)

        optimizer_distance = OptimizerDistance()
        opt_result_distance_list = optimizer_distance.get_placement_distance_list(
            opt_result_storage_cost_list, opt_result_latency_time_list, optimizer_best_worst_node, target_weights)
        distance_min_value = min(opt_result_distance_list)
        distance_min_index = opt_result_distance_list.index(distance_min_value)
        optimizer_result = opt_result_list[distance_min_index]

        print "\n 多种纠删码参数，计算最终结果"
        # print 'opt_result_storage_cost_list', opt_result_storage_cost_list
        # print 'opt_result_latency_time_list', opt_result_latency_time_list
        # print 'opt_result_distance_list', opt_result_distance_list
        print 'optimizer_best_worst_node', optimizer_best_worst_node
        MyPrint().myprintlist(opt_result_storage_cost_list, 'opt_result_storage_cost_list')
        MyPrint().myprintlist(opt_result_latency_time_list, 'opt_result_latency_time_list')
        MyPrint().myprintlist(opt_result_distance_list, 'opt_result_distance_list')
        print "\n 多种纠删码参数，最终结果"
        MyPrint().myprintdict(optimizer_result, 'optimizer_result')



    ######################################################################################

    def get_fault_tolerance_features_list(self):
        # 纠删码配置参数列表
        cloud_availability = 0.9995  # 每一个云地域的可用性
        A_availability = 0.999999  # 总体可用性最小为A_availability
        N = len(CloudInformation().get_cloud_bucket_list())
        fault_tolerance_features_list = []
        for m in range(2, 3):  # 容错级别m的范围
            # for k in range(1, N+1-m):
            for k in range(1, 7):
                if k+m > N:
                    break
                A0 = self.availability_value(cloud_availability, k, m)
                # print 'k', k, 'm', m, 'A', A0
                if A_availability > A0:
                    break
                fault_tolerance_features = {
                    'fault_tolerance_level': m,
                    'erasure_code_k': k,
                    'erasure_code_n': m+k,  # erasure_code_n = erasure_code_k + fault_tolerance_level
                    'availability': A0,
                }
                fault_tolerance_features_list.append(fault_tolerance_features)
        return fault_tolerance_features_list

    def availability_value(self, cloud_availability, k, m):
        # 可用性计算
        n = m + k
        A = 0
        for fac_m in range(m+1, n+1):
            A0 = self.combination_value(n, fac_m)
            for i in range(fac_m):
                A0 *= (1.0-cloud_availability)
            for i in range(n - fac_m):
                A0 *= cloud_availability
            A += A0
        A = 1 - A
        return A

    def combination_value(self, n, m):
        # 组合 n选m
        return self.factorial_value(n)/(self.factorial_value(m)*self.factorial_value(n-m))

    def factorial_value(self, n):
        # 阶乘
        res = 1.0
        for i in range(1, n+1):
            res *= i
        return res




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



    optimizer_availability = OptimizerAvailability()
    res = optimizer_availability.get_fault_tolerance_features_list()
    MyPrint().myprintlist(res, "fault list")
    optimizer_availability.optimizer_availability()
