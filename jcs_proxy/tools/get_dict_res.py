# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/1/18 15:37'

class GetDictRes(object):
    """
    定义返回值格式
    """
    def __init__(self):
        pass

    def get_dict_res(self):
        """
        定义返回值格式
        :return: dict
        """
        dict_res = {}
        dict_res['status'] = 0  # 0执行成功，1执行失败
        dict_res['result'] = {}  # 执行结果信息
        return dict_res