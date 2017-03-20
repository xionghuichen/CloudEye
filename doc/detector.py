#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.3.20
# Modified    :   2017.3.20
# Version     :   1.0

def decorator_a(func):
    print 'Get in decorator_a'
    def inner_a(*args, **kwargs):
        print 'Get in inner_a'
        return func(*args, **kwargs)
    return inner_a

def decorator_b(func):
    print 'Get in decorator_b'
    def inner_b(*args, **kwargs):
        print 'Get in inner_b'
        return func(*args, **kwargs)
    return inner_b

@decorator_b
@decorator_a
def f(x):
    print 'Get in f'
    return x * 2

f(1)

# https://segmentfault.com/a/1190000007837364