#!/usr/bin/env python
# coding=utf-8
# FaceSetCoreModel.py
import functools

from BaseCoreModel import BaseCoreModel
from _exceptions.http_error import DBError
from facepp_sdk.facepp import APIError
import time
def repeat_send(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        again = True
        count = 0
        while(again):
            again = False
            count +=1
            try:
                return method(self, *args, **kwargs)
            except APIError as e:
                print "error happen:",str(e.body)
                again = True
                if count > 10:
                    raise DBError("face plus plus databases error!")
                else:
                    time.sleep(2)
    return wrapper

class FaceSetCoreModel(BaseCoreModel):
    def __init__(self, *argc, **argkw):
        super(FaceSetCoreModel, self).__init__(*argc, **argkw)  
        self.temp_faceset_token='468d4f8ba70bddbf41aa9b3d2deeb04a'



    @repeat_send
    def search_person(self,url):
        return self.facepp.search(image_url=url,faceset_token=self.temp_faceset_token)