#!/usr/bin/env python
# coding=utf-8
# BaseCoreModel.py
import functools
import logging
from _exceptions.http_error import DBError
from facepp_sdk.facepp import APIError, File
def repeat_send(method):
    """this decorator for face++ request. 
    Beacuse face++ free appkey often send high concurrency error.
    after add this decorator, request will send repeatly until response successfully.
    
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        again = True
        count = 0
        while again :
            again = False
            count +=1
            try:
                logging.info("trying connecting to third part service")
                return method(self, *args, **kwargs)    
            except APIError as e:
                logging.info("error happen:%s"%str(e.body))
                again = True
                if count > 15:
                    raise DBError("third part service database error!")
                else:
                    time.sleep(1)
    return wrapper

class BaseCoreModel(object):
    def __init__(self, *argc, **argkw):
        self.mongodb = argkw['mongodb']
        self.session = argkw['sqlsession']
        self.youtu = argkw['youtu']
        self.ali_service = argkw['ali_service']
        self.ali_bucket = argkw['ali_bucket']
        self.redis = argkw['redis']