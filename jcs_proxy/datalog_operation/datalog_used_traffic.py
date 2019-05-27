# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/5/30 16:45'

from elasticsearch import Elasticsearch
from tools.get_dict_res import GetDictRes
from config.configuration import SERVER

class DatalogUsedTraffic(object):
    # 将数据操作信息 插入ES中
    def __init__(self):
        self.es = Elasticsearch(SERVER["host"]+":9200")
        # self.es = Elasticsearch()
        self.index = "jcsproxy_index"
        self.doc_type = "jcsproxy_type"

    def insert(self, doc):
        # 插入日志doc到ES
        return self.es.index(index=self.index, doc_type=self.doc_type, body=doc)

    def get(self):
        # 得到ES中的部分日志
        self.es.indices.refresh(index=self.index)
        res = self.es.search(index=self.index, doc_type=self.doc_type, body={"query": {"match_all": {}}})
        return res

    # def count(self):
    #     body = {
    #         "size" : 0,
    #         "aggs":{
    #             "used_traffic":{
    #                 "sum":{
    #                     "field": "file_size"
    #                 }
    #             }
    #         }
    #     }
    # body = {
    #     "size" : 0,
    #     "aggs":{
    #         "jcsproxy_area":{
    #             "terms":{
    #                 "field": "jcsproxy_area.keyword"
    #             },
    #         }
    #     }
    # }
    # body = {
    #     "size" : 0,
    #     "aggs":{
    #         "bucket_list":{
    #             "terms":{
    #                 "field": "bucket_name_list.keyword"
    #             },
    #         }
    #     }
    # }
    #     return self.es.search(index=self.index, doc_type=self.doc_type, body=body)

    ######################################################################################

    def count_jcsproxy_used_traffic(self, query=None):
        """
        每个jcsproxy上传下载流量
        :return:
        """
        # 聚合语句
        body = {
            "size" : 0,
            "aggs":{
                "jcsproxy_area":{
                    "terms":{
                        "field": "jcsproxy_area.keyword"
                    },
                    "aggs":{
                        "file_operate":{
                            "terms":{
                                "field": "file_operate.keyword"
                            },
                            "aggs":{
                                "jcsproxy_used_traffic":{
                                    "sum":{
                                        "field": "file_size"
                                    }
                                }
                            },
                        }
                    }
                }
            }
        }
        if query != None:
            body['query'] = query

        # 聚合计数
        self.es.indices.refresh(index=self.index)
        res = self.es.search(index=self.index, doc_type=self.doc_type, body=body)

        # 提取返回结果
        # print res['aggregations']['jcsproxy_area']['buckets'][0]['file_operate']['buckets'][0]['jcsproxy_used_traffic'][ 'value']
        jcsproxy_area_res_dict = {}
        jcsproxy_area_res = res['aggregations']['jcsproxy_area']['buckets']
        for jcsproxy_area_one in jcsproxy_area_res:
            jcsproxy_area_key = jcsproxy_area_one['key']
            jcsproxy_area_res_dict[jcsproxy_area_key] = {}
            file_operate_res = jcsproxy_area_one['file_operate']['buckets']
            for file_operate_one in file_operate_res:
                file_operate_key = file_operate_one['key']
                jcsproxy_area_res_dict[jcsproxy_area_key][file_operate_key] = file_operate_one['jcsproxy_used_traffic']['value']
        res_dict = {}
        res_dict['jcsproxy_area'] = jcsproxy_area_res_dict
        return res_dict

    def count_jcsproxy_bucket_used_traffic(self, query=None):
        """
        每个jcsproxy 和每个云地域之间的上传下载流量
        :return:
        """
        body = {
            "size" : 0,
            "aggs":{
                "jcsproxy_area":{
                    "terms":{
                        "field": "jcsproxy_area.keyword"
                    },
                    "aggs":{
                        "file_operate":{
                            "terms":{
                                "field": "file_operate.keyword"
                            },
                            "aggs":{
                                "bucket_name_list": {
                                    "terms":{
                                        "field": "bucket_name_list.keyword"
                                    },
                                    "aggs":{
                                        "jcsproxy_bucket_used_traffic": {
                                            "sum": {
                                                "field": "block_size"
                                            }
                                        }
                                    }
                                },
                            }
                        }
                    }
                }
            }
        }
        if query != None:
            body['query'] = query
        self.es.indices.refresh(index=self.index)
        res = self.es.search(index=self.index, doc_type=self.doc_type, body=body)

        # print res['aggregations']['jcsproxy_area']['buckets'][0]['file_operate']['buckets'][0]['bucket_name_list'] \
        #            ['buckets'][0]['jcsproxy_bucket_used_traffic']['value']
        jcsproxy_area_res_dict = {}
        jcsproxy_area_res = res['aggregations']['jcsproxy_area']['buckets']
        for jcsproxy_area_one in jcsproxy_area_res:
            jcsproxy_area_key = jcsproxy_area_one['key']
            jcsproxy_area_res_dict[jcsproxy_area_key] = {}
            file_operate_res = jcsproxy_area_one['file_operate']['buckets']
            for file_operate_one in file_operate_res:
                file_operate_key = file_operate_one['key']
                jcsproxy_area_res_dict[jcsproxy_area_key][file_operate_key] = {}
                bucket_name_list_res = file_operate_one['bucket_name_list']['buckets']
                for bucket_name_list_one in bucket_name_list_res:
                    bucket_name_key = bucket_name_list_one['key']
                    value = bucket_name_list_one['jcsproxy_bucket_used_traffic']['value']
                    jcsproxy_area_res_dict[jcsproxy_area_key][file_operate_key][bucket_name_key] = value
        res_dict = {}
        res_dict['jcsproxy_area'] = jcsproxy_area_res_dict
        return res_dict

    ##############################################################

    def count_jcsproxy_used_traffic_file(self, file_key):
        """
        某个文件的上传下载流量
        :param file_key:
        :return:
        """
        query = {
            "match": {
                "file_key.keyword": file_key
            }
        }
        res_dict = self.count_jcsproxy_used_traffic(query)
        res_dict['file_key'] = file_key
        return res_dict

    def count_jcsproxy_bucket_used_traffic_file(self, file_key):
        query = {
            "match": {
                "file_key.keyword": file_key
            }
        }
        res_dict = self.count_jcsproxy_bucket_used_traffic(query)
        res_dict['file_key'] = file_key
        return res_dict

    #######################################################################


    def count_jcsproxy_used_traffic_user(self, user_name):
        """
        某个用户的上传下载流量
        :param file_key:
        :return:
        """
        query = {
            "match": {
                "user_name.keyword": user_name
            }
        }
        res_dict = self.count_jcsproxy_used_traffic(query)
        res_dict['user_name'] = user_name
        return res_dict

    def count_jcsproxy_bucket_used_traffic_user(self, user_name):
        query = {
            "match": {
                "user_name.keyword": user_name
            }
        }
        res_dict = self.count_jcsproxy_bucket_used_traffic(query)
        res_dict['user_name'] = user_name
        return res_dict


    ###########################################################################

    def test(self, file_key):
        body = {
            "query": {
                "match": {
                    "file_key.keyword": file_key
                }
            }
        }
        # res = self.es.search(index=self.index, doc_type=self.doc_type)
        res = self.es.search(index=self.index, doc_type=self.doc_type, body=body)
        return res


    def delete_all(self):
        # 删除所有日志
        dict_res = GetDictRes().get_dict_res()
        try:
            self.es.indices.delete(index=self.index)
        except:
            dict_res['status'] = 1
            dict_res['result'] = "no such index"
        return dict_res

