# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/1/19 12:14'

from metadata.zookeeper_client import ZookeeperClient
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    print("metadata zk ")
    metadata_zk_operate = ZookeeperClient()

    # node_path = "/lyf/test"
    # node_info = "hello lyf test"
    node_path = "/key目录/key键值"
    node_info = "这是内容 value"

    print("check node exists")
    res = metadata_zk_operate.check_node_exists(node_path)            # node不存在
    print(res)

    print("create node info")
    res = metadata_zk_operate.create_node_info(node_path, node_info)  # 新建node
    print(res)
    res = metadata_zk_operate.create_node_info(node_path, node_info)  # 新建node, node已存在，操作失败
    print(res)
    res = metadata_zk_operate.create_node_info(node_path, node_info, cover=True)  # 新建node，node已存在则覆盖
    print(res)

    print("check nod exists")
    res = metadata_zk_operate.check_node_exists(node_path)            # node存在
    print(res)


    print("get node info")
    res = metadata_zk_operate.get_node_info("")                     # 获取node信息，为空
    print(res)
    res = metadata_zk_operate.get_node_info(node_path)              # 获取node信息
    print(res)
    res = metadata_zk_operate.get_node_info("wrong")                # 获取node信息，node不存在，操作失败
    print(res)


    print("list node name")
    res = metadata_zk_operate.list_node_name("")                    # node名列表，根目录
    print(res)
    res = metadata_zk_operate.list_node_name(node_path)             # node名列表
    print(res)
    res = metadata_zk_operate.list_node_name("wrong")               # node名列表，node不存在，操作失败
    print(res)

    print("list node info")
    res = metadata_zk_operate.list_node_info("")                    # node信息列表，根目录
    print(res)
    res = metadata_zk_operate.list_node_info(node_path)             # node信息列表
    print(res)
    res = metadata_zk_operate.list_node_info("wrong")               # node信息列表，node不存在，操作失败
    print(res)

    print("delete node info")
    res = metadata_zk_operate.delete_node_info(node_path)           # 删除node, 存在children，操作失败
    print(res)
    res = metadata_zk_operate.delete_node_info(node_path, recursive=True)  # 删除node，存在children,则递归删除
    print(res)
    res = metadata_zk_operate.delete_node_info(node_path)           # 删除node, node不存在，操作失败
    print(res)

    metadata_zk_operate.zk_stop()                                   #关闭连接

