# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/5/31 23:36'

from config.cloud_information import CloudInformation
from myprint import MyPrint
from optimizer_init import OptimizerInit
from optimizer_distance import OptimizerDistance
from optimizer_replacement import OptimizerReplacement
from tools.get_func_time import GetFuncTime


class OptimizerResultTest(object):
    def __init__(self):
        pass

    def run(self):
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

        # print "optimizer init"
        optimizer_init = OptimizerInit(file_size, storage_time, jcsproxy_request_features,
                                       fault_tolerance_features, target_weights)


        print "遍历算法"
        opt_result1, best_worst_node1, func_time1 = self.traversal_cal(optimizer_init)
        MyPrint().myprintdict(opt_result1, 'correct opt_result1')
        print 'best_worst_node1', best_worst_node1

        print ""
        print "启发式算法结果测试"
        loop_num = 10000
        for i in range(loop_num):  # 启发式算法和遍历结果是否相同
            if i%500 == 0:
                print i
            opt_result2, best_worst_node2, func_time2 = self.replacement_cal(optimizer_init)
            if abs(opt_result1['latency_time'] - opt_result2['latency_time']) > 0.000001 \
                or abs(opt_result1['storage_cost'] - opt_result2['storage_cost']) > 0.0000001 \
                or best_worst_node1 != best_worst_node2:
                print ""
                print opt_result1['latency_time'] == opt_result2['latency_time']
                print opt_result1['storage_cost'] == opt_result2['storage_cost']
                print best_worst_node1 == best_worst_node2
                MyPrint().myprintdict(opt_result2, 'wrong opt_result2')
                print 'best_worst_node2', best_worst_node2






    def traversal_cal(self, optimizer_init):
        optimizer_distance = OptimizerDistance()
        # placement_list, opt_result = optimizer_distance.optimzer_distance(optimizer_init)
        res, func_time = GetFuncTime().get_func_time(optimizer_distance.optimzer_distance, (optimizer_init, ))
        placement_list = res[0]
        best_worst_node = optimizer_distance.get_best_worst_node(placement_list)
        opt_result = res[1]
        return opt_result, best_worst_node, func_time

    def replacement_cal(self, optimizer_init):
        optimizer_replacement = OptimizerReplacement()
        # replacement_res_list, opt_result = optimizer_replacement.optimizer_replacement(optimizer_init)
        res, func_time = GetFuncTime().get_func_time(optimizer_replacement.optimizer_replacement, (optimizer_init, ))
        best_worst_node = optimizer_replacement.best_worst_node
        replacement_res_list = res[0]
        opt_result = res[1]
        return opt_result, best_worst_node, func_time

if __name__ == '__main__':
    opt_res_test = OptimizerResultTest()
    opt_res_test.run()