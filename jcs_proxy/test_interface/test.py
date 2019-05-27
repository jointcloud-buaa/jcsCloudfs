# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/12/13 3:51'

from xmlrpclib import ServerProxy
from config.configuration import SERVER
import sys



if __name__ == '__main__':

    server_rpc = ServerProxy("http://"+SERVER["host"]+":"+str(SERVER["port"]))
    manager_operate = server_rpc

    # print manager_operate.list_dir('liuyf', '')


