#!/usr/bin/python
# _*_ coding: UTF-8 _*_

import sys
import time
sys.path.append("..")
from Channel import *

channel_id = '3553319807874691148' #android
msg = '{"title":"Message from Push","description":"hello world"}'
#msg_ios = '{"aps":{"alert":"iOS Message from Push","sound":"","badge":1},"key1":"value1","key2":"value2"}'
opts = {'msg_type':0, 'expires':300} 

c = Channel()

try:
    ret = c.pushMsgToSingleDevice(channel_id, msg, opts)
    print 'ret: ',
    print ret
    print c.getRequestId()
except ChannelException as e:
    print '[code]',
    print e.getLastErrorCode()
    print '[msg]',
    print e.getLastErrorMsg()
    print '[request id]',
    print c.getRequestId()

try:
    ret = c.pushMsgToAll(msg, opts)
    print 'ret: ',
    print ret
    print c.getRequestId()
except ChannelException as e:
    print '[code]',
    print e.getLastErrorCode()
    print '[msg]',
    print e.getLastErrorMsg()
    print '[request id]',
    print c.getRequestId()

try:
    ret = c.pushMsgToTag('test', msg, 1, opts)
    print 'ret: ',
    print ret
    print '[request id]',
    print c.getRequestId()
except ChannelException as e:
    print '[code]',
    print e.getLastErrorCode()
    print '[msg]',
    print e.getLastErrorMsg()
    print '[request id]',
    print c.getRequestId()
