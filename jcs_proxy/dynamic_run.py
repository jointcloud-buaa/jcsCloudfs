# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/7/4 21:00'

from dynamic_adjustment.adjustment_truth import AdjustmentTruth
from dynamic_adjustment.dynamic_download_file import DynamicDownloadFile
from dynamic_adjustment.dynamic_all_file import DynamicAllFile
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

def dynamic_download_file():
    # 动态调整下载文件的数据放置策略（每天）
    adjustment_truth = AdjustmentTruth()
    dynamic = DynamicDownloadFile(adjustment_truth)
    # 直接设置文件访问模式
    user_name = 'liuyf'
    # file_name = u'06_ZY1606311_刘云飞.pdf'
    # jcsproxy_request_features = {
    #     'aliyun-beijing': 0,
    #     'aliyun-shanghai': 30,
    #     'aliyun-shenzhen': 30,
    # }
    # dynamic.set_file_download_model(user_name, file_name, jcsproxy_request_features)
    # 进行动态调整
    dynamic.dynamic_download_file()


def dynamic_all_file():
    # 动态调整所有文件的数据放置策略（每月）
    adjustment_truth = AdjustmentTruth()
    DynamicAllFile(adjustment_truth).dynamic_all_file()


if __name__ == '__main__':
    # BlockingScheduler
    # scheduler = BlockingScheduler()
    # scheduler.add_job(dynamic_download_file, 'cron', hour=0)
    # scheduler.add_job(dynamic_all_file, 'cron', day=1, hour=1)
    # scheduler.start()

    dynamic_download_file()



