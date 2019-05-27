# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/5/24 16:40'

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from optimizer_init import OptimizerInit
from optimizer_distance import OptimizerDistance
import json
from replacement_latency_time_minmax import ReplacementLatencyTimeMinmax
from replacement_storage_cost_minmax import ReplacementStorageCostMinmax
from optimizer_replacement import OptimizerReplacement

class OptimizerPlot(object):
    def __init__(self):
        pass

    def optimizer_plot(self, optimizer_init):
        optimizer_distance = OptimizerDistance()
        placement_list, opt_result = optimizer_distance.optimzer_distance(optimizer_init)
        best_worst_node = optimizer_distance.get_best_worst_node(placement_list)

        print "画图"
        self.plot_result(placement_list, best_worst_node, opt_result, optimizer_init)



    def plot_result(self, placement_list, best_worst_node, opt_result, optimizer_init):
        # 画图
        # 提取所有情况值
        storage_cost_list = []
        latency_time_list = []
        for placement_info in placement_list:
            storage_cost_list += placement_info['storage_cost_list']
            latency_time_list += placement_info['latency_time_list']

        plt.figure()
        # 所有情况，画图
        # plt.plot(storage_cost_list, latency_time_list, 'b.')
        plt.scatter(storage_cost_list, latency_time_list, s=1, c='b', marker='.')
        plt.plot(best_worst_node['best_storage_cost'], best_worst_node['best_latency_time'], 'g*')
        plt.plot(best_worst_node['worst_storage_cost'], best_worst_node['worst_latency_time'], 'g*')
        plt.plot(opt_result['storage_cost'], opt_result['latency_time'], 'r*')

        # latency_time 替换取得最小值/最大值过程，画图
        replacement_latency_time_minmax = ReplacementLatencyTimeMinmax()
        replacement_latency_time_minmax_list = replacement_latency_time_minmax.replacement_latency_time_minmax_list(
            optimizer_init)
        min_latency_time_list = []
        min_storage_cost_list = []
        max_latency_time_list = []
        max_storage_cost_list = []
        for minmax_info in replacement_latency_time_minmax_list:
            min_latency_time_list.append(minmax_info['latency_time_min'])
            min_storage_cost_list.append(minmax_info['storage_cost_min'])
        for minmax_info in replacement_latency_time_minmax_list:
            max_latency_time_list.append(minmax_info['latency_time_max'])
            max_storage_cost_list.append(minmax_info['storage_cost_max'])
        plt.scatter(min_storage_cost_list, min_latency_time_list, s=12, c='g', marker='o')
        plt.scatter(max_storage_cost_list, max_latency_time_list, s=12, c='g', marker='o')

        # storage_cost 替换取得最小值/最大值过程，画图
        replacement_storage_cost_minmax = ReplacementStorageCostMinmax()
        replacement_storage_cost_min_list, replacement_storage_cost_max_list = \
            replacement_storage_cost_minmax.replacement_storage_cost_minmax_list(optimizer_init)
        min_storage_cost_list = []
        min_latency_time_list = []
        max_storage_cost_list = []
        max_latency_time_list = []
        for minmax_info in replacement_storage_cost_min_list:
            min_storage_cost_list.append(minmax_info['storage_cost_min'])
            min_latency_time_list.append(minmax_info['latency_time_min'])
        for minmax_info in replacement_storage_cost_max_list:
            max_storage_cost_list.append(minmax_info['storage_cost_max'])
            max_latency_time_list.append(minmax_info['latency_time_max'])
        plt.scatter(min_storage_cost_list, min_latency_time_list, s=12, c='g', marker='v')
        plt.scatter(max_storage_cost_list, max_latency_time_list, s=12, c='g', marker='s')

        # 最大最小值，画图
        latency_time_minmax_info = replacement_latency_time_minmax_list[len(replacement_latency_time_minmax_list) - 1]
        storage_cost_min_info = replacement_storage_cost_min_list[len(replacement_storage_cost_min_list) - 1]
        storage_cost_max_info = replacement_storage_cost_max_list[len(replacement_storage_cost_max_list) - 1]
        minmax_res = {}
        minmax_res['best_latency_time'] = latency_time_minmax_info['latency_time_min']
        minmax_res['worst_latency_time'] = latency_time_minmax_info['latency_time_max']
        minmax_res['best_storage_cost'] = storage_cost_min_info['storage_cost_min']
        minmax_res['worst_storage_cost'] = storage_cost_max_info['storage_cost_max']
        print ""
        print "minmax res:", minmax_res
        plt.plot(minmax_res['best_storage_cost'], minmax_res['best_latency_time'], 'g*')
        plt.plot(minmax_res['worst_storage_cost'], minmax_res['worst_latency_time'], 'g*')

        # replacement 求解最优过程，画图
        optimizer_replacement = OptimizerReplacement()
        replacement_min_list, replacement_opt_result = optimizer_replacement.optimizer_replacement(optimizer_init)
        min_storage_cost_list = []
        min_latency_time_list = []
        for placement_info in replacement_min_list:
            min_storage_cost_list.append(placement_info['storage_cost'])
            min_latency_time_list.append(placement_info['latency_time'])
        plt.scatter(min_storage_cost_list, min_latency_time_list, s=12, c='r', marker='o')
        plt.plot(replacement_opt_result['storage_cost'], replacement_opt_result['latency_time'], 'r*')


        # 设置表头，横坐标纵坐标
        plt.title('jcsproxy_storage_features:' + json.dumps(optimizer_init.jcsproxy_storage_features) + '\n'
            'fault_tolerance_features:' + json.dumps(optimizer_init.fault_tolerance_features) + '\n'
             'target_weights:' + json.dumps(optimizer_init.target_weights),
            fontsize=6)
        plt.xlabel('storage cost(Y)')
        plt.ylabel('latency time(s)')
        out_png = "plot_result_.png"
        plt.savefig(out_png, dpi=150)


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

    optimizer_plot = OptimizerPlot()
    optimizer_plot.optimizer_plot(optimizer_init)