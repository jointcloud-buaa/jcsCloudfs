# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/6/27 13:39'

from dynamic_adjustment.adjustment_truth import AdjustmentTruth
from datalog_operation.datalog_used_traffic import DatalogUsedTraffic
from manager.manager_interface import ManagerInterface
from config.configuration import CONFIG
import time
from all_file_request_features import AllFileRequestFeatures
from dynamic_adjustment.dynamic_all_file import DynamicAllFile
from metadata.zookeeper_delete import delete_zookeeper_all

class DownloadFileTruthTest(object):
    def __init__(self):
        self.timedelta_daily = 1.0
        self.user_name = "liuyf_test"
        self.cloud_file_path = "remote.txt"
        self.local_file_path = "/storage/liuyf_test/jcsProxyDir/datatest/test_4"
        self.download_file_path = "/storage/liuyf_test/jcsProxyDir/datatest/test_download"

    def test_run(self, download_features_func):
        # 获取下载模式
        customize_request_features_origin, customize_request_features_new = \
                download_features_func()
        # 根据下载模式执行操作
        self.create_test_situation(customize_request_features_origin, customize_request_features_new)
        time.sleep(1)
        # 数据放置动态调整
        adjustment_truth = AdjustmentTruth()
        DynamicAllFile(adjustment_truth).dynamic_all_file()

    def test_migration_correct(self):
        # 获取下载模式
        customize_request_features_origin, customize_request_features_new = \
                    AllFileRequestFeatures().test_data_block_migration()
        # 根据下载模式执行操作
        self.create_test_situation(customize_request_features_origin, customize_request_features_new)
        time.sleep(1)
        # 数据放置动态调整
        adjustment_truth = AdjustmentTruth()
        DynamicAllFile(adjustment_truth).dynamic_all_file()
        print "\n数据迁移后，第二次计算"
        DynamicAllFile(adjustment_truth).dynamic_all_file()

    def test_no_file(self):
        print "测试，删除已经存在的测试文件"
        # 获取下载模式
        customize_request_features_origin, customize_request_features_new = \
                    AllFileRequestFeatures().test_data_block_migration()
        # 根据下载模式执行操作
        self.create_test_situation(customize_request_features_origin, customize_request_features_new)
        print "删除已经存在的测试文件"
        manager_interface = ManagerInterface()
        print manager_interface.delete_file(self.user_name, self.cloud_file_path)
        time.sleep(1)
        # 数据放置动态调整
        adjustment_truth = AdjustmentTruth()
        DynamicAllFile(adjustment_truth).dynamic_all_file()

    def test_multi_file(self):
        print "测试，多文件处理"
        # 获取下载模式
        customize_request_features_origin, customize_request_features_new = \
            AllFileRequestFeatures().test_data_block_migration()
        # 根据下载模式执行操作
        self.create_test_situation(customize_request_features_origin, customize_request_features_new)
        print "\n\n再次上传下载，构建多个文件"
        # 获取下载模式
        customize_request_features_origin, customize_request_features_new = \
            AllFileRequestFeatures().test_update_metadata()
        # 根据下载模式执行操作
        self.user_name = "liuyf_test1"
        self.cloud_file_path = "remote1.txt"
        self.create_test_situation(customize_request_features_origin, customize_request_features_new)
        time.sleep(1)

        # 数据放置动态调整
        adjustment_truth = AdjustmentTruth()
        DynamicAllFile(adjustment_truth).dynamic_all_file()


    def create_test_situation(self, customize_request_features_origin, customize_request_features_new):
        print "上传测试文件"
        manager_interface = ManagerInterface()
        print manager_interface.put_file(self.user_name, self.cloud_file_path, self.local_file_path,
                                         cover=True, jcsproxy_request_features=customize_request_features_origin)  # 注意monthly
        print "更改CONFIG.jcsproxy_area，下载测试文件，构建操作日志"
        for jcsproxy_area, request_number in customize_request_features_new.iteritems():
            CONFIG['jcsproxy_area'] = jcsproxy_area
            for i in range(request_number):
                print manager_interface.get_file(self.user_name, self.cloud_file_path, self.download_file_path)


if __name__ == '__main__':
    print "删除ES中的测试日志"
    print DatalogUsedTraffic().delete_all()
    print "删除zookeeper中的所有元数据信息"
    delete_zookeeper_all()

    download_featrues = AllFileRequestFeatures()
    dynamic_test = DownloadFileTruthTest()

    # dynamic_test.test_run(download_featrues.test_no_download)
    # dynamic_test.test_run(download_featrues.test_no_operation)
    # dynamic_test.test_run(download_featrues.test_update_metadata)
    # dynamic_test.test_run(download_featrues.test_data_block_migration)
    #
    # dynamic_test.test_migration_correct()
    # dynamic_test.test_no_file()
    dynamic_test.test_multi_file()