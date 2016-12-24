#!/usr/bin/env python
# coding=utf-8
# FindPerson.py
import json
import base64
import logging

import tornado.web
import tornado.gen

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
        url = self.get_argument("url")# fade url just for test
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

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        message_mapping = [
        'empty image'
        ]
        result =ReturnStruct(message_mapping)
        base64ImgStr_list = eval(self.get_argument('base64ImgStr_list'))
        imgBytes_list = []
        if base64ImgStr_list == []:
            result.code = 0
        else:
            for image_str in base64ImgStr_list:
                imgBytes_list.append(base64.b64decode(image_str))
            # get face_token _list
            result2 = yield tornado.gen.Task(self.face_model.detect_img_list, imgBytes_list)
        result.mergeInfo(result2)
            # get oss key list

        self.return_to_client(result)
        self.finish()