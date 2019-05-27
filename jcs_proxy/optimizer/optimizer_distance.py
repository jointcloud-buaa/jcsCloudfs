# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/5/15 19:42'


from optimizer_init import OptimizerInit
from optimizer_placement import OptimizerPlacement
from myprint import MyPrint
from placement_nk_interface import PlacementNkInterface


class OptimizerDistance(object):
    def __init__(self):
        pass

    def optimzer_distance(self, optimizer_init):
        # 遍历求解距离best点最近的节点
        optimizer_placement = OptimizerPlacement()
        placement_list = optimizer_placement.get_optimizer_placement(optimizer_init)
        best_worst_node = self.get_best_worst_node(placement_list)
        placement_list = self.get_distance_list(placement_list, best_worst_node, optimizer_init.target_weights)
        opt_result = self.get_opt_result(placement_list, optimizer_init, optimizer_placement)
        # print ""
        # MyPrint().myprintdict(opt_result, "opt result:")
        return placement_list, opt_result

    ###################################################################################################

    def get_best_worst_node(self, placement_list):
        # 虚拟最优点，虚拟最差点
        storage_cost_min = 100000000
        storage_cost_max = -1
        for placement_info in placement_list:
            placement_min = min(placement_info['storage_cost_list'])
            placement_max = max(placement_info['storage_cost_list'])
            if storage_cost_min > placement_min:
                storage_cost_min = placement_min
            if storage_cost_max < placement_max:
                storage_cost_max = placement_max

        latency_time_min = 100000000
        latency_time_max = -1
        for placement_info in placement_list:
            placement_min = min(placement_info['latency_time_list'])
            placement_max = max(placement_info['latency_time_list'])
            if latency_time_min > placement_min:
                latency_time_min = placement_min
            if latency_time_max < placement_max:
                latency_time_max = placement_max

        best_worst_node = {}
        best_worst_node['best_storage_cost'] = storage_cost_min
        best_worst_node['worst_storage_cost'] = storage_cost_max
        best_worst_node['best_latency_time'] = latency_time_min
        best_worst_node['worst_latency_time'] = latency_time_max

        # print ""
        # print "best_worst_node", best_worst_node
        return best_worst_node

    ###############################################################################################

    def get_distance_list(self, placement_list, best_worst_node, target_weights):
        for placement_info in placement_list:
            distance_list = self.get_placement_distance_list(placement_info['storage_cost_list'],
                                    placement_info['latency_time_list'], best_worst_node, target_weights)
            placement_info['distance_list'] = distance_list
        return placement_list

    def get_placement_distance_list(self, storage_cost_list, latency_time_list, best_worst_node, target_weights):
        distance_list = []
        for i in range(len(storage_cost_list)):
            if (best_worst_node['worst_storage_cost'] - best_worst_node['best_storage_cost']) == 0:
                storage_cost_distance = 0.0
            else:
                storage_cost_distance = (storage_cost_list[i] - best_worst_node['best_storage_cost']) \
                                        / 1 #(best_worst_node['worst_storage_cost'] - best_worst_node['best_storage_cost'])
            storage_cost_distance = storage_cost_distance * target_weights['storage_cost_weight']
            latency_time_distance = (latency_time_list[i] - best_worst_node['best_latency_time']) \
                                    / 1 #(best_worst_node['worst_latency_time'] - best_worst_node['best_latency_time'])
            latency_time_distance = latency_time_distance * target_weights['latency_time_weight']
            # distance = math.sqrt(storage_cost_distance * storage_cost_distance +
            #                      latency_time_distance * latency_time_distance)
            distance = storage_cost_distance * storage_cost_distance + \
                                 latency_time_distance * latency_time_distance
            distance_list.append(distance)
        return distance_list

    ###############################################################################################

    def get_opt_result(self, placement_list, optimizer_init, optimizer_placement):
        placement_distance_list = []
        for placement_info in placement_list:
            placement_distance_list.append(min(placement_info['distance_list']))
        opt_distance_value = min(placement_distance_list)
        opt_placement_index = placement_distance_list.index(opt_distance_value)
        opt_placement_info = placement_list[opt_placement_index]

        opt_placement = opt_placement_info['placement']  # 最优方案
        opt_plan_power_index = opt_placement_info['distance_list'].index(opt_distance_value)
        opt_storage_cost = opt_placement_info['storage_cost_list'][opt_plan_power_index]
        opt_latency_time = opt_placement_info['latency_time_list'][opt_plan_power_index]

        jcsproxy_placement_nk = self.get_jcsproxy_placement_nk_from_power(
            opt_placement, opt_plan_power_index, optimizer_init.jcsproxy_area_list,
            optimizer_placement.plan_nk_list, optimizer_placement.plan_power_list)

        opt_result = {}
        opt_result['placement'] = opt_placement
        opt_result['jcsproxy_placement_nk'] = jcsproxy_placement_nk
        opt_result['storage_cost'] = opt_storage_cost
        opt_result['latency_time'] = opt_latency_time
        opt_result['distance'] = opt_distance_value
        # jcsproxy_placement_nk属性值
        opt_result.update(self.get_jcsproxy_placement_nk_info(opt_placement, jcsproxy_placement_nk, optimizer_init))
        # 输入属性值
        opt_result['jcsproxy_storage_features'] = optimizer_init.jcsproxy_storage_features
        opt_result['fault_tolerance_features'] = optimizer_init.fault_tolerance_features
        opt_result['target_weights'] = optimizer_init.target_weights
        return opt_result

    def get_jcsproxy_placement_nk_info(self, placement, jcsproxy_placement_nk, optimizer_init):
        placement_nk_operate = PlacementNkInterface()
        jcsproxy_latency_time = placement_nk_operate.jcsproxy_latency_time_nk(placement, jcsproxy_placement_nk, optimizer_init)
        jcsproxy_storage_cost = placement_nk_operate.jcsproxy_storage_cost_nk(placement, jcsproxy_placement_nk, optimizer_init)

        placement_bucket_name_list = self.get_placement_bucket_name_list(placement, optimizer_init.cloud_bucket_list)
        jcsproxy_placement_nk_bucket_name_list = self.get_jcsproxy_placement_nk_bucket_name_list(jcsproxy_placement_nk, optimizer_init.cloud_bucket_list)

        placement_nk_info = {}
        placement_nk_info['jcsproxy_storage_cost'] = jcsproxy_storage_cost
        placement_nk_info['jcsproxy_latency_time'] = jcsproxy_latency_time
        placement_nk_info['bucket_name_list'] = placement_bucket_name_list
        placement_nk_info['jcsproxy_bucket_name_list'] =  jcsproxy_placement_nk_bucket_name_list
        return placement_nk_info


    def get_jcsproxy_placement_nk_from_power(self, placement, power_index, jcsproxy_area_list, plan_nk_list, plan_power_list):
        # 根据power_index，取得jcsproxy_placement_nk
        jcsproxy_placement_nk = {}
        plan_power = plan_power_list[power_index]
        for i in range(len(plan_power)):
            plan_nk = plan_nk_list[plan_power[i]]
            placement_nk = []
            for j in range(len(plan_nk)):
                placement_nk.append(placement[plan_nk[j]])
            jcsproxy_area = jcsproxy_area_list[i]
            jcsproxy_placement_nk[jcsproxy_area] = placement_nk
        return jcsproxy_placement_nk


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



if __name__ == '__main__':
    # 输入参数
    jcsproxy_request_features = {
        'aliyun-beijing': 3,
        'aliyun-shanghai': 0,
        'aliyun-shenzhen': 0,
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

    optimizer_distance = OptimizerDistance()
    placement_list, opt_result = optimizer_distance.optimzer_distance(optimizer_init)
    MyPrint().myprintdict(opt_result, 'opt_result')




