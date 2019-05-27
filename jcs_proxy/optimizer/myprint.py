# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/5/24 15:30'

class MyPrint(object):
    def __init__(self):
        pass

    def myprintdict(self, mydict, mydict_name):
        print ""
        print mydict_name
        for key in mydict:
            print key, mydict[key]

    def myprintlist(self, mylist, mylist_name):
        print ""
        print mylist_name
        for one in mylist:
            print one