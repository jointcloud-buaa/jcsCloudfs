# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/11/28 15:42'

from optimizer.optimizer import Optimizer
from optimizer.myprint import MyPrint
from tools.get_func_time import GetFuncTime

class OptimizerTest(object):

    def test_file_list(self):
        file_size_list = [64]
        # file_size_list = [4, 8, 16, 32, 64, 128, 256, 512]
        res_list = []
        time_list = []
        for file_size in file_size_list:
            res, func_time = self.test_file_one(file_size)
            res_list.append(res)
            time_list.append(func_time)

        print "\n输出"
        for res in res_list:
            print res
        print "处理placement"
        for res in res_list:
            placement = res['placement']
            print sorted([i + 1 for i in placement])
            placement_nk = res['jcsproxy_placement_nk']
            for jcsproxy_area in placement_nk:
                print jcsproxy_area
                print sorted([i + 1 for i in placement_nk[jcsproxy_area]])

        print "成本", [res['storage_cost'] for res in res_list]
        print "延迟", [res['latency_time'] for res in res_list]
        print "时间开销", time_list

    def test_file_one(self, file_size):
        # file_size = 64
        storage_time = 1
        jcsproxy_request_features = {
            'aliyun-beijing': 1000,
            'aliyun-shanghai': 0,
            'aliyun-shenzhen': 1000,
        }
        fault_tolerance_features = {
            'fault_tolerance_level': 1,
            'erasure_code_k': 4,
            'erasure_code_n': 6,
        }
        target_weights = {}  # 优化目标权重
        target_weights['storage_cost_weight'] = 0.5
        target_weights['latency_time_weight'] = 0.5

        # 自定义placement
        placement = [i - 1 for i in [1,  3, 5, 6, 7]]
        optimizer_res, func_time = GetFuncTime().get_func_time(self.opt_run,
                        (file_size, storage_time, jcsproxy_request_features,
                     fault_tolerance_features, target_weights, placement), )

        # print "输出"
        # MyPrint().myprintdict(optimizer_res, 'optimizer_res')
        # print "placement 处理"
        # placement = optimizer_res['placement']
        # print [i + 1 for i in placement]
        # placement_nk = optimizer_res['jcsproxy_placement_nk']
        # for jcsproxy_area in placement_nk:
        #     print jcsproxy_area
        #     print [i + 1 for i in placement_nk[jcsproxy_area]]
        return optimizer_res, func_time

    def opt_run(self, file_size, storage_time, jcsproxy_request_features,
                     fault_tolerance_features, target_weights, placement):
        optimizer = Optimizer()
        optimizer_init = optimizer.get_optimizer_init(file_size, storage_time, jcsproxy_request_features,
                                                      fault_tolerance_features, target_weights)
        optimizer_res = optimizer.get_optimizer_placement(optimizer_init, placement)  # 根据指定的placement
        return optimizer_res

if __name__ == '__main__':
    test = OptimizerTest()
    test.test_file_list()







