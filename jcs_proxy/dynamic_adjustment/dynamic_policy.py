# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/6/21 14:48'

from metadata.file_info import MetadataFileInfo
from optimizer.optimizer import Optimizer
from optimizer.myprint import MyPrint
from config.cloud_information import CloudInformation
from migration_policy import MigrationPolicy

class DynamicPolicy(object):
    """
    计算动态调整策略,只计算
    """
    def __init__(self, dynamic_run):
        self.dynamic_run = dynamic_run

    def dynamic_policy(self, file_key, file_request_features):
        """
        计算动态调整策略，过程(一个文件)
        :param file_key:
        :param file_request_features:
        :return:
        """
        # 计算动态调整相关信息值
        file_metadata, old_policy, new_policy = self.cal_policy_info(file_key, file_request_features)
        # 动态调整操作判断
        #  old_policy和new_policy，distance比较
        if new_policy['distance'] < old_policy['distance']:
            print "\n进行数据迁移，并更新元数据"
            self.dynamic_run.data_block_migration(file_key, file_request_features, new_policy, file_metadata['cloud_block_path_dict'])
        else:  # 不进行数据迁移
            # old_policy和origin_policy，jcsproxys_download_plan比较
            if not self.check_jcsproxy_bucket(old_policy['jcsproxy_bucket_name_list'], file_metadata['jcsproxy_bucket_name_list']):
                print "\n只更新元数据"
                self.dynamic_run.update_metadata(file_key, old_policy)
            else:
                print "\n不执行任何操作"

    def cal_policy_info(self, file_key, file_request_features):
        """
        计算相关信息值
        :param file_key:
        :param file_request_features:
        :return:
        """
        # 获取元数据
        file_metadata = self.dynamic_run.get_file_metadata(file_key)
        # 计算旧策略，新策略
        optimizer = Optimizer()
        optimizer_init = optimizer.get_optimizer_init(file_metadata['file_size'],
                                            file_metadata['storage_time'], file_request_features)
        best_worst_node = optimizer.get_best_worst_node(optimizer_init)
        old_placement = self.get_placement_from_bucket_list(file_metadata['bucket_name_list'])
        old_policy = optimizer.get_optimizer_placement(optimizer_init, placement=old_placement)
        new_policy = optimizer.get_optimizer_placement(optimizer_init)

        # 迁移策略和迁移成本
        # migration_diff, migration_cost = MigrationPolicy().migration_policy(file_metadata, old_policy, new_policy)

        # 数据重置成本，为一次下载成本
        jcsproxy_list = ['aliyun-beijing', 'aliyun-shanghai', 'aliyun-shenzhen']
        jcsproxy_storage_cost = old_policy['jcsproxy_storage_cost']
        jcsproxy_area = 'aliyun-beijing'
        for jcsproxy_one in jcsproxy_list:
            if jcsproxy_storage_cost.has_key(jcsproxy_one):
                jcsproxy_area = jcsproxy_one
                break
        download_expense = jcsproxy_storage_cost[jcsproxy_area]['download_expense']
        request_frequency = old_policy['jcsproxy_storage_features'][jcsproxy_area]['request_frequency']
        migration_cost = download_expense/float(request_frequency)


        # 更新新策略的distance
        new_cost = new_policy['storage_cost']+migration_cost
        new_distance = self.get_placement_distance(best_worst_node, new_cost, new_policy['latency_time'],
                                                   new_policy['target_weights'])
        new_policy['distance'] = new_distance

        print ""
        print "计算相关信息值"
        MyPrint().myprintdict(file_metadata, 'file_metadata')
        MyPrint().myprintdict(old_policy, 'old_policy')
        MyPrint().myprintdict(new_policy, 'new_policy')
        print ""
        print 'best_worst_node', best_worst_node
        print 'old_policy[\'storage_cost\']', old_policy['storage_cost']
        print 'old_policy[\'latency_time\']', old_policy['latency_time']
        print 'old_policy[\'distance\']', old_policy['distance']
        print 'new_policy[\'storage_cost\']', new_policy['storage_cost']
        print 'new_policy[\'latency_time\']', new_policy['latency_time']
        print 'new_policy[\'distance\']', new_policy['distance']
        # print 'migration_diff', migration_diff
        print 'migration_cost', migration_cost
        return file_metadata, old_policy, new_policy  #, migration_diff


    ####################################################################################

    def get_placement_from_bucket_list(self, bucket_name_list):
        """
        bucket_name_list -> placement
        :param bucket_name_list:
        :return:
        """
        cloud_bucket_list = CloudInformation().get_cloud_bucket_list()
        placement = []
        for bucket_name in bucket_name_list:
            for i, cloud_bucket in enumerate(cloud_bucket_list):
                if bucket_name == cloud_bucket['bucket_name']:
                    placement.append(i)
        return placement

    def check_bucket_list(self, old_bucket_list, new_bucket_list):
        """
        数据放置方案是否相同
        :param old_bucket_list:
        :param new_bucket_list:
        :return:
        """
        for new_bucket_name in new_bucket_list:
            if new_bucket_name not in old_bucket_list:
                return False
        return True

    def check_jcsproxy_bucket(self, old_jcsproxy_bucket, new_jcsproxy_bucket):
        """
        数据下载方案是否相同
        :param old_jcsproxy_bucket_list:
        :param new_jcsproxy_bucket_list:
        :return:
        """
        if len(old_jcsproxy_bucket) != len(new_jcsproxy_bucket):
            return False
        for jcsproxy_area in old_jcsproxy_bucket:
            if jcsproxy_area not in new_jcsproxy_bucket:
                return False
            for old_bucket_i in old_jcsproxy_bucket[jcsproxy_area]:
                if old_bucket_i not in new_jcsproxy_bucket[jcsproxy_area]:
                    return False
        return True


    def get_placement_distance(self, best_worst_node, storage_cost, latency_time, target_weights):
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
        print "**************"
        print 'storage_cost', storage_cost
        print 'latency_time', latency_time
        print 'storage_cost_distance', storage_cost_distance
        print 'latency_time_distance', latency_time_distance
        return distance


