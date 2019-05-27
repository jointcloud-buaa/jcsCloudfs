# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/1/17 20:49'

from metadata.cloud_bucket_info import MetadataCloudBucketInfo
from server.server_rpc import ServerRpc
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    print("cloud bucket info set")
    MetadataCloudBucketInfo()
    print("JointCloudStorage server start")
    ServerRpc().server_start()

