# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/6/12 16:37'

from elasticsearch import Elasticsearch
from tools.get_dict_res import GetDictRes
import json
import datetime
from config.configuration import SERVER


class DatalogMonitor(object):
    def __init__(self):
        self.es = Elasticsearch(SERVER["host"]+":9200")  # 设置 host，port
        # self.es = Elasticsearch()
        self.index = "jcsproxy_index"
        self.doc_type = "jcsproxy_type"

    def count_download_file(self, start_time, end_time, file_key=None):
        """
        聚合timedelta_days天以内的，file_key，jcsproxy_ara，get_file次数
        :param timedelta_days:
        :return:
        """
        body_aggs = {
            "size": 0,
            "aggs": {
                "file_key":{
                    "terms":{
                        "field": "file_key.keyword"
                    },
                    "aggs":{
                        "jcsproxy_area":{
                            "terms":{
                                "field": "jcsproxy_area.keyword"
                            }
                        }
                    }
                }
            }
        }
        # gt_time = time_end-datetime.timedelta(days=timedelta_days)  # 查询几天以内的
        body_query = {
            "query": {
                "constant_score": {  # 它将一个不变的常量评分应用于所有匹配的文档。它被经常用于你只需要执行一个 filter 而没有其它查询的情况下
                    "filter": {   # 过滤器，执行速度块，不会计算相关度（直接跳过了整个评分阶段）而且很容易被缓存
                        "bool":{
                            "must": [{
                                "range": {
                                    "timestamp": {
                                        #  "gt": "now-5d"
                                        #"  gt": "2018-06-30T21:26:38"
                                        # "gt": gt_time
                                        "gt": start_time,
                                        "lt": end_time,
                                    }
                                }
                            },
                            {
                                "term": {
                                    "file_operate.keyword": "get_file"
                                }
                            }]
                        }
                    }
                }
            }
        }
        if not file_key == None:
            update_file_key={
                "term":{
                    "file_key.keyword": file_key
                }
            }
            body_query['query']['constant_score']['filter']['bool']['must'].append(update_file_key)
        body = {}
        body.update(body_query)
        body.update(body_aggs)

        # 聚合计数
        self.es.indices.refresh(index=self.index)
        res = self.es.search(index=self.index, doc_type=self.doc_type, body=body)

        # 提取返回结果
        file_key_res_dict = {}
        file_key_res = res['aggregations']['file_key']['buckets']
        for file_key_one in file_key_res:
            file_key = file_key_one['key']
            file_key_res_dict[file_key] = {}
            jcsproxy_area_res = file_key_one['jcsproxy_area']['buckets']
            for jcsproxy_area_one in jcsproxy_area_res:
                jcsproxy_area = jcsproxy_area_one['key']
                file_key_res_dict[file_key][jcsproxy_area] = jcsproxy_area_one['doc_count']
        # res_dict = {}
        # res_dict['file_key'] = file_key_res_dict
        res_dict = file_key_res_dict
        return res_dict


    def test(self, file_key):
        body = {
            "query": {
                "match": {
                    "file_key.keyword": file_key
                }
            }
        }
        res = self.es.search(index=self.index, doc_type=self.doc_type)
        res = self.es.search(index=self.index, doc_type=self.doc_type, body=body)
        return res


if __name__ == '__main__':
    data_monitor = DatalogMonitor()

    start_time = datetime.datetime.now()-datetime.timedelta(days=1)
    end_time = datetime.datetime.now()
    print 'start_time', start_time
    print 'end_time', end_time
    res = data_monitor.count_download_file(start_time, end_time)
    print res

    # now = datetime.datetime.now()
    # start_time = datetime.datetime(now.year, now.month, 1)
    # end_time = datetime.datetime(now.year, now.month+1, 1)-datetime.timedelta(days=1)
    start_time = datetime.datetime.now()-datetime.timedelta(days=30)
    end_time = datetime.datetime.now()
    print 'start_time', start_time
    print 'end_time', end_time
    res = data_monitor.count_download_file(start_time, end_time)
    print res

    print "\nfile_key"
    start_time = datetime.datetime.now()-datetime.timedelta(days=30)
    end_time = datetime.datetime.now()
    print 'start_time', start_time
    print 'end_time', end_time
    res = data_monitor.count_download_file(start_time, end_time, file_key="liuyf_test/remote.txt")
    print res
    res = data_monitor.count_download_file(start_time, end_time, file_key="liuyf_test/remote.txt1")
    print res