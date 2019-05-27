# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/6/21 19:41'

from optimizer.optimizer import Optimizer
from optimizer.myprint import MyPrint
from optimizer.optimizer_availability import OptimizerAvailability

class AdjustmentCustomization(object):
    """
    自定义虚拟数据获取，自定义虚拟执行动态调整操作
    """

    def __init__(self, customize_request_features_origin=None, customize_request_features_new=None,
                 storage_time=None,
                 customize_file_key=None, customize_file_size=None, ):
        self.timedelta_daily = 1  # 侧重于每天下载量多的文件尽快调整，统计1天内文件下载模式
        self.timedelta_monthly = 30  # 侧重于每个月的下载量少的文件调整，统计30天内文件下载模式
        # self.dynamic_path = CONFIG['datatest_path']  # 动态调整数据块的下载路径

        # 自定义数据量，计算动态调整策略时使用(如果是None，则使用默认数值)
        if customize_file_key==None:
            customize_file_key = "test_64"
        if customize_file_size==None:
            customize_file_size = 64.0
        if storage_time==None:
            storage_time = 1
        if customize_request_features_origin == None:
            customize_request_features_origin = {  # 初始1天的下载模式(get..month是每月的下载模式)
                'aliyun-beijing': 10,
                # 'aliyun-shanghai': 3,
                # 'aliyun-shenzhen': 10,
            }
        if customize_request_features_new == None:
            customize_request_features_new = {  # 当前统计1天新的下载模式(get..month是每月的下载模式)
                # 'aliyun-beijing': 10,
                # 'aliyun-shanghai': 0.3,
                'aliyun-shenzhen': 10,
            }

        self.customize_file_key = customize_file_key
        self.customize_file_size = customize_file_size
        self.customize_request_features_origin = customize_request_features_origin
        self.customize_request_features_new = customize_request_features_new
        self.customize_storage_time = storage_time
        self.fault_tolerance_features = {  # 纠删码参数
            'fault_tolerance_level': 2,
            'erasure_code_k': 3,
            'erasure_code_n': 5,  # erasure_code_n = erasure_code_k + fault_tolerance_level
        }
        self.target_weights = {  # 优化目标权重
            'storage_cost_weight': 0.5,
            'latency_time_weight': 0.5
        }

    def check_file_exists(self, file_key):
        dict_res = {}
        dict_res['status'] = 0
        return dict_res

    def get_file_download_mode_daily(self):
        """
        自定义一天内，文件下载模式
        包括：文件名，下载的jcsproxy，下载次数
        :return:
        """
        if len(self.customize_request_features_new) == 0:  # 如果一天内没有文件下载，返回{}
            return {}
        file_key = self.customize_file_key
        request_features = self.customize_request_features_new
        file_download_mode = {}
        file_download_mode[file_key] = request_features
        # print "\n获取每天的下载模式", file_download_mode
        return file_download_mode

    def get_file_download_mode_monthly(self, file_key):
        """
        统计一个月内，一个文件下载模式
        包括：文件名，下载的jcsproxy，下载次数
        :return:
        """
        request_features = self.customize_request_features_new
        file_download_mode = {}
        file_download_mode[file_key] = request_features  # 如果此文件一个月内没有下载，返回{"file_key":{}}
        # print "\n获取每月的下载模式",file_download_mode
        return file_download_mode

    def list_all_dir_name(self, dir_path=""):
        list_all_dir_name = [{'isdir': True, 'file_name': 'liuyf_test', 'children': [{'isdir': False, 'file_name': 'remote.txt'}]}]
        return list_all_dir_name

    def get_file_metadata(self, file_key):
        """
        自定义文件元数据信息
        :param file_key:
        :return:
        """
        # 计算动态调整策略需要用到的一些值
        res_dict = {}
        res_dict['file_key'] = self.customize_file_key
        res_dict['file_size'] = self.customize_file_size
        res_dict['storage_time'] = self.customize_storage_time
        res_dict['block_size'] = self.customize_file_size/self.fault_tolerance_features['erasure_code_k']
        res_dict['jcsproxy_request_features'] = self.change_day_to_month(self.customize_request_features_origin)
        # res_dict['jcsproxy_request_features'] = self.customize_request_features_origin
        # optimizer = Optimizer()
        # optimizer_init = optimizer.get_optimizer_init(self.customize_file_size, self.customize_storage_time,
        #                                     res_dict['jcsproxy_request_features'], self.fault_tolerance_features)
        # opt_result = optimizer.get_optimizer_placement(optimizer_init)

        file_size = self.customize_file_size
        storage_time = self.customize_storage_time
        jcsproxy_request_features = res_dict['jcsproxy_request_features']
        fault_tolerance_features = None
        target_weights = self.target_weights
        optimizer_availability = OptimizerAvailability()
        optimizer_res = optimizer_availability.optimizer_availability(file_size, storage_time,
                                                                      jcsproxy_request_features,
                                                                      fault_tolerance_features, target_weights)
        opt_result = optimizer_res

        res_dict['bucket_name_list'] = opt_result['bucket_name_list']
        res_dict['jcsproxy_bucket_name_list'] = opt_result['jcsproxy_bucket_name_list']
        res_dict['cloud_block_path_dict'] = self.get_cloud_block_path_dict(opt_result['bucket_name_list'])
        return res_dict

    def get_cloud_block_path_dict(self, bucket_name_list):
        """
        生成文件纠删码块名字
        :return:
        """
        cloud_file_key = self.customize_file_key
        fault_tolerance_features = self.fault_tolerance_features
        cloud_block_path_dict = {}
        for i in range(fault_tolerance_features['erasure_code_n']):
            if fault_tolerance_features['erasure_code_n'] > 9 and i <= 9:
                block_suffix = '.0' + str(i) + '_' + str(fault_tolerance_features['erasure_code_n']) + '.fec'  # 纠删码块后缀
            else:
                block_suffix = '.' + str(i) + '_' + str(fault_tolerance_features['erasure_code_n']) + '.fec'
            bucket_name = bucket_name_list[i]
            cloud_block_path_dict[bucket_name] = cloud_file_key.encode('utf-8') + block_suffix  # block纠删码块名字也可以是唯一id
        return cloud_block_path_dict

    ################################################################

    def data_block_migration(self, file_key, new_policy, migration_diff, cloud_block_path_dict):
        print "data_block_migration"
        # print "\n进行数据迁移，并更新元数据"
        MyPrint().myprintdict(new_policy, 'new_policy')
        # MyPrint().myprintdict(migration_diff, 'migration_diff')
        # MyPrint().myprintdict(cloud_block_path_dict, 'cloud_block_path_dict')
        self.update_metadata(file_key, new_policy)

    def update_metadata(self, file_key, change_policy):
        print "update_metadata"
        # print "\n更新元数据"
        print ""
        print 'file_key', file_key
        # MyPrint().myprintdict(change_policy, 'change_policy')

    ##############################################################################

    def change_day_to_month(self, file_request_features):
        """
        每天下载次数转换成每月下载次数计算
        :param file_request_features:
        :return:
        """
        for jcsproxy_area in file_request_features:
            file_request_features[jcsproxy_area] *= 30.0/self.timedelta_daily
        return file_request_features
