# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/5/24 18:28'

from config.cloud_information import CloudInformation
from myprint import MyPrint
from optimizer_init import OptimizerInit
from optimizer_distance import OptimizerDistance
from optimizer_replacement import OptimizerReplacement
from tools.get_func_time import GetFuncTime

class OptimzierTimeTest(object):
    def __init__(self):
        pass

    def test_run(self):
        loop_num = 3
        func_time1_list = []
        func_time2_list = []
        for i in range(loop_num):
            func_time1, func_time2 = self.run()
            func_time1_list.append(func_time1)
            func_time2_list.append(func_time2)

        avg_time1 = self.avg_list(func_time1_list)
        avg_time2 = self.avg_list(func_time2_list)
        print ""
        print 'avg_time1', avg_time1
        print 'avg_time2', avg_time2
        print ""
        print "cloud bucket list len:", len(CloudInformation().get_cloud_bucket_list())

    def avg_list(self, my_list):
        sum = 0.0
        for one in my_list:
            sum += one
        avg = sum / len(my_list)
        return avg


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


        # opt_result1, best_worst_node1, func_time1 = self.traversal_cal(optimizer_init)
        opt_result1, best_worst_node1, func_time1 = self.replacement_cal(optimizer_init)
        opt_result2, best_worst_node2, func_time2 = self.replacement_cal(optimizer_init)
        print ""
        MyPrint().myprintdict(opt_result1, 'opt_result1')
        MyPrint().myprintdict(opt_result2, 'opt_result2')
        print ""
        MyPrint().myprintdict(best_worst_node1, 'best_worst_node1')
        MyPrint().myprintdict(best_worst_node2, 'best_worst_node2')
        print ""
        print 'func_time1', func_time1
        print 'func_time2', func_time2
        print ""
        # 两个结果是否相等
        print opt_result1['latency_time'] == opt_result2['latency_time']
        print opt_result1['storage_cost'] == opt_result2['storage_cost']
        print best_worst_node1 == best_worst_node2
        return func_time1, func_time2



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
    opt_time_test = OptimzierTimeTest()
    opt_time_test.test_run()