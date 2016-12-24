#!/usr/bin/env python
# coding=utf-8
# FindPerson.py
import json
import base64
import logging

import tornado.web
import tornado.gen

from Base import throwBaseException
from _exceptions.http_error import MyMissingArgumentError
from Base import BaseHandler
from config.globalVal import ReturnStruct

class SearchPersonHandler(BaseHandler):
    def __init__(self, *argc, **argkw):
        super(SearchPersonHandler, self).__init__(*argc, **argkw)
        self.confidence_threshold = 95

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        message_mapping = [
            'search success and confidence higher than %s'%self.confidence_threshold,
            'search success but confidence does not higher than %s'%self.confidence_threshold,
            'search failed'
        ]
        result = ReturnStruct(message_mapping)
        # 1. [todo]upload
        try:
            url = self.get_argument("url")# fade url just for test
        except tornado.web.MissingArgumentError, e:
            raise MyMissingArgumentError(e.arg_name)   
        # 2. search_person
        searchResult =yield tornado.gen.Task(self.face_model.search_person, url)
        if result != None:
            if searchResult['confidence'] > self.confidence_threshold:
                result.code = 0
                result.data = searchResult
            else:
                result.code = 1
        else:
            result.code = 2
        # 3. get person_detail.
        # 4. update track.
        # 5. push message.
        self.return_to_client(result)
        self.finish()

class CallHelpHandler(BaseHandler):
    def __init__(self, *argc, **argkw):
        super(CallHelpHandler, self).__init__(*argc, **argkw)

    @tornado.gen.coroutine
    def post(self):
        message_mapping = [
        'empty image'
        ]
        result =ReturnStruct(message_mapping)
        try:
            base64ImgStr_list = eval(self.get_argument('base64ImgStr_list'))
            user_id = self.get_secure_cookie("user_id")
            info_data={
                'name':self.get_argument('name'),
                'sex':int(self.get_argument('sex')),
                'age':int(self.get_argument('age')),
                'relation_telephone':self.get_argument('relation_telephone'),
                'relation_name':self.get_argument('relation_name'),
                'relation_id': user_id,
                'lost_time':self.get_argument('lost_time'),
                'lost_spot':self.get_argument('lost_spot'),
                'description':self.get_argument('description')
            }
        except tornado.web.MissingArgumentError, e:
            raise MyMissingArgumentError(e.arg_name)     

        if user_id == None or user_id == '':
            raise MyMissingArgumentError("cookie: user_id ")
        imgBytes_list = []
        if base64ImgStr_list == []:
            result.code = 0
        else:
            # has image
            for image_str in base64ImgStr_list:
                imgBytes_list.append(base64.b64decode(image_str))
            # get face_token _list
            result_detect = yield tornado.gen.Task(self.face_model.detect_img_list, imgBytes_list)
            result.mergeInfo(result_detect)
            if result_detect.code == 0:
                # upload pictures.
                result_pic_key = yield tornado.gen.Task(self.picture_model.store_pictures,imgBytes_list,user_id)
                # todo, error handler
                # store information.[track and person]
                detect_result_list = result_detect.data['detect_result_list']
                self.person_model.store_new_person(result_pic_key, detect_result_list, info_data)
            # send message

            # get oss key list

        self.return_to_client(result)
        self.finish()