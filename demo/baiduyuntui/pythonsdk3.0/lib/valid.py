#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import inspect

import re

import socket

from lib.ChannelException import ChannelException
 
opt_keys ={
        'pushMsgToSingleDevice' : ('expires', 'device_type', 'msg_expires', 'msg_type', 'deploy_status'),
        'pushMsgToAll' : ('expires', 'device_type', 'msg_expires', 'msg_type', 'deploy_status', 'send_time'),
        'pushMsgToTag' : ('expires', 'device_type', 'msg_expires', 'msg_type', 'deploy_status', 'send_time'),
        'pushBatchUniMsg' : ('expires', 'device_type', 'msg_expires', 'msg_type', 'topic_id'),
        'queryTimerRecords' : ('expires', 'device_type', 'start', 'limit', 'range_start', 'range_end'),
        'queryTopicRecords':('expires', 'device_type', 'start', 'limit', 'range_start', 'range_end'),
        'queryTimerList' : ('expires', 'device_type', 'timer_id', 'start', 'limit'),
        'queryTopicList' : ('expires', 'device_type', 'start', 'limit'),
        'queryTags' : ('expires', 'device_type', 'tag', 'start', 'limit')}

def validParam(*varargs, **keywords):
    """验证参数的装饰器。"""
     
    varargs = map(_toStardardCondition, varargs)
    keywords = dict((k, _toStardardCondition(keywords[k]))
                    for k in keywords)
     
    def generator(func):
        args, varargname, kwname = inspect.getargspec(func)[:3]
        dctValidator = _getcallargs(args, varargname, kwname,
                                    varargs, keywords)
         
        def wrapper(*callvarargs, **callkeywords):
            dctCallArgs = _getcallargs(args, varargname, kwname,
                                       callvarargs, callkeywords)
             
            k, item = None, None
            try:
                for k in dctValidator:
                    if k == varargname:
                        for item in dctCallArgs[k]:
                            assert dctValidator[k](item)
                    elif k == kwname:
                        for item in dctCallArgs[k].values():
                            assert dctValidator[k](item)
                    else:
                        item = dctCallArgs[k]
                        assert dctValidator[k](item)
            except:
                raise ChannelException(
                       ('parameter validation fails, param: %s, value: %s(%s)'
                       % (k, item, item.__class__.__name__)), 3)
             
            return func(*callvarargs, **callkeywords)
         
        wrapper = _wrapps(wrapper, func)
        return wrapper
     
    return generator
 
 
def _toStardardCondition(condition):
    """将各种格式的检查条件转换为检查函数"""
     
    if inspect.isclass(condition):
        return lambda x: isinstance(x, condition)
     
    if isinstance(condition, (tuple, list)):
        cls, condition = condition[:2]
        if condition is None:
            return _toStardardCondition(cls)
         
        if cls in (str, unicode) and condition[0] == condition[-1] == '/':
            return lambda x: (isinstance(x, cls)
                              and re.match(condition[1:-1], x) is not None)
         
        return lambda x: isinstance(x, cls) and eval(condition)
     
    return condition
 
 
def nullOk(cls, condition=None):
    """这个函数指定的检查条件可以接受None值"""
     
    return lambda x: x is None or _toStardardCondition((cls, condition))(x)
 
 
def multiType(*conditions):
    """这个函数指定的检查条件只需要有一个通过"""
     
    lstValidator = map(_toStardardCondition, conditions)
    def validate(x):
        for v in lstValidator:
            if v(x):
                return True
    return validate
 
 
def _getcallargs(args, varargname, kwname, varargs, keywords):
    """获取调用时的各参数名-值的字典"""
     
    dctArgs = {}
    varargs = tuple(varargs)
    keywords = dict(keywords)
     
    argcount = len(args)
    varcount = len(varargs)
    callvarargs = None
     
    if argcount <= varcount:
        for n, argname in enumerate(args):
            dctArgs[argname] = varargs[n]
         
        callvarargs = varargs[-(varcount-argcount):]
     
    else:
        for n, var in enumerate(varargs):
            dctArgs[args[n]] = var
         
        for argname in args[-(argcount-varcount):]:
            if argname in keywords:
                dctArgs[argname] = keywords.pop(argname)
         
        callvarargs = ()
     
    if varargname is not None:
        dctArgs[varargname] = callvarargs
     
    if kwname is not None:
        dctArgs[kwname] = keywords
     
    dctArgs.update(keywords)
    return dctArgs
 
 
def _wrapps(wrapper, wrapped):
    """复制元数据"""
     
    for attr in ('__module__', '__name__', '__doc__'):
        setattr(wrapper, attr, getattr(wrapped, attr))
    for attr in ('__dict__',):
        getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
     
    return wrapper


def _checkValue(key, value):
    if key == 'msg_type':
        @validParam(msg_type=(int, '-1<x<2'))
        def foo(msg_type): pass
        foo(value)
    if key == 'expires':
        @validParam(expires=(int, '0<x'))
        def foo(expires): pass
        foo(value)
    if key == 'device_type':
        @validParam(device_type=(int, '2<x<5'))
        def foo(device_type): pass
        foo(value)
    if key == 'start':
        @validParam(int)
        def foo(start): pass
        foo(value)
    if key == 'limit':
        @validParam(limit=(int, '0<x<101'))
        def foo(limit): pass
        foo(value)
    if key == 'range_start':
        @validParam(int)
        def foo(range_start): pass
        foo(value)
    if key == 'range_end':
        @validParam(int)
        def foo(range_end): pass
        foo(value)
    if key == 'timer_id':
        @validParam(str)
        def foo(timer_id): pass
        foo(value)
    if key == 'deploy_status':
        @validParam(deploy_status=(int, '0<x<3'))
        def foo(deploy_status): pass
        foo(value)
    if key == 'topic_id':
        @validParam(topic_id=(str, 'len(x)<20'))
        def foo(topic_id): pass
        foo(value)
    if key == 'send_time':
        @validParam(int)
        def foo(send_time): pass
        foo(value)
    if key == 'tag':
        @validParam(tag=(str, '0<len(x)<129'))
        def foo(tag): pass
        foo(value)


def validOptDict(x, api_name):
    """校验可选字段"""

    if x is None:
        return True
    else:
        for key, value in x.items():
            if not key in opt_keys[api_name]:
                raise ChannelException(
                       ('parameter validation fails, param: %s is not required'
                       % (key)), 3)
            else:
                _checkValue(key, value)
