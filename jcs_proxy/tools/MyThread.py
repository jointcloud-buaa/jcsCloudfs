# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/4/26 22:06'

import threading

class MyThread(threading.Thread):
    def __init__(self, func, args, name = ''):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.name = name
        self.res = ''

    def getResult(self):
        return self.res

    def run(self):
        self.res = self.func(*self.args)


def add(a, b):
    return a+b

if __name__ == '__main__':
    thread1 = MyThread(add, (1,2), )
    thread1.start()
    thread1.join()
    res = thread1.getResult()
    print res

    print ""
    print "threads"
    nloops = 3
    threads = []
    for i in range(nloops):
        t = MyThread(add, (i, i+1), )
        threads.append(t)
    for i in range(nloops):
        threads[i].start()
    for i in range(nloops):
        threads[i].join()
    results = []
    for i in range(nloops):
        res = threads[i].getResult()
        results.append(res)
        print res