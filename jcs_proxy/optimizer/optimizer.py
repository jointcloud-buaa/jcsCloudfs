# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/5/31 19:43'

from config.configuration import CONFIG
from optimizer_init import OptimizerInit
from optimizer_replacement import OptimizerReplacement
from myprint import MyPrint

class Optimizer(object):
    def __init__(self):
        self.jcsproxy_area = CONFIG['jcsproxy_area']
        self.best_worst_node = None

    def get_optimizer_init(self, file_size, storage_time=None, jcsproxy_request_features=None,
                 fault_tolerance_features=None, target_weights=None):
        # 默认参数设置
        if storage_time == None:
            storage_time = 1
        if jcsproxy_request_features == None:
            jcsproxy_request_features = {}
            jcsproxy_request_features[self.jcsproxy_area] = 10

        if fault_tolerance_features == None:
            fault_tolerance_features = {  # 存储特性
                'fault_tolerance_level': 2,
                'erasure_code_k': 3,
                'erasure_code_n': 5,  # erasure_code_n = erasure_code_k + fault_tolerance_level
            }
        fault_tolerance_features['erasure_code_n'] = fault_tolerance_features['fault_tolerance_level'] + fault_tolerance_features['erasure_code_k']
        if target_weights == None:
            target_weights = {}  # 优化目标权重
            target_weights['storage_cost_weight'] = 0.5
        target_weights['latency_time_weight'] = 1 - target_weights['storage_cost_weight']

        optimizer_init = OptimizerInit(file_size, storage_time, jcsproxy_request_features,
                                        fault_tolerance_features, target_weights)
        return optimizer_init

    def get_optimizer_placement(self, optimizer_init, placement=None):
        optimizer_replacement = OptimizerReplacement()
        if placement == None:
            replacement_res_list, opt_result = optimizer_replacement.optimizer_replacement(optimizer_init)
        else:
            opt_result = optimizer_replacement.optimizer_placement_info(optimizer_init, placement)

        # 增加jcsproxy_request_features，storage_time信息
        update_dict = {}
        update_dict['jcsproxy_request_features'] = optimizer_init.jcsproxy_request_features
        update_dict['storage_time'] = optimizer_init.storage_time
        opt_result.update(update_dict)
        return opt_result

    def get_best_worst_node(self, optimizer_init):
        optimizer_replacement = OptimizerReplacement()
        return optimizer_replacement.get_best_worst_node(optimizer_init)


if __name__ == '__main__':
    opt = Optimizer()
    # file_size = 10
    # opt_result = opt.get_optimizer_placement(file_size)
    # MyPrint().myprintdict(opt_result, 'opt_result')
