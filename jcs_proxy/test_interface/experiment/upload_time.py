# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/11/28 14:56'


import os
from config.configuration import CONFIG
from manager.put_file import PutFile
from tools.get_func_time import GetFuncTime

class UploadDownloadTime(object):
    def __init__(self):
        pass

    def put_file_list(self):
        # file_size_list = [4, 8]
        file_size_list = [4, 8, 16, 32, 64, 128, 256, 512]
        res_list = []
        time_list = []
        for file_size in file_size_list:
            res, func_time = self.put_file_one(file_size)
            res_list.append(res)
            time_list.append(func_time)

        print "\n输出"
        print "处理placement"
        for res in res_list:
            placement = res['result']['file_info']['optimizer_res']['placement']
            print sorted([i+1 for i in placement])
        print "时间开销", time_list


    def put_file_one(self, file_size):
        print "上传测试开始，file_size", file_size
        # 文件路径
        # file_size = 64
        user_name = "liuyf_test"
        cloud_file_path = "dir/test_" + str(file_size)
        local_file_path = os.path.join(CONFIG["test_file_path"], "test_" + str(file_size))

        # 配置参数
        # file_size
        storage_time = 1
        jcsproxy_request_features = {
            'aliyun-beijing': 1000,
            'aliyun-shanghai': 0,
            'aliyun-shenzhen': 1000,
        }
        fault_tolerance_features = None
        target_weights = {}
        target_weights['storage_cost_weight'] = 0.5
        target_weights['latency_time_weight'] = 0.5

        res, func_time = GetFuncTime().get_func_time(PutFile().put_file,
                            (user_name, cloud_file_path, local_file_path, True,
                            storage_time, jcsproxy_request_features, fault_tolerance_features, target_weights))
        print "上传测试结束，file_size", file_size
        print res
        print func_time
        # print res['result']['file_info']['optimizer_res']['placement']
        # print res['result']['file_info']['optimizer_res']['bucket_name_list']
        # print res['result']['file_info']['optimizer_res']['jcsproxy_bucket_name_list']
        return res, func_time


if __name__ == '__main__':
    test = UploadDownloadTime()
    test.put_file_list()





