#!/usr/bin/env python
# coding=utf-8
# base.py

import os
import ConfigParser
import functools
import logging
import json
import urllib
import tornado.web
import tornado.gen
import tornado.httpclient
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
import json
from bson import ObjectId
from config.globalVal import MAX_WORKERS
from BuizModel.UserBuizModel import UserBuizModel 
from BuizModel.FaceSetBuizModel import FaceSetBuizModel
from BuizModel.PictureBuizModel import PictureBuizModel
from BuizModel.PersonBuizModel import PersonBuizModel
from BuizModel.MessageBuizModel import MessageBuizModel
from _exceptions.http_error import MyMissingArgumentError

def throw_base_exception(method):
    """This is a decorator to handler all of common exception in this App

    Should be add in all of post or get method in xxxHandler.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except tornado.web.MissingArgumentError, e:
            raise MyMissingArgumentError(e.arg_name)
    return wrapper
    

class BaseHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

    def __init__(self, *argc, **argkw):
        super(BaseHandler, self).__init__(*argc, **argkw)
        para = {} 
        para['mongodb'] = self.application.mongodb 
        self.session = self.application.sqldb() 
        para['sqlsession'] = self.session
        para['youtu'] = self.application.youtu
        para['ali_service'] = self.application.ali_service
        para['ali_bucket'] = self.application.ali_bucket
        para['redis'] = self.application.redis
        self._user_model = UserBuizModel(**para) 
        self._face_model = FaceSetBuizModel(**para)
        self._picture_model = PictureBuizModel(**para)
        self._person_model = PersonBuizModel(**para)
        self._message_model = MessageBuizModel(**para)
        self.confirm_level = self.face_model.VERY_HIGH_CONFIDENCE
        # logging.info("------request is ----------: %s \n \n" % self.request)
        args = self.request.arguments
        # logging.info("-----request arguments-------: %s \n \n" % json.dumps(args,indent=2))
    @property
    def message_model(self):
        return self._message_model

    @property
    def person_model(self):
        return self._person_model
        
    @property
    def user_model(self):
        return self._user_model

    @property
    def face_model(self):
        return self._face_model

    @property
    def picture_model(self):
        return self._picture_model
    
    def __del__(self):
        self.session.close()

    @run_on_executor
    def background_task(self,function,*argc):
        return function(*argc)

    def change_custom_string_to_json(self, dic):
        # logging.info("in change custom string to json")
        if isinstance(dic, dict):
            for key, value in dic.items():
                # print "in dictory : ",key, value
                # logging.info(" print key %s and value %s"%(key,value))
                if type(value) == bool:
                    # logging.info("in bool value ,key is%s"%key)
                    dic[key] = str(value)
                elif key == '_id' or key == 'person_id' or key == 'message_id':
                    dic[key] = str(dic[key])
                elif key == 'missing_person_list':
                    for index,item in enumerate(dic[key]):
                        dic[key][index]= str(item)
                elif key == 'std_pic_key' or key == 'std_photo_key' or key == 'picture_key' or key == 'pic_key' or key =='picture_key_list':
                    if dic[key] =='empty':
                        continue
                    if type(dic[key]) == list:
                        for index,item in enumerate(dic[key]):
                            dic[key][index]= self.picture_model.get_url(item)
                    else:
                        dic[key] = self.picture_model.get_url(value)
                if isinstance(value, dict):
                    self.change_custom_string_to_json(value)
                elif isinstance(value, list):
                    for list_value in value:
                        self.change_custom_string_to_json(list_value)

    def return_to_client(self,return_struct, JQuery=''):
        self.change_custom_string_to_json(return_struct.data)
        # return_struct.print_info("after change")
        temp_json = json.dumps({'code':return_struct.code,
            'message':return_struct.message_mapping[return_struct.code],
            'data':return_struct.data},ensure_ascii=False)
        temp_json.replace("null", "\'empty\'")
        if JQuery != '':
            temp_json = JQuery+'('+temp_json+')'
        self.write(temp_json)


