# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/5/22 14:13'

from latency_time import LatencyTime
from config.cloud_information import CloudInformation

class JcsproxyLatencyTime(object):
    def __init__(self):
        pass

    def get_jcsproxy_latency_time_list(self, jcsproxy_area_list):
        """
        取得每个jcsproxy的latency_time_list
        :param jcsproxy_area_list:
        :return:
        """
        jcsproxy_latency_time_list = {}
        for jcsproxy_area in jcsproxy_area_list:
            latency_time_list = LatencyTime().get_latency_time_list(jcsproxy_area)
            jcsproxy_latency_time_list[jcsproxy_area] = latency_time_list
        return jcsproxy_latency_time_list

    def get_jcsproxy_latency_time_sort(self, jcsproxy_area_list):
        """
        取得每个jcsproxy的latency_time_sort
        :param jcsproxy_area_list:
        :return:
        """
        jcsproxy_latency_time_sort = {}
        for jcsproxy_area in jcsproxy_area_list:
            latency_time_sort = LatencyTime().get_latency_time_sort(jcsproxy_area)
            latency_time_sort = self.get_cloud_bucket_index(latency_time_sort)
            jcsproxy_latency_time_sort[jcsproxy_area] = latency_time_sort
        # jcsproxy_latency_time_sort = self.get_jcsproxy_sort_num(jcsproxy_latency_time_sort, jcsproxy_area_list)
        return jcsproxy_latency_time_sort

    ############################################################################################

    def get_latency_time_weights_sum_list(self, jcsproxy_area_list, jcsproxy_request_weights):
        """
        每个bucket在多个jcsproxy中延迟权值和
        :param jcsproxy_area_list:
        :param jcsproxy_request_weights:
        :return:
        """
        cloud_bucket_list = CloudInformation().get_cloud_bucket_list()
        jcsproxy_latency_time = self.get_jcsproxy_latency_time_list(jcsproxy_area_list)
        latency_time_weights_sum_list = []
        for i in range(len(cloud_bucket_list)):
            latency_time_weights_sum = 0
            for jcsproxy_area in jcsproxy_area_list:
                latency_time_weights_sum += jcsproxy_latency_time[jcsproxy_area][i]['latency_time'] * \
                                       jcsproxy_request_weights[jcsproxy_area]
            res_one = {}
            res_one['bucket_name'] = cloud_bucket_list[i]['bucket_name']
            res_one['latency_time'] = latency_time_weights_sum
            latency_time_weights_sum_list.append(res_one)
        return latency_time_weights_sum_list

    def get_latency_time_weights_sum_sort(self, jcsproxy_area_list, jcsproxy_request_weights):
        latency_time_list = self.get_latency_time_weights_sum_list(jcsproxy_area_list, jcsproxy_request_weights)
        latency_time_list_len = len(latency_time_list)
        for i in range(0, latency_time_list_len):  # 按latency_time 排序
            min_index = i
            for j in range(i, latency_time_list_len):
                if latency_time_list[j]['latency_time'] < latency_time_list[min_index]['latency_time']:
                    min_index = j
            if min_index != i:
                t = latency_time_list[i]
                latency_time_list[i] = latency_time_list[min_index]
                latency_time_list[min_index] = t

        latency_time_list = self.get_cloud_bucket_index(latency_time_list)
        return latency_time_list


    #############################################################################################

    def get_cloud_bucket_index(self, area_sort):
        # 根据area_sort中的bucket_name，添加对应的cloud_bucket_index
        cloud_bucket_list = CloudInformation().get_cloud_bucket_list()
        for area_sort_one in area_sort:
            for cloud_bucket in cloud_bucket_list:
                if cloud_bucket['bucket_name'] == area_sort_one['bucket_name']:
                    cloud_bucket_index = cloud_bucket_list.index(cloud_bucket)
                    area_sort_one['cloud_bucket_index'] = cloud_bucket_index
                    break
        return area_sort

    def myprintdict(self, mydict, mydict_name):
        print mydict_name
        for key in mydict:
            print key, mydict[key]

    def myprintlist(self, mylist, mylist_name):
        print mylist_name
        for one in mylist:
            print one


if __name__ == '__main__':
    jcsproxy_area_list = ["aliyun-beijing", "aliyun-shenzhen"]
    # jcsproxy_request_features
    jcsproxy_request_weights = {
        "aliyun-beijing": 0.5,
        "aliyun-shenzhen": 0.5
    }
    fault_tolerance_features = \
    {'erasure_code_k': 3, 'erasure_code_n': 5, 'fault_tolerance_level': 2}

    jcsproxy_latency_time = JcsproxyLatencyTime()
    jcsproxy_latency_time_list = jcsproxy_latency_time.get_jcsproxy_latency_time_list(jcsproxy_area_list)
    jcsproxy_latency_time.myprintdict(jcsproxy_latency_time_list, "jcsproxy_latency_time_list")
    jcsproxy_latency_time_sort = jcsproxy_latency_time.get_jcsproxy_latency_time_sort(jcsproxy_area_list)
    jcsproxy_latency_time.myprintdict(jcsproxy_latency_time_sort, "jcsproxy_latency_time_sort")
    latency_time_weights_sum_list = jcsproxy_latency_time.get_latency_time_weights_sum_list(jcsproxy_area_list, jcsproxy_request_weights)
    jcsproxy_latency_time.myprintlist(latency_time_weights_sum_list, "latency_time_weights_sum_list")
    latency_time_weights_sum_sort = jcsproxy_latency_time.get_latency_time_weights_sum_sort(jcsproxy_area_list, jcsproxy_request_weights)
    jcsproxy_latency_time.myprintlist(latency_time_weights_sum_sort, "latency_time_weights_sum_sort")

    # latency sort 输出
    print ""
    for jcsproxy_area in jcsproxy_area_list:
        area_sort = jcsproxy_latency_time_sort[jcsproxy_area]
        print jcsproxy_area
        for area_sort_one in area_sort:
            print area_sort_one['cloud_bucket_index'], ",", round(area_sort_one['latency_time'], 4)

    print ""
    for jcsproxy_area in jcsproxy_area_list:
        area_list = jcsproxy_latency_time_list[jcsproxy_area]
        print jcsproxy_area
        for area_list_one in area_list:
            print round(area_list_one['latency_time'], 4)

    for i in range(22):
        print i
