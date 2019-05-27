# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/6/5 14:28'

from cloud_interface.delete_cloud_all import delete_cloud_all
from metadata.zookeeper_delete import delete_zookeeper_all
from datalog_operation.datalog_used_traffic import DatalogUsedTraffic

if __name__ == '__main__':
    print "删除云上所有存储文件"
    delete_cloud_all()

    print "删除zookeeper中的所有元数据信息"
    delete_zookeeper_all()

    print "删除ES中的所有日志信息"
    print DatalogUsedTraffic().delete_all()