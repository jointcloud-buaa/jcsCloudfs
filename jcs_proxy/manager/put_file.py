# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/1/15 16:58'

import os
import datetime
import hashlib
from cloud_interface.cloud_interface import CloudInterface
from metadata.file_info import MetadataFileInfo
from tools.get_func_time import GetFuncTime
from tools.get_dict_res import GetDictRes
from config.configuration import CONFIG
from optimizer.optimizer import Optimizer
from config.cloud_information import CloudInformation
from optimizer.erasure_code_zfec import ErasureCodeZfec
from datalog_operation.datalog_used_traffic import DatalogUsedTraffic
from tools.MyThread import MyThread
from optimizer.optimizer_availability import OptimizerAvailability


class PutFile(object):
    """
    上传文件操作
    """
    def __init__(self):
        self.jcsproxy_area = CONFIG['jcsproxy_area']

    def put_file(self, user_name, cloud_file_path, local_file_path, cover=False,
                 storage_time=None, jcsproxy_request_features=None,
                 fault_tolerance_features=None, target_weights=None,
                 placement=None):
        """
        上传文件（本地到云端）
        :param user_name: str, 用户名
        :param cloud_file_path: str, 云端文件路径
        :param local_file_path: str, 本地文件路径
        :param cover: bool, 是否覆盖文件
        :return: dict_res
        """
        file_operate = "put_file"
        # cloud_file_key = user_name + "/" + cloud_file_path
        cloud_file_key = os.path.join(user_name, cloud_file_path)
        # 1.计算数据放置策略
        file_size = os.path.getsize(local_file_path)
        file_size /= (1024.0*1024.0)

        if placement == None:
            optimizer_availability = OptimizerAvailability()
            optimizer_res = optimizer_availability.optimizer_availability(file_size, storage_time, jcsproxy_request_features,
                     fault_tolerance_features, target_weights)
        else:
            optimizer = Optimizer()
            optimizer_init = optimizer.get_optimizer_init(file_size, storage_time, jcsproxy_request_features,
                     fault_tolerance_features, target_weights)
            # optimizer_res = optimizer.get_optimizer_placement(optimizer_init)
            optimizer_res = optimizer.get_optimizer_placement(optimizer_init, placement)  # 根据指定的placement

        # 对于Trione测试
        # optimizer_res['jcsproxy_bucket_name_list']['aliyun-shenzhen'] = optimizer_res['jcsproxy_bucket_name_list']['aliyun-beijing']

        # 2.纠删码分块，上传到多个云
        cloud_operate_res_list, cloud_operate_time_list, cloud_block_path_dict, block_size = \
            self.put_file_to_cloud(optimizer_res, cloud_file_key, local_file_path)
        # 3.插入文件元信息
        file_info = self.build_file_info(cloud_file_key, local_file_path)
        file_info['optimizer_res'] = optimizer_res
        file_info['cloud_block_path_dict'] = cloud_block_path_dict
        file_info['block_size'] = block_size
        create_file_info_res = MetadataFileInfo().create_file_info(cloud_file_key, file_info, cover)

        # 4.插入数据操作信息
        datalog_info = self.build_datalog_info(file_info, file_operate, user_name)
        insert_datalog_res = DatalogUsedTraffic().insert(datalog_info)

        # 返回信息
        dict_res = GetDictRes().get_dict_res()
        dict_res["result"]["file_operate"] = file_operate
        dict_res["result"]["file_info"] = file_info
        dict_res["result"]["cloud_operate_res"] = cloud_operate_res_list
        dict_res["result"]["cloud_operate_time_res"] = cloud_operate_time_list
        return dict_res


    def print_put_file_res(self, dict_res):
        print ""
        print "print put file dict_res[]:"
        print 'status', dict_res['status']
        for key in dict_res['result']:
            print key, dict_res['result'][key]

        print ""
        print "dict_res['result']['file_info']"
        for key in dict_res['result']['file_info']:
            print key, dict_res['result']['file_info'][key]

        print ""
        print "dict_res['result']['file_info']['optimizer_res']"
        for key in dict_res['result']['file_info']['optimizer_res']:
            print key, dict_res['result']['file_info']['optimizer_res'][key]



    def get_file_md5(self, local_file_path):
        """
        获得文件的md5值
        :param local_path: 
        :return: 
        """
        fp = open(local_file_path, 'rb')
        data = fp.read()
        hash_md5 = hashlib.md5(data)
        file_md5 = hash_md5.hexdigest()
        fp.close()
        return file_md5

    def put_file_to_cloud(self, optimizer_res, cloud_file_key, local_file_path):
        """
        将文件纠删码分块，上传到几个云地域
        :param optimizer_res:
        :param cloud_file_key:
        :param local_file_path:
        :return:
        """
        bucket_name_list = optimizer_res['bucket_name_list']
        fault_tolerance_features = optimizer_res['fault_tolerance_features']

        # 纠删码分块
        ec_zfec = ErasureCodeZfec()
        dst_path = local_file_path
        ec_zfec.split_file(local_file_path, dst_path,
                           fault_tolerance_features['erasure_code_n'], fault_tolerance_features['erasure_code_k'])

        # # n个纠删码分块文件名
        # local_block_path_list = []
        # cloud_block_path_list = []
        # for i in range(fault_tolerance_features['erasure_code_n']):
        #     if fault_tolerance_features['erasure_code_n'] > 9 and i <= 9:
        #         block_suffix = '.0' + str(i) + '_' + str(fault_tolerance_features['erasure_code_n']) + '.fec'  # 纠删码块后缀
        #     else:
        #         block_suffix = '.' + str(i) + '_' + str(fault_tolerance_features['erasure_code_n']) + '.fec'
        #     local_block_path_list.append(local_file_path.encode('utf-8') + block_suffix)
        #     cloud_block_path_list.append(cloud_file_key.encode('utf-8') + block_suffix)  # block纠删码块名字也可以是唯一id
        # n个纠删码分块文件名，dict与bucket_name对应
        local_block_path_dict = {}
        cloud_block_path_dict = {}
        for i in range(fault_tolerance_features['erasure_code_n']):
            if fault_tolerance_features['erasure_code_n'] > 9 and i <= 9:
                block_suffix = '.0' + str(i) + '_' + str(fault_tolerance_features['erasure_code_n']) + '.fec'  # 纠删码块后缀
            else:
                block_suffix = '.' + str(i) + '_' + str(fault_tolerance_features['erasure_code_n']) + '.fec'
            bucket_name = bucket_name_list[i]
            local_block_path_dict[bucket_name] = local_file_path.encode('utf-8') + block_suffix
            cloud_block_path_dict[bucket_name] = cloud_file_key.encode('utf-8') + block_suffix  # block纠删码块名字也可以是唯一id

        # 依次上传到云，并发上传
        cloud_operate_res_list = []
        put_file_time_list = []
        threads = []
        for bucket_name in bucket_name_list:
            cloud_account = CloudInformation().get_cloud_account_from_bucket_name(bucket_name)
            cloud_operate = CloudInterface(cloud_account)
            # 依次上传
            # put_file_res, put_file_time = GetFuncTime().get_func_time(cloud_operate.put_file,
            #                                                 (cloud_block_path_list[i], local_block_path_list[i]))
            # cloud_operate_res_list.append(put_file_res)
            # put_file_time_list.append(put_file_time)
            # 多线程并发上传
            thread_one = MyThread(GetFuncTime().get_func_time,
                                  (cloud_operate.put_file, (cloud_block_path_dict[bucket_name],
                                                            local_block_path_dict[bucket_name])))
            threads.append(thread_one)
        for i in range((len(bucket_name_list))):
            threads[i].start()
        for i in range((len(bucket_name_list))):
            threads[i].join()
        for i in range((len(bucket_name_list))):
            put_file_res, put_file_time = threads[i].getResult()
            cloud_operate_res_list.append(put_file_res)
            put_file_time_list.append(put_file_time)

        block_size = os.path.getsize(local_block_path_dict[bucket_name_list[0]])
        block_size /= (1024.0 * 1024.0)
        # 删除纠删码块
        # for local_block_path in local_block_path_list:
        #     os.remove(local_block_path)
        for local_block_path in local_block_path_dict.itervalues():
            os.remove(local_block_path)
        return cloud_operate_res_list, put_file_time_list, cloud_block_path_dict, block_size

    def build_file_info(self, cloud_file_key, local_file_path):
        file_key = cloud_file_key
        file_size = os.path.getsize(local_file_path)
        file_size /= (1024.0 * 1024.0)
        file_md5 = self.get_file_md5(local_file_path)
        file_ctime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_info = {}
        file_info['file_key'] = file_key
        file_info['file_size'] = file_size
        file_info['file_md5'] = file_md5
        file_info['file_ctime'] = file_ctime
        return file_info

    def build_datalog_info(self, file_info, file_operage, user_name):
        datalog_info = {}
        datalog_info['file_ctime'] = file_info['file_ctime']
        datalog_info['file_key'] = file_info['file_key']
        datalog_info['file_md5'] = file_info['file_md5']
        datalog_info['file_size'] = file_info['file_size']
        datalog_info['block_size'] = file_info['block_size']
        datalog_info['file_operate'] = file_operage
        datalog_info['jcsproxy_area'] = self.jcsproxy_area
        datalog_info['bucket_name_list'] = file_info['optimizer_res']['bucket_name_list']  # 上传是n个，下载是k个
        datalog_info['user_name'] = user_name
        datalog_info['timestamp'] = datetime.datetime.now()
        return datalog_info



