# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/1/17 14:59'


import os
from cloud_interface.cloud_interface import CloudInterface
from metadata.file_info import MetadataFileInfo
from tools.get_func_time import GetFuncTime
from tools.get_dict_res import GetDictRes
from config.cloud_information import CloudInformation
from optimizer.erasure_code_zfec import ErasureCodeZfec
from config.configuration import CONFIG
from datalog_operation.datalog_used_traffic import DatalogUsedTraffic
from tools.MyThread import MyThread
import datetime
from optimizer.optimizer_init import OptimizerInit
from optimizer.optimizer_replacement import OptimizerReplacement

class GetFile(object):
    """
    下载文件操作
    """
    def __init__(self):
        self.jcsproxy_area = CONFIG['jcsproxy_area']


    # def get_url(self, user_name, cloud_file_path):
    #     """
    #     下载文件（得到云端文件url链接）
    #     :param user_name: str, 用户名
    #     :param cloud_file_path: str, 云端文件路径
    #     :return: dict_res
    #     """
    #     cloud_file_key = user_name + "/" + cloud_file_path
    #     # 1.获取文件元信息
    #     metadata_file_info = MetadataFileInfo()
    #     file_info = metadata_file_info.get_file_info(cloud_file_key)["result"]
    #     # 2.获取文件下载策略
    #     cloud_bucket = OptimizerPolicy().get_file_policy()
    #     metadata_cloud_info = MetadataCloudInfo()
    #     cloud_info = metadata_cloud_info.get_cloud_info(cloud_bucket["cloud_name"],
    #                                                     cloud_bucket["bucket_name"])["result"]
    #     # 3.获得云端文件url链接
    #     cloud_operate = CloudInterface(cloud_info)
    #     cloud_operate_res, cloud_operate_time = GetFuncTime().get_func_time(cloud_operate.get_url, (cloud_file_key, ))
    #     # 4.插入数据操作记录
    #     datalog_info = PutFileManager().build_datalog_info(cloud_file_key, "get_url",
    #                                                        cloud_bucket, cloud_operate_time, self.proxy_name)
    #     insert_datalog_res = DataLog().insert_operdata(datalog_info)
    #     # 返回信息
    #     dict_res = GetDictRes().get_dict_res()
    #     dict_res["result"]["file_operate"] = "get_url"
    #     dict_res["result"]["cloud_operate_res"] = cloud_operate_res
    #     dict_res["result"]["file_info"] = file_info
    #     dict_res["result"]["datalog_info"] = datalog_info
    #     return dict_res

    def get_file(self, user_name, cloud_file_path, local_file_path):
        """
        下载文件（云端到本地）
        :param user_name: str, 用户名
        :param cloud_file_path: str, 云端文件路径
        :param local_file_path: str, 本地文件路径
        :return: dict_res
        """
        file_operate = "get_file"
        cloud_file_key = user_name + "/" + cloud_file_path
        # 1.获取用户文件信息
        metadata_file_info = MetadataFileInfo()
        file_info = metadata_file_info.get_file_info(cloud_file_key)["result"]
        # 3.下载纠删码块到本地，合并纠删码块
        cloud_operate_res_list, cloud_operate_time_list, download_bucket_name_list = \
            self.get_file_from_cloud(file_info, local_file_path)
        # # 4.插入数据操作记录
        datalog_info = self.build_datalog_info(file_info, file_operate, download_bucket_name_list, user_name)
        insert_datalog_res = DatalogUsedTraffic().insert(datalog_info)
        # 返回信息
        dict_res = GetDictRes().get_dict_res()
        dict_res["result"]["file_operate"] = file_operate
        dict_res["result"]["file_info"] = file_info
        dict_res["result"]["download_bucket_name_list"] = download_bucket_name_list
        dict_res["result"]["cloud_operate_res"] = cloud_operate_res_list
        dict_res["result"]["cloud_operate_time_res"] = cloud_operate_time_list
        return dict_res

    def get_file_name(self, cloud_file_key):
        file_split = str.split(cloud_file_key.encode('utf-8'), "/")
        return file_split[len(file_split)-1]

    def get_file_dir(self, cloud_file_key):
        file_split = str.split(cloud_file_key.encode('utf-8'), "/")
        file_dir = '/'
        for i in range(len(file_split) - 1):
            file_dir = os.path.join(file_dir, file_split[i])
        return file_dir

    def check_avalible_bucket_list(self, download_bucket_name_list, opt_bucket_name_list, optimizer_res):
        # 考虑某些云故障不能下载，从后面选择云替换下载。以后改成重新计算下载策略
        cloud_bucket_name_list = CloudInformation().get_cloud_bucket_name_list()
        erasure_code_k = len(download_bucket_name_list)
        cloud_fault_list = []
        for bucket_name in download_bucket_name_list:  # 找到不可用的bucket_name
            if bucket_name not in cloud_bucket_name_list:
                cloud_fault_list.append(bucket_name)
        if len(cloud_fault_list) == 0:
            return download_bucket_name_list

        # for bucket_name in cloud_fault_list:  # 删除不可用的bucket_name
        #     download_bucket_name_list.remove(bucket_name)
        # for bucket_name in opt_bucket_name_list:  # 新增可用的bucket_name
        #     if len(download_bucket_name_list) == erasure_code_k:
        #         break
        #     if bucket_name not in download_bucket_name_list \
        #         and bucket_name in cloud_bucket_name_list:
        #         download_bucket_name_list.append(bucket_name)

        # 重新计算数据下载方案
        jcsproxy_request_features = optimizer_res['jcsproxy_request_features']
        jcsproxy_storage_features = optimizer_res['jcsproxy_storage_features']
        jcsproxy_area_list = ["aliyun-beijing", "aliyun-shanghai", "aliyunshenzhen"]
        one_area_features = {}
        for jcsproxy_area in jcsproxy_area_list:
            if jcsproxy_area in jcsproxy_storage_features.keys():
                one_area_features = jcsproxy_storage_features[jcsproxy_area]
                break
        file_size = one_area_features['storage_size']
        storage_time = one_area_features['storage_time']
        fault_tolerance_features = optimizer_res['fault_tolerance_features']
        target_weights = optimizer_res['target_weights']
        optimizer_init = OptimizerInit(file_size, storage_time, jcsproxy_request_features,
                                       fault_tolerance_features, target_weights)
        placement = []
        for bucket_name in opt_bucket_name_list:
            if bucket_name in cloud_bucket_name_list:
                placement.append(cloud_bucket_name_list.index(bucket_name))
        res_info = OptimizerReplacement().optimizer_placement_info(optimizer_init, placement)  # 重新计算下载方案
        jcsproxy_placement = res_info['jcsproxy_placement_nk'][CONFIG['jcsproxy_area']]
        download_bucket_name_list = OptimizerReplacement().get_placement_bucket_name_list(jcsproxy_placement, optimizer_init.cloud_bucket_list)

        print "重新计算下载策略"
        print CONFIG['jcsproxy_area']
        print 'download_bucket_name_list', download_bucket_name_list
        return download_bucket_name_list

    def get_file_from_cloud(self, file_info, local_file_path):
        cloud_block_path_dict = file_info['cloud_block_path_dict']
        optimizer_res = file_info['optimizer_res']
        erasure_code_k = optimizer_res['fault_tolerance_features']['erasure_code_k']
        opt_bucket_name_list = optimizer_res['bucket_name_list']
        print "optimizer_res['jcsproxy_bucket_name_list']", optimizer_res['jcsproxy_bucket_name_list']
        print " optimizer_res['bucket_name_list']",  optimizer_res['bucket_name_list']
        print "file_info", file_info
        if optimizer_res['jcsproxy_bucket_name_list'].has_key(self.jcsproxy_area):
            download_bucket_name_list = optimizer_res['jcsproxy_bucket_name_list'][self.jcsproxy_area]
        else:  # 某地区没有下载策略，则取前k个云下载。以后改成重新计算下载策略
            download_bucket_name_list = optimizer_res['bucket_name_list'][:erasure_code_k]

        # 考虑某些云故障不能下载，从后面选择云替换下载。以后改成重新计算下载策略
        download_bucket_name_list = self.check_avalible_bucket_list(download_bucket_name_list, opt_bucket_name_list, optimizer_res)

        # k个纠删码块存储在本地的临时路径
        download_local_block_path_list = []
        download_cloud_block_path_list = []
        local_file_dir = self.get_file_dir(local_file_path)
        for bucket_name in download_bucket_name_list:
            block_name = self.get_file_name(cloud_block_path_dict[bucket_name])
            local_block_path = os.path.join(local_file_dir, block_name)
            download_local_block_path_list.append(local_block_path)
            download_cloud_block_path_list.append(cloud_block_path_dict[bucket_name])
        # k个纠删码块存储在本地的临时路径,dict与bucket_name对应
        # download_local_block_path_dict = {}
        # download_cloud_block_path_dict = {}
        # local_file_dir = self.get_file_dir(local_file_path)
        # for bucket_name in download_bucket_name_list:
        #     block_name = self.get_file_name(cloud_block_path_dict[bucket_name])
        #     local_block_path = os.path.join(local_file_dir, block_name)
        #     download_local_block_path_dict[bucket_name] = local_block_path
        #     download_cloud_block_path_dict[bucket_name] = cloud_block_path_dict[bucket_name]

        # 从云上下载k个纠删码块，并发下载
        cloud_operate_res_list = []
        get_file_time_list = []
        threads = []
        for i, bucket_name in enumerate(download_bucket_name_list):
            cloud_account = CloudInformation().get_cloud_account_from_bucket_name(bucket_name)
            cloud_operate = CloudInterface(cloud_account)
            # 依次下载
            # get_file_res, get_file_time = GetFuncTime().get_func_time(cloud_operate.get_file,
            #                                             (download_cloud_block_path_list[i], download_local_block_path_list[i]))
            # cloud_operate_res_list.append(get_file_res)
            # get_file_time_list.append(get_file_time)
            # 多线程并发下载
            thread_one = MyThread(GetFuncTime().get_func_time,
                                  (cloud_operate.get_file, (download_cloud_block_path_list[i],
                                                            download_local_block_path_list[i])))
            threads.append(thread_one)
        for i in range(erasure_code_k):
            threads[i].start()
        for i in range(erasure_code_k):
            threads[i].join()
        for i in range(erasure_code_k):
            get_file_res, get_file_time = threads[i].getResult()
            cloud_operate_res_list.append(get_file_res)
            get_file_time_list.append(get_file_time)

        # 合并纠删码块
        ec_zfec = ErasureCodeZfec()
        print "download_local_block_path_list", download_local_block_path_list
        print "local_file_path", local_file_path
        ec_zfec.merge_blocks(download_local_block_path_list, local_file_path)

        # 删除纠删码块
        for local_block_path in download_local_block_path_list:
            os.remove(local_block_path)

        return cloud_operate_res_list, get_file_time_list, download_bucket_name_list


    def build_datalog_info(self, file_info, file_operage, download_bucket_name_list, user_name):
        datalog_info = {}
        datalog_info['file_ctime'] = file_info['file_ctime']
        datalog_info['file_key'] = file_info['file_key']
        datalog_info['file_md5'] = file_info['file_md5']
        datalog_info['file_size'] = file_info['file_size']
        datalog_info['block_size'] = file_info['block_size']
        datalog_info['file_operate'] = file_operage
        datalog_info['jcsproxy_area'] = self.jcsproxy_area
        datalog_info['bucket_name_list'] = download_bucket_name_list  # 上传是n个，下载是k个
        datalog_info['user_name'] = user_name
        datalog_info['timestamp'] = datetime.datetime.now()
        return datalog_info

if __name__ == '__main__':
    print("manage get file")
    manager_get_file = GetFile()

    user_name = "liuyf_test"
    cloud_file_path = "dir/remote.txt"
    local_file_path = os.path.join(CONFIG["test_file_path"], "test.txt")

    # print("manager get url")
    # res = manager_get_file.get_url(user_name, cloud_file_path)
    # print(res)

    print("manager get file")
    res = manager_get_file.get_file(user_name, cloud_file_path, local_file_path)
    print(res)
