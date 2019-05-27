# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/6/11 15:00'

class ReadWriteFile(object):
    def __init__(self):
        pass

    def write_file(self, file_name, str_data):
        # 覆盖写入
        fp = open(file_name, 'wb')
        fp.write(str_data)
        fp.close()

    def read_file(self, file_name):
        fp = open(file_name, 'rb')
        str_data = fp.read()
        fp.close()
        return str_data

if __name__ == '__main__':
    content = "this is content"
    file_path = '/storage/liuyf_test/jcsProxyDir/datatest/percentage_test'
    file_operator = ReadWriteFile()
    file_operator.write_file(file_path, content)
    print file_operator.read_file(file_path)