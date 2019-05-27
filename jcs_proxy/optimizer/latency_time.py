# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/5/1 22:34'

from config.configuration import CONFIG
from config.cloud_information import CloudInformation
import os
import json

class LatencyTime(object):
    def __init__(self):
        self.program_path = CONFIG['program_path']

    def get_latency_time_list(self, jcsproxy_area):
        """
        取得此jcsproxy_area到每个云地域cloud_bucket_list的延迟测试值
        :param jcsproxy_area: "aliyun-beijing", "aliyun-shanghai", "aliyun-shenzhen"等
        :return:
        """
        latency_time_path = self.program_path+"/optimizer/latency_time_" + jcsproxy_area + ".json"
        fp = open(latency_time_path, "r")
        latency_time_str = fp.read()
        fp.close()
        latency_time_all = json.loads(latency_time_str)
        # 只取cloud_bucket_list中的latency_time值
        cloud_bucket_list = CloudInformation().get_cloud_bucket_list()
        latency_time_list = []
        for cloud_bucket in cloud_bucket_list:
            bucket_name = cloud_bucket['bucket_name']
            for latency_time_one in latency_time_all:
                if latency_time_one['bucket_name'] == bucket_name:
                    latency_time_list.append(latency_time_one)
                    break
        return latency_time_list

    def get_latency_time_sort(self, jcsproxy_area):
        """
        对latency_time_list进行排序
        :param jcsproxy_area:
        :return:
        """
        latency_time_list = self.get_latency_time_list(jcsproxy_area)
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
        return latency_time_list

    def myprintlist(self, mylist, mylist_name=""):
        print mylist_name
        for one in mylist:
            print one

    def myprintlist2(self, mylist, mylist_name=""):
        print mylist_name
        print mylist[0]['jcsproxy_area']
        for one in mylist:
            print one['latency_time'], one['bucket_name']

if __name__ == '__main__':
    latency_time = LatencyTime()

    jcsproxy_area = "aliyun-beijing"
    latency_time_list = latency_time.get_latency_time_list(jcsproxy_area)
    latency_time.myprintlist(latency_time_list, "latency time list")
    latency_time_sort_list = latency_time.get_latency_time_sort(jcsproxy_area)
    latency_time.myprintlist(latency_time_sort_list, "latency time list")
    latency_time.myprintlist2(latency_time_sort_list, "latency time list")
    print ""

    jcsproxy_area = "aliyun-shanghai"
    latency_time_list = latency_time.get_latency_time_list(jcsproxy_area)
    latency_time.myprintlist(latency_time_list, "latency time list")
    latency_time_sort_list = latency_time.get_latency_time_sort(jcsproxy_area)
    latency_time.myprintlist(latency_time_sort_list, "latency time list")
    latency_time.myprintlist2(latency_time_sort_list, "latency time list")
    print ""

    jcsproxy_area = "aliyun-shenzhen"
    latency_time_list = latency_time.get_latency_time_list(jcsproxy_area)
    latency_time.myprintlist(latency_time_list, "latency time list")
    latency_time_sort_list = latency_time.get_latency_time_sort(jcsproxy_area)
    latency_time.myprintlist(latency_time_sort_list, "latency time list")
    latency_time.myprintlist2(latency_time_sort_list, "latency time list")
    print ""
