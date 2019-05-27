# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/4/26 18:53'

import os
from config.configuration import CONFIG

class CreateTestFile(object):
    def __init__(self):
        self.datatest_path = CONFIG["test_file_path"]
        self.file_size_list = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]

    def create_defsize_file_list(self):
        try:
            os.mkdir(self.datatest_path)
        except:
            pass
        for i in range(len(self.file_size_list)):
            print "生成文件，file_size(M):", self.file_size_list[i]
            self.create_defsize_file(self.file_size_list[i])

    def create_defsize_file(self, file_size):
        file_name = 'test_' + str(file_size)
        local_file = os.path.join(self.datatest_path, file_name)
        fp = open(local_file, "w")
        fp.seek(file_size * 1024 * 1024 - 1)
        fp.write('\0')
        fp.close()

    def create_text_file(self):
        print "生成文件，test.txt， 文件.txt"
        file_name = "test.txt"
        local_file = os.path.join(self.datatest_path, file_name)
        fp = open(local_file, "w")
        fp.write("this is test.txt")
        fp.close()
        file_name = "文件.txt"
        local_file = os.path.join(self.datatest_path, file_name)
        fp = open(local_file, "w")
        fp.write("this is 文件.txt")
        fp.close()



if __name__ == '__main__':
    # 生成特定大小的测试文件
    CreateTestFile().create_defsize_file_list()
    CreateTestFile().create_text_file()