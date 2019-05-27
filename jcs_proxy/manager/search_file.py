# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/6/5 16:17'

from tools.get_dict_res import GetDictRes
from metadata.file_info import MetadataFileInfo
import re

class SearchFile(object):
    def __init__(self):
        self.metadata_file_info = MetadataFileInfo()

    def search_file(self, dir_path, file_name):  # dir_path = user_name
        """
        搜索文件，根据文件名
        递归遍历搜索
        :param file_name:
        :return:
        """
        res_list = []
        self.deep_search_file(res_list, dir_path, file_name)
        dict_res = GetDictRes().get_dict_res()
        dict_res['status'] = 0
        dict_res['result'] = res_list
        return dict_res

    def deep_search_file(self, res_list, now_dir_path, find_file_name):
        dict_res = self.metadata_file_info.list_dir_name(now_dir_path)
        if dict_res['status'] == 0:
            file_name_list = dict_res['result']
            for file_name in file_name_list:
                search_str = ".*"+find_file_name+".*"
                m = re.search(search_str, file_name)
                if m is not None:  # 如果正则匹配到了
                    res_list.append(now_dir_path+'/'+file_name)
                self.deep_search_file(res_list, now_dir_path+'/'+file_name, find_file_name)