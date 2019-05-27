# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/6/11 10:11'

import os
import sys
import datetime
import time
import oss2
from oss2.api import PartInfo
from read_write_file import ReadWriteFile
from tools.MyThread import MyThread
import threading


class AliyunOSSExplorer(object):
    """
    阿里云操作接口，aliyun
    """
    def __init__(self, auth_info):
        """
         传入云端账户信息auth_info
        :param auth_info: dict, 云端账户信息
        """
        self.auth_info = auth_info
        self.auth = oss2.Auth(self.auth_info['accesskey_id'], self.auth_info['accesskey_secret'])
        self.bucket = oss2.Bucket(self.auth, self.auth_info['endpoint'], self.auth_info['bucket_name'])

    def check_auth_info(self):
        """
        判断云端账户信息auth_info是否正确（通过调用云端提供的接口验证）
        :return: bool
        """
        try:
            self.bucket.object_exists('check_file')
            return True
        except:
            return False


    ###########################################################

    #新接口试验

    def put_object(self):
        """
        上传字符串
        :return:
        """
        print "put object"
        content = 'a'*1024*1024
        res = self.bucket.put_object('remote_test.txt', content, progress_callback=self.percentage)
        print res.status

    def put_object_file(self):
        print "put object file"
        cloud_file_path = "remote_test.txt"
        local_file_path = "/storage/liuyf_test/jcsProxyDir/datatest/test_4"
        with open(local_file_path, 'rb') as fileobj:
            res = self.bucket.put_object(cloud_file_path, fileobj, progress_callback=self.percentage)
        print res.status

    def put_object_from_file(self):
        print "put objcet from file"
        cloud_file_path = "remote_test.txt"
        local_file_path = "/storage/liuyf_test/jcsProxyDir/datatest/test_32"
        # res = self.bucket.put_object_from_file(cloud_file_path, local_file_path, progress_callback=self.percentage)
        res = self.bucket.put_object_from_file(cloud_file_path, local_file_path, progress_callback=self.percentage_in_file)
        print res.status

    def resumable_upload(self):
        """
        断点续传
        如果上传的本地文件很大，或网络状况不够理想，会出现上传中途失败。
        对已经上传的数据重新上传会浪费时间，占用网络资源
        ResumableStore 指定把进度保存到 /tmp/.py-oss-upload 目录下
        multipart_threshold 指明只要文件长度不小于100KB就进行分片上传
        part_size 参数建议每片大小为100KB。如果文件太大，那么分片大小也可能会大于100KB
        num_threads 参数指定并发上传线程数为4
        :return:
        """
        cloud_file_path = "remote_test.txt"
        local_file_path = "/storage/liuyf_test/jcsProxyDir/datatest/test_4"
        res = oss2.resumable_upload(self.bucket, cloud_file_path, local_file_path,
            store=oss2.ResumableStore(root='/tmp'),
            multipart_threshold=100*1024,
            part_size=100*1024,
            num_threads=4,
            progress_callback=self.percentage)
        print res.status

    def multipart_upload(self):
        """
        采用分片上传，用户可以对上传做更为精细的控制。
        这适用于诸如预先不知道文件大小、并发上传、自定义断点续传等场景。一次分片上传可以分为三个步骤：
        初始化（Bucket.init_multipart_upload）：获得Upload ID
        上传分片（Bucket.upload_part）：这一步可以并发进行
        完成上传（Bucket.complete_multipart_upload）：合并分片，生成OSS文件
        :return:
        """
        cloud_file_path = "remote_test.txt"
        local_file_path = "/storage/liuyf_test/jcsProxyDir/datatest/test_4"

        total_size = os.path.getsize(local_file_path)
        part_size = oss2.determine_part_size(total_size, preferred_size=100 * 1024)  # 确定分片大小的帮助函数
        # 初始化分片
        upload_id = self.bucket.init_multipart_upload(cloud_file_path).upload_id
        parts = []
        # 逐个上传分片
        with open(local_file_path, 'rb') as fileobj:
            part_number = 1
            offset = 0
            while offset < total_size:
                num_to_upload = min(part_size, total_size - offset)
                result = self.bucket.upload_part(cloud_file_path, upload_id, part_number,
                                                oss2.SizedFileAdapter(fileobj, num_to_upload),
                                                 progress_callback=self.percentage)
                # SizedFileAdapter(fileobj, size)会生成一个新的file object，起始偏移和原先一样，但最多只能读取size大小。
                parts.append(PartInfo(part_number, result.etag))
                offset += num_to_upload
                part_number += 1
        # 完成分片上传
        res = self.bucket.complete_multipart_upload(cloud_file_path, upload_id, parts)
        print res.status
        # 验证一下
        with open(local_file_path, 'rb') as fileobj:
            assert self.bucket.get_object(cloud_file_path).read() == fileobj.read()


    def append_object(self):
        """
        首次上传的偏移量（position参数）设为0。如果文件已经存在，且
            不是可追加文件，则抛出ObjectNotAppendable异常；
            是可追加文件，如果传入的偏移和文件当前长度不等，则抛出PositionNotEqualToLength异常。
        如果不是首次上传，可以通过Bucket.head_object方法或上次追加返回值的next_position属性，得到偏移参数。
        :return:
        """
        try:
            self.bucket.delete_object('append.txt')
        except:
            None
        conent = 'a' *1024*1024
        result = self.bucket.append_object('append.txt', 0, conent, progress_callback=self.percentage)
        print "next position", result.next_position
        res = self.bucket.append_object('append.txt', result.next_position, conent, progress_callback=self.percentage)
        print res.status

    #################################################################

    """
    上传接口都提供了可选参数progress_callback，用来帮助实现进度条功能。
    """

    def percentage(self, consumed_bytes, total_bytes):
        """
        进度条回调函数，计算当前完成的百分比
        :param consumed_bytes: 已经上传/下载的数据量
        :param total_bytes: 总数据量
        """
        if total_bytes:
            rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
            print '\r{0}% '.format(rate), datetime.datetime.now()
            # sys.stdout.flush()  # 刷新输出


    def percentage_in_file(self, consumed_bytes, total_bytes):
        """
        当前完成的百分比写入文件
        :param consumed_bytes:
        :param total_bytes:
        :return:
        """
        file_operator = ReadWriteFile()
        file_path = '/storage/liuyf_test/jcsProxyDir/datatest/percentage_test'
        if total_bytes:
            rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
            write_data = str(datetime.datetime.now())
            write_data += " " + str(rate)
            file_operator.write_file(file_path, write_data)
            # print '\r{0}% '.format(rate), datetime.datetime.now()
            # sys.stdout.flush()  # 刷新输出

    def read_percentage(self):
        # 读取进度文件
        print "read_percentage"
        file_path = '/storage/liuyf_test/jcsProxyDir/datatest/percentage_test'
        file_operator = ReadWriteFile()
        while True:
            time.sleep(1)
            rate_res = file_operator.read_file(file_path)
            if len(rate_res) <= 1:  # 读和写并行，有可能出现内容为空的情况
                # print "len", len(rate_res)  # len ==0
                continue
            print rate_res
            rate_list = rate_res.split(" ")
            print rate_list[2]
            if rate_list[2] == '100':
                break
        os.remove(file_path)  # 删除进度文件



    ####################################################################

    def get_object_to_file(self):
        """
        下载到文件
        :return:
        """
        cloud_file_path = "remote_test.txt"
        local_file_path = "/storage/liuyf_test/jcsProxyDir/datatest/download_test"
        res = self.bucket.get_object_to_file(cloud_file_path, local_file_path, progress_callback=self.percentage)
        print res.status

    def resumable_download(self):
        """
        当需要下载的文件很大，或网络状况不够理想，往往下载到中途就失败了。
        如果下次重试，还需要重新下载，就会浪费时间和带宽。

        断点续传的过程大致如下：
            在本地创建一个临时文件，文件名由原始文件名加上一个随机的后缀组成；
            通过指定HTTP请求的 Range 头，按照范围读取OSS文件，并写入到临时文件里相应的位置；
            下载完成之后，把临时文件重名为目标文件。
        在上述过程中，断点信息，即已经下载的范围等信息，会保存在本地磁盘上。
        如果因为某种原因下载中断了，后续重试本次下载，就会读取断点信息，然后只下载缺失的部分。

        含义是
        ResumableDownloadStore 指定把断点信息保存到 /tmp/.py-oss-download 目录下
        multiget_threshold 指明当文件长度不小于20MB时，就采用分范围下载
        part_size 建议每次下载10MB。如果文件太大，那么实际的值会大于指定值
        num_threads 指定并发下载线程数为3

        使用该函数应注意如下细节：
        对同样的源文件、目标文件，避免多个程序（线程）同时调用该函数。因为断点信息会在磁盘上互相覆盖，或临时文件名会冲突。
        避免使用太小的范围（分片），即 part_size 参数不宜过小，建议大于或等于 oss2.defaults.multiget_part_size 。
        如果目标文件已经存在，那么该函数会覆盖此文件。
        :return:
        """
        cloud_file_path = "remote_test.txt"
        local_file_path = "/storage/liuyf_test/jcsProxyDir/datatest/download_test"
        oss2.resumable_download(self.bucket, cloud_file_path, local_file_path,
          store=oss2.ResumableDownloadStore(root='/tmp'),
          multiget_threshold=200*1024,
          part_size=100*1024,
          num_threads=3,
            progress_callback=self.percentage)



if __name__ == '__main__':
    cloud_account = {"cloud_name": "aliyun",
             "accesskey_id": "LTAI58b1C5nvV7jq",
             "accesskey_secret": "3oDwN052MRSXskXzTwnl9w2m0BeuxA",
             "endpoint": "http://oss-cn-beijing.aliyuncs.com",
             "bucket_name": "g504oss"
             }

    cloud_operator = AliyunOSSExplorer(cloud_account)
    res = cloud_operator.check_auth_info()
    print res

    # cloud_operator.put_object()
    # cloud_operator.put_object_file()
    # cloud_operator.put_object_from_file()
    # cloud_operator.resumable_upload()
    # cloud_operator.multipart_upload()
    # cloud_operator.append_object()

    # cloud_operator.get_object_to_file()
    # cloud_operator.resumable_download()


    threads = []
    t_func = MyThread(cloud_operator.put_object_from_file, (), )
    t_read = MyThread(cloud_operator.read_percentage, (), )
    threads.append(t_func)
    threads.append(t_read)
    nloops = len(threads)
    for i in range(nloops):
        threads[i].start()
    for i in range(nloops):
        threads[i].join()