# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/6/27 13:36'

from dynamic_adjustment.adjustment_customization import AdjustmentCustomization
from all_file_request_features import AllFileRequestFeatures
from dynamic_adjustment.dynamic_all_file import DynamicAllFile

class DownloadFileCustomizationTest(object):

    def test_run(self, download_features_func):
        # 获取下载模式
        customize_request_features_origin, customize_request_features_new = \
                    download_features_func()
        adjustment_customization = AdjustmentCustomization(
                    customize_request_features_origin, customize_request_features_new)
        DynamicAllFile(adjustment_customization).dynamic_all_file()

if __name__ == '__main__':
    download_featrues = AllFileRequestFeatures()
    dynamic_test = DownloadFileCustomizationTest()

    # dynamic_test.test_run(download_featrues.test_no_download)0l
    # dynamic_test.test_run(download_featrues.test_no_operation)
    # dynamic_test.test_run(download_featrues.test_update_metadata)
    dynamic_test.test_run(download_featrues.test_data_block_migration)