if __name__ == '__main__':
    print("manage operate")
    manager_put_file = PutFile()

    # print "上传文件，不设置配置参数"
    # user_name = "liuyf"
    # cloud_file_path = "测试文件.txt"
    # local_file_path = os.path.join(CONFIG["test_file_path"], "test_16")
    #
    # res = manager_put_file.put_file(user_name, cloud_file_path, local_file_path, cover=True)
    # print(res)
    # print manager_put_file.print_put_file_res(res)



    print "上传文件，设置配置参数"
    user_name = "liuyf"
    cloud_file_path = u"测试文件2.txt"
    local_file_path = os.path.join(CONFIG["test_file_path"], "test_32")

    jcsproxy_request_features = {
        'aliyun-beijing': 1000,
        'aliyun-shanghai': 0,
        'aliyun-shenzhen': 300,
    }
    file_size = 32
    storage_time = 1

    target_weights = {}  # 优化目标权重
    target_weights['storage_cost_weight'] = 0.5
    target_weights['latency_time_weight'] = 1 - target_weights['storage_cost_weight']

    res = manager_put_file.put_file(user_name, cloud_file_path, local_file_path, True,
                                    storage_time, jcsproxy_request_features, None, target_weights)
    print(res)
    print manager_put_file.print_put_file_res(res)








