#!/usr/bin/env python
# coding=utf-8
# FindPerson.py


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
        result = ReturnStruct()
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
        # 3. get person_detail
        # 4. update track
        # 5. push message.
        result.message = message_mapping[result.code]
        self.return_to_client(result)
        self.finish()