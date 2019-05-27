# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/1/16 22:01'

import datetime
import time

class GetFuncTime(object):
    """
    计算某个方法的执行时间
    """
    def __init__(self):
        pass

    def change_to_seconds(self, str_time):
        # 时间0:01:01.407098 转换成 61.407098 s
        my_split = str_time.split(':')
        hours = float(my_split[0])
        minutes = float(my_split[1])
        seconds = float(my_split[2])
        sum_sec = seconds + minutes*60 + hours*60*60
        return sum_sec

    def get_func_time(self, func, args):
        """
        计算某个方法的执行时间
        :param func: 
        :param args: 
        :return: 
        """
        start_time = datetime.datetime.now()
        res = func(*args)
        end_time = datetime.datetime.now()
        func_time = self.change_to_seconds(str(end_time-start_time))
        return res, func_time

class Add(object):
    def add(self, a, b):
        time.sleep(1)
        return a+b

if __name__ == '__main__':
    print("test")
    res, func_time = GetFuncTime().get_func_time(Add().add, (1, 2))
    print(res)
    print(func_time)