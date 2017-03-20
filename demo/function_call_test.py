#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.3.20
# Modified    :   2017.3.20
# Version     :   1.0



class c1(object):
    def f1(self,f2,*args):
        f2(*args)
    
    def f2(self,t1,t2):
        print t1
        print t2

if __name__ == '__main__':
    c = c1()
    c.f1(c.f2,100,2000)
