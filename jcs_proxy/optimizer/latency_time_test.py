# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/11/29 2:51'

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from config.configuration import CONFIG
from config.cloud_information import CloudInformation
from cloud_interface.cloud_interface import CloudInterface
from tools.get_func_time import GetFuncTime

class LatencyTimeTest(object):
    def __init__(self):
        self.cloud_bucket_list = CloudInformation().get_cloud_bucket_list()
        self.jcsproxy_area = CONFIG['jcsproxy_area']
        self.loop_num = 5  # 循环测试次数
        self.file_size_list = [4]  # 测试文件大小
        self.time_sleep = 2  # 间隔时间s

    def test_run(self):
        upload_res = {}
        download_res = {}
        for loop_one in range(self.loop_num):
            for file_size in self.file_size_list:
                print 'file_size: ', file_size
                upload_time_list, download_time_list = self.test_file_one(file_size)
                upload_res[loop_one] = upload_time_list
                download_res[loop_one] = download_time_list

        print "\计算平均值结果"
        print "upload_res_avg", self.cal_avg(upload_res)
        print "download_res_avg", self.cal_avg(download_res)

    def cal_avg(self, res_dict):
        # 计算平均值，先相加，再除以loop_num
        res_list = res_dict[0]
        for loop_i in range(1, self.loop_num):
            for res_one in res_list:
                bucket_name = res_one['bucket_name']
                new_list = res_dict[loop_i]
                for new_one in new_list:
                    if new_one['bucket_name'] == bucket_name:
                        res_one['latency_time'] += new_one['latency_time']
                        break
        for res_one in res_list:
            res_one['latency_time'] /= self.loop_num
        return res_list



    def test_file_one(self, file_size):
        upload_time_list = []
        download_time_list = []
        for cloud_bucket in self.cloud_bucket_list:
            cloud_account = CloudInformation().get_cloud_account_from_bucket_name(cloud_bucket['bucket_name'])
            cloud_path = "latency_test"+CONFIG['jcsproxy_area']
            file_path = os.path.join(CONFIG["test_file_path"], "test_"+str(file_size))

            cloud_operate = CloudInterface(cloud_account)
            res, func_time = GetFuncTime().get_func_time(cloud_operate.put_file, (cloud_path, file_path))
            new_dict = {}
            new_dict['cloud_name'] = cloud_bucket['cloud_name']
            new_dict['bucket_name'] = cloud_bucket['bucket_name']
            new_dict['jcsproxy_area'] = CONFIG['jcsproxy_area']
            new_dict['latency_time'] = func_time
            upload_time_list.append(new_dict)

            cloud_operate = CloudInterface(cloud_account)
            res, func_time = GetFuncTime().get_func_time(cloud_operate.get_file, (cloud_path, file_path))
            new_dict = {}
            new_dict['cloud_name'] = cloud_bucket['cloud_name']
            new_dict['bucket_name'] = cloud_bucket['bucket_name']
            new_dict['jcsproxy_area'] = CONFIG['jcsproxy_area']
            new_dict['latency_time'] = func_time
            download_time_list.append(new_dict)
        print 'upload_time_list', upload_time_list
        print 'download_time_list', download_time_list
        return upload_time_list, download_time_list

if __name__ == '__main__':
    test = LatencyTimeTest()
    test.test_run()




