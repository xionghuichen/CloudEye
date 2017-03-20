#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.3.20
# Modified    :   2017.3.20
# Version     :   1.0

from __future__ import absolute_import, print_function, division, with_statement
 
def loop1():
  """ 循环1负责抛出一个函数和对应的参数, 并接收结果
  """
  a = 0
  ret = 1
  while True:
    ret = yield sum, [a, ret]
    a, ret = ret, a
    print("Loop1 ret", ret)

def loop2():
  """ 循环2 负责接收函数并计算结果, 然后 yield 出结果
  """
  while True:
    # send 的赋值语句，对func,args赋值，也就是 sum [a,ret]
    func, args = yield 
    yield func(args)
    print("Loop2")
 
 
l1 = loop1()
l2 = loop2()
tmp = l1.next()
print(tmp)
for i in range(10):
  l2.next()
  ret = l2.send(tmp)
  tmp = l1.send(ret)
# 关于 yield ：http://www.cnblogs.com/coder2012/p/4990834.html