# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/5/1 15:28'

from config.cloud_information import CloudInformation

class StorageCost(object):
    def __init__(self):
        pass

    def get_storage_cost(self, storage_features, bucket_name):
        """
        计算费用
        storage_features
        :param storage_size:存储量（M）
        :param storage_time:存储时间（月）
        :param download_size:下载量（M）
        :param request_frequency:请求次数（次）
        :param cloud_bucket: 存储bucket
        :return:
        """
        storage_size = storage_features['storage_size']
        storage_time = storage_features['storage_time']
        download_size = storage_features['download_size']
        request_frequency = storage_features['request_frequency']
        cloud_price = CloudInformation().get_cloud_price_from_bucket_name(bucket_name)
        # 存储费用（低频存储有最短存储期限）
        if storage_time < cloud_price['lowmonth']:
            storage_time = cloud_price['lowmonth']
        storage_expense = cloud_price['storage'] * (storage_size/1024.0) * storage_time
        # 下载费用（低频存储有数据取回费用）
        download_expense = (cloud_price['download'] + cloud_price['retrieve']) * (download_size / 1024.0)
        # 请求次数费用
        request_expense = cloud_price['request'] * (storage_time*request_frequency/10000.0)
        sum_expense = storage_expense+download_expense+request_expense
        res = {'storage_expense': storage_expense,
                'download_expense': download_expense,
                'request_expense': request_expense,
                'sum_expense': sum_expense,
                'bucket_name': bucket_name}
        return res

    def get_storage_cost_list(self, storage_features):
        # 只计算cloud_bucket_list中的cost值
        cloud_bucket_list = CloudInformation().get_cloud_bucket_list()
        storage_cost_list =[]
        for cloud_bucket in cloud_bucket_list:
            storage_cost_list.append(self.get_storage_cost(storage_features, cloud_bucket['bucket_name']))
        return storage_cost_list

    def get_storage_cost_sort(self, storage_features, features_name):
        storage_cost_list = self.get_storage_cost_list(storage_features)
        storage_cost_list_len = len(storage_cost_list)
        for i in range(0, storage_cost_list_len):
            min_index = i
            for j in range(i, storage_cost_list_len):
                if storage_cost_list[j][features_name] < storage_cost_list[min_index][features_name]:
                    min_index = j
            if min_index != i:
                t = storage_cost_list[i]
                storage_cost_list[i] = storage_cost_list[min_index]
                storage_cost_list[min_index] = t
        return storage_cost_list

    def myprintlist(self, mylist, mylist_name):
        print mylist_name
        for one in mylist:
            print one

if __name__ == '__main__':
    storage_cost = StorageCost()
    storage_features = {
        'storage_size':  100,
        'storage_time': 6,
        'download_size': 20480,
        'request_frequency': 100,
    }
    storage_features['download_size'] = storage_features['storage_size'] * storage_features['storage_time'] * \
                                        storage_features['request_frequency']
    print "storage_features:", storage_features

    bucket_name = "jcsproxy-aliyun-beijing"
    res = storage_cost.get_storage_cost(storage_features, bucket_name)
    print res

    storage_cost_list = storage_cost.get_storage_cost_list(storage_features)
    storage_cost.myprintlist(storage_cost_list, "storage_cost_list")

    features_name = "storage_expense"
    storage_cost_sort_list = storage_cost.get_storage_cost_sort(storage_features, features_name)
    storage_cost.myprintlist(storage_cost_sort_list, features_name)
    features_name = "sum_expense"
    storage_cost_sort_list = storage_cost.get_storage_cost_sort(storage_features, features_name)
    storage_cost.myprintlist(storage_cost_sort_list, features_name)
    features_name = "download_expense"
    storage_cost_sort_list = storage_cost.get_storage_cost_sort(storage_features, features_name)
    storage_cost.myprintlist(storage_cost_sort_list, features_name)


