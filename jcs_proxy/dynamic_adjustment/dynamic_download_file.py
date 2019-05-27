# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/6/28 15:58'

import os
from dynamic_policy import DynamicPolicy

class DynamicDownloadFile(object):
    """
    每天统计下载文件的下载模式，进行动态调整
    """
    def __init__(self, dynamic_run):
        """
        :param dynamic_run:  虚拟数据执行/真实数据执行
        """
        self.dynamic_run = dynamic_run
        self.timedelta_daily = 1.0
        self.file_download_model = {}  # 设置下载模式

    def set_file_download_model(self, user_name, file_name, download_model):
        self.file_download_model[os.path.join(user_name, file_name)] = download_model

    def dynamic_download_file(self):
        """
        遍历所有下载文件
        :param file_download_mode:
        :return:
        """
        print "\n每天统计下载文件的下载模式"
        # 获取一天内的下载模式
        if self.file_download_model == {}:
            file_download_mode = self.dynamic_run.get_file_download_mode_daily()  # 下载文件的下载模式
        else:
            file_download_mode = self.file_download_model
        print 'file_download_mode', file_download_mode
        if len(file_download_mode) == 0:
            print "\n一天内没有文件下载"
            return None

        for file_key, file_request_features in file_download_mode.iteritems():
            file_request_features = self.change_day_to_month(file_request_features)
            print file_key, file_request_features
            check_exists = self.dynamic_run.check_file_exists(file_key)
            if check_exists["status"] == 1:
                print "文件不存在，可能已被删除"
                # return None
                continue
            # 动态调整
            dynamic_policy = DynamicPolicy(self.dynamic_run)
            dynamic_policy.dynamic_policy(file_key, file_request_features)

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

