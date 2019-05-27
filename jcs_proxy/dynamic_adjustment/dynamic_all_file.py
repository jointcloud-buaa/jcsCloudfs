# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/6/28 15:58'

import os
from adjustment_truth import AdjustmentTruth
from dynamic_policy import DynamicPolicy

class DynamicAllFile(object):
    """
    每月统计所有文件的下载模式，进行动态调整
    """
    def __init__(self, dynamic_run):
        """
        :param dynamic_run:  虚拟数据执行/真实数据执行
        """
        self.dynamic_run = dynamic_run

    def dynamic_all_file(self):
        """
        遍历所有文件
        :return:
        """
        print "\n每月统计所有文件的下载模式"
        list_all_dir_name = self.dynamic_run.list_all_dir_name()  # 所有文件
        print 'list_all_dir_name', list_all_dir_name
        self.deep_cal(list_all_dir_name)

    def deep_cal(self, list_all, now_dir_path=""):
        """
        深度遍历所有文件，进行动态调整
        :param list_all:
        :param now_dir_path:
        :return:
        """
        for list_one in list_all:
            file_path = os.path.join(now_dir_path, list_one['file_name'])
            if list_one['isdir'] == True:
                self.deep_cal(list_one['children'], file_path)
            else:
                # 处理文件
                file_key = file_path
                file_download_mode = self.dynamic_run.get_file_download_mode_monthly(file_key)  # 一个文件的下载模式
                print '一个文件的下载模式file_download_mode', file_download_mode
                file_request_features = file_download_mode[file_key]
                if len(file_request_features) == 0:  # 如果一个月下载次数为0，需要重新定义下载模式
                    file_request_features = self.month_download_zero(file_key)
                    print "文件一个内下载次数为0", file_request_features
                # 动态调整
                dynamic_policy = DynamicPolicy(self.dynamic_run)
                dynamic_policy.dynamic_policy(file_key, file_request_features)

    def month_download_zero(self, file_key):
        file_metadata = self.dynamic_run.get_file_metadata(file_key)
        jcsproxy_request_features = file_metadata['jcsproxy_request_features']
        for jcsproxy_area in jcsproxy_request_features:
            jcsproxy_request_features[jcsproxy_area] = 0.1
        return jcsproxy_request_features





