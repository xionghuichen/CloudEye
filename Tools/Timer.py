#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.3.19
# Modified    :   2017.3.19
# Version     :   1.0

import datetime
import random
import logging
class Timer(object):
    def __init__(self,info):
        self.id = random.randint(1,10000)
        self.time_now = datetime.datetime.now()
        logging.info("[id: %s start time :%s ] %s"%(self.id,info,self.time_now))

    def mark(self,info):
        tn = datetime.datetime.now()
        logging.info("[id: %s time used:%s,]%s"%(self.id,info,tn - self.time_now))
        self.time_now = tn

    def end(self,info):
        tn = datetime.datetime.now()
        logging.info("[id: %s time used:%s,]%s"%(self.id, info,tn - self.time_now))
        logging.info("[id: %s function end] %s"%(self.id, tn))
