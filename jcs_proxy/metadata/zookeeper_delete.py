# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/5/9 16:42'

from zookeeper_client import ZookeeperClient

def delete_zookeeper_all():
    # 删除zookeeper中的所有元数据信息
    node_path = "/JCS-Proxy/metadata"
    zk_client = ZookeeperClient()
    print zk_client.list_node_name(node_path)
    print zk_client.delete_node_info(node_path, True)
    print zk_client.list_node_name(node_path)

if __name__ == '__main__':
    delete_zookeeper_all()

