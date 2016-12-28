#!/usr/bin/env python
# coding=utf-8
# MissPerson.py

import json
import base64
import logging
import time
import datetime

import tornado.web
import tornado.gen

from _exceptions.http_error import MyMissingArgumentError, ArgumentTypeError
from Base import BaseHandler
from config.globalVal import ReturnStruct

class LastestUpdatePersonHandler(BaseHandler):
    def __init__(self, *argc, **argkw):
        super(LastestUpdatePersonHandler, self).__init__(*argc, **argkw)

    def post(self):
        """
        Args:
            spot:
            max_distance:
            formal:0 or 1:
            page:
            size:

        Returns:
{       {
            "message": "default message",
            "code": 0,
            "data": {
                "formal": 0,
                "size": 10,
                "person_list": [
                    {
                        "person_id": "58632b5316b2d67fe717fd49",
                        "picture_key": "http://cloudeye.oss-cn-shanghai.aliyuncs.com/reporter%3A48%3A%3A1482894162.96.jpg?OSSAccessKeyId=LTAIkY3jD1E5hu8z&Expires=1482901703&Signature=oatfO4cLEBC19peakhj4VkGkL9g%3D",
                        "name": "俞敏洪"
                    }
                    {
                        "person_id": "5863140516b2d67b38f27f60",
                        "picture_key": "http://cloudeye.oss-cn-shanghai.aliyuncs.com/reporter%3A48%3A%3A1482888196.89.jpeg?OSSAccessKeyId=LTAIkY3jD1E5hu8z&Expires=1482901703&Signature=pSo3Hagi1cYpPQwc5MpCeAlNjZw%3D",
                        "name": "chenxionghui"
                    }
                ],
                "page": 0
        }
}

        """
        result = ReturnStruct()
        spot = eval(self.get_argument("spot"))
        max_distance = float(self.get_argument("max_distance"))
        formal = int(self.get_argument("formal"))
        page = int(self.get_argument('page'))
        size = int(self.get_argument('size'))
        # get the formal cases by size and spot range.
        person_info = self.person_model.get_lastest_person(spot, max_distance, formal, page, size)
        result.data['person_list'] = person_info
        result.data['page'] = page
        result.data['size'] = size
        result.data['formal'] =formal
        self.return_to_client(result)
        self.finish()
        # get the unformal cases by size and spot range.
        # get lastest case by spot range