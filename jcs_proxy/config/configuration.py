# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/1/18 14:45'


SERVER = {
    "host": "your-ip-address-here",
    "port": 8888,
}

CONFIG = {
    "jcsproxy_area": "aliyun-beijing",                                       # 部署地域表示

    # zookeeper路径
    "zk_host": "your-ip-address-here",
    "zk_port": "2181",
    "zk_user_info_path": "/JCS-Proxy/metadata/user_info",                    # 用户账户信息
    "zk_file_info_path": "/JCS-Proxy/metadata/file_info",                    # 文件元数据信息
    "zk_file_statistics_path": "/JCS-Proxy/metadata/statistics",             # 文件操作统计信息
    "zk_cloud_bucket_info_path": "/JCS-Proxy/metadata/cloud_bucket_info",    # 云地域账号信息

    # 文件路径
    "test_file_path": "/storage/ivic/jc/jcsproxy_dir/test_file",                  # 测试文件路径
    # 云故障数据恢复，临时存储路径
    "data_recovery_path": "/storage/ivic/jc/jcsproxy_dir/recovery",
    # 程序文件路径
    "program_path": "/home/cloudfs/jcs_proxy",
}
