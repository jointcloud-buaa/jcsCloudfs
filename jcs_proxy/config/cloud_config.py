# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/10/7 19:56'

CLOUDCONFIG = {
    # 云name
    "cloud_name_list": ['aliyun', 'baidu', 'ksyun'],

    # 云bucket
    "cloud_bucket_list": [
        {'cloud_name': 'aliyun', 'area_name': 'qingdao', 'storage_type': 'standard',
            'bucket_name': 'shaoly-aliyun-qingdao', 'endpoint': 'http://oss-cn-qingdao.aliyuncs.com'},
        {'cloud_name': 'aliyun', 'area_name': 'shanghai', 'storage_type': 'standard',
         'bucket_name': 'shaoly-aliyun-shanghai', 'endpoint': 'http://oss-cn-shanghai.aliyuncs.com'},
        {'cloud_name': 'ksyun', 'area_name': 'beijing', 'storage_type': 'standard',
         'bucket_name': 'ks3test-bj', 'endpoint': 'ks3-cn-beijing.ksyun.com'}
    ],

    # 云账户（子账号，ksyun不是）
    "cloud_account_list": [
        {"cloud_name": "aliyun",
         "accesskey_id": "your-ak-here",
         "accesskey_secret": "your-sk-here",
         "endpoint": "http://oss-cn-beijing.aliyuncs.com",
         "bucket_name": "shaoly-aliyun-beijing"
         },
        {"cloud_name": "ksyun",
         "accesskey_id": "your-ak-here",
         "accesskey_secret": "your-sk-here",
         "endpoint": "ks3-cn-beijing.ksyun.com",
         "bucket_name": "ks3test-bj"
         }
    ],

    # 云定价
    "cloud_price_list": [
        # 标准存储
        {'cloud_name': 'aliyun',
         'storage_type': 'standard',
         'storage': 0.148,  # 标准存储：0.148元/GB/月
         'download': 0.5,  # 下载流量：0.5元/GB
         'request': 0.01,  # 请求费用：0.01元/万次
         'retrieve': 0,  # 数据取回费用
         'lowmonth': 0,  # 最短存储期限为0个月
         },
        {'cloud_name': 'baidu',
         'storage_type': 'standard',
         'storage': 0.128,
         'download': 0.6,
         'request': 0.01,
         'retrieve': 0,
         'lowmonth': 0,
         },
        {'cloud_name': 'ksyun',
         'storage_type': 'standard',
         'storage': 0.17,
         'download': 0.56,
         'request': 0.01,
         'retrieve': 0,  # 数据取回费用
         'lowmonth': 0,  # 最短存储期限为0个月
         },

        # 低频存储
        {'cloud_name': 'aliyun',
         'storage_type': 'low',
         'storage': 0.08,
         'download': 0.5,
         'request': 0.1,
         'retrieve': 0.0325,  # 数据取回费用0.0325元/GB
         'lowmonth': 1,  # 最短存储期限为1个月
         },
        {'cloud_name': 'baidu',
         'storage_type': 'low',
         'storage': 0.08,
         'download': 0.6,
         'request': 0.25,
         'retrieve': 0.03,
         'lowmonth': 1,
         },

        # # 冷存储
        # {'cloud_name': 'baidu',
        #  'storage_type': 'cold',
        #  'storage': 0.048,
        #  'download': 0.6,
        #  'request': 0.5,
        #  'retrieve': 0.15,
        #  'lowmonth': 3,
        #  }
    ],
}
