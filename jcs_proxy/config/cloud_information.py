# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/5/1 15:45'

from cloud_config import CLOUDCONFIG
from metadata.cloud_bucket_info import MetadataCloudBucketInfo

class CloudInformation(object):

    def get_cloud_name_list(self):
        # 云名称列表
        return CLOUDCONFIG["cloud_name_list"]

    def get_cloud_bucket_list(self):
        # return CLOUDCONFIG["cloud_bucket_list"]
        # 获取可用云地域信息列表
        return MetadataCloudBucketInfo().get_bucket_list_from_num(1)

    def get_cloud_account_list(self):
        # 获取云账号列表
        return CLOUDCONFIG["cloud_account_list"]

    def get_cloud_price_list(self):
        # 获取云价格类表
        return CLOUDCONFIG["cloud_price_list"]

    def get_cloud_bucket_name_list(self):
        cloud_bucket_list = self.get_cloud_bucket_list()
        cloud_bucket_name_list = []
        for cloud_bucket in cloud_bucket_list:
            cloud_bucket_name_list.append(cloud_bucket['bucket_name'])
        return cloud_bucket_name_list

    def get_cloud_account_from_cloud_name(self, cloud_name='aliyun'):
        cloud_account_list = self.get_cloud_account_list()
        for cloud_account in cloud_account_list:
            if cloud_account['cloud_name'] == cloud_name:
                return cloud_account

    def get_cloud_account_from_bucket_name(self, bucket_name):
        cloud_bucket_list = self.get_cloud_bucket_list()
        for cloud_bucket in cloud_bucket_list:
            if bucket_name == cloud_bucket['bucket_name']:
                cloud_account = self.get_cloud_account_from_cloud_name(cloud_bucket['cloud_name'])
                cloud_account['bucket_name'] = bucket_name
                cloud_account['endpoint'] = cloud_bucket['endpoint']
                return cloud_account

    def get_cloud_price_from_bucket_name(self, bucket_name):
        cloud_bucket_list = self.get_cloud_bucket_list()
        cloud_price_list = self.get_cloud_price_list()
        for cloud_bucket in cloud_bucket_list:
            if bucket_name == cloud_bucket['bucket_name']:
                for cloud_price in cloud_price_list:
                    if cloud_bucket['cloud_name'] == cloud_price['cloud_name'] and \
                        cloud_bucket['storage_type'] == cloud_price['storage_type']:
                            return cloud_price


if __name__ == '__main__':
    cloud_info = CloudInformation()
    print cloud_info.get_cloud_name_list()
    print cloud_info.get_cloud_bucket_list()
    print 'cloud_bucket_list len: ', len(cloud_info.get_cloud_bucket_list())
    print cloud_info.get_cloud_account_list()
    print cloud_info.get_cloud_price_list()

    print ""
    cloud_name = 'aliyun'
    cloud_bucket = cloud_info.get_cloud_bucket_list()[1]
    print cloud_info.get_cloud_account_from_cloud_name(cloud_name)
    print cloud_info.get_cloud_account_from_bucket_name(cloud_bucket['bucket_name'])
    print cloud_info.get_cloud_price_from_bucket_name(cloud_bucket['bucket_name'])

