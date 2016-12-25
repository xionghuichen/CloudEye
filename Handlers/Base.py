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
import json
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
    def __init__(self, *argc, **argkw):
        super(BaseHandler, self).__init__(*argc, **argkw)
        para = {} 
        para['mongodb'] = self.application.mongodb 
        self.session = self.application.sqldb() 
        para['sqlsession'] = self.session
        para['facepp'] = self.application.facepp
        para['ali_service'] = self.application.ali_service
        para['ali_bucket'] = self.application.ali_bucket
        para['redis'] = self.application.redis
        self._user_model = UserBuizModel(**para) 
        self._face_model = FaceSetBuizModel(**para)
        self._picture_model = PictureBuizModel(**para)
        self._person_model = PersonBuizModel(**para)
        self._message_model = MessageBuizModel(**para)

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


    def change_custom_string_to_json(self, dic):
        # logging.info("in change custom string to json")
        if isinstance(dic, dict):
            for key, value in dic.items():
                # print "in dictory : ",key, value
                # logging.info(" print key %s and value %s"%(key,value))
                if type(value) == bool:
                    # logging.info("in bool value ,key is%s"%key)
                    dic[key] = str(value)
                elif key == '_id':
                    dic[key] = str(dic[key])
                elif key == 'missing_person_list':
                    for index,item in enumerate(dic[key]):
                        dic[key][index]= str(item)
                # elif key == 'image_urls' and isinstance(value, list) and dic[key] != []:
                #     count = 0
                #     while count < len(value):
                #         dic[key][count] = value[count]['origin']
                #         dic[key][count] = Aliyun().parseUrlByFakeKey(
                #             dic[key][count])
                #         count += 1
                # elif key == 'circle_url' and dic[key] != {}:
                #     dic[key] = Aliyun().parseUrlByFakeKey(dic[key])
                if isinstance(value, dict):
                    self.change_custom_string_to_json(value)
                elif isinstance(value, list):
                    # print " out of list ", value
                    for list_value in value:
                        # print "in list : "+str(list_value)
                        self.change_custom_string_to_json(list_value)

    def return_to_client(self,return_struct):
        self.change_custom_string_to_json(return_struct.data)
        return_struct.print_info("after change")
        temp_json = json.dumps({'code':return_struct.code,
            'message':return_struct.message_mapping[return_struct.code],
            'data':return_struct.data})
        temp_json.replace("null", "\'empty\'")
        self.write(temp_json)


