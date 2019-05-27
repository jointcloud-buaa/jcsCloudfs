# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/10/7 19:42'

class Singleton(object):
    _instance = None
    _first_init = True
    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kw)
        return cls._instance