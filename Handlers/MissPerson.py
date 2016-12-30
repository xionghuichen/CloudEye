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
from Base import throw_base_exception
from Base import BaseHandler
from config.globalVal import ReturnStruct

class LastestUpdatePersonHandler(BaseHandler):
    def __init__(self, *argc, **argkw):
        super(LastestUpdatePersonHandler, self).__init__(*argc, **argkw)

    @throw_base_exception     
    def get(self):
        """ Get the person brief information which update resently.

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
        # temp for web request.
        jquery = ''
        try:
            jquery = str(self.get_argument('jsoncallback'))
        except Exception as e:
            pass
        # get the formal cases by size and spot range.
        person_info = self.person_model.get_lastest_person(spot, max_distance, formal, page, size)
        result.data['person_list'] = person_info
        result.data['page'] = page
        result.data['size'] = size
        result.data['formal'] =formal
        self.return_to_client(result, jquery)
        self.finish()

class LastestUpdateMessageHandler(BaseHandler):
    def __init__(self, *argc, **argkw):
        super(LastestUpdateMessageHandler, self).__init__(*argc, **argkw)

    @throw_base_exception     
    def get(self):
        """Get lastest update message [include LBS message, call help mesage and camera find high confidence picture message]

        Args:
            spot:
            max_distance:
            page:
            size:

        Returns:
             {
                "message": "default message",
                "code": 0,
                "data": {
                    "message_list": [
                        {
                            "pic_key": "http://cloudeye.oss-cn-shanghai.aliyuncs.com/user48%3A%3A1482904514.95.jpg?OSSAccessKeyId=LTAIkY3jD1E5hu8z&Expires=1482906060&Signature=SDRhsnWkqQt59dc%2B%2BAkUgZPuqTA%3D",
                            "name": "俞敏洪",
                            "std_pic_key": "http://cloudeye.oss-cn-shanghai.aliyuncs.com/r?OSSAccessKeyId=LTAIkY3jD1E5hu8z&Expires=1482906060&Signature=BT1EQ4VbmIfTBbEeRVWJtpxEbto%3D",
                            "spot": [
                                22.9,
                                22.9
                            ],
                            "date": 1482904513,
                            "person_id": "586353c316b2d60f26bf73ec",
                            "type": 2
                        },
                        {
                            "pic_key": "empty",
                            "name": "chenxionghui",
                            "std_pic_key": "http://cloudeye.oss-cn-shanghai.aliyuncs.com/r?OSSAccessKeyId=LTAIkY3jD1E5hu8z&Expires=1482906060&Signature=BT1EQ4VbmIfTBbEeRVWJtpxEbto%3D",
                            "spot": [
                                22.9,
                                22.9
                            ],
                            "date": 1482888255,
                            "person_id": "5863144416b2d67b38f27f65",
                            "type": 0
                        }
                    ],
                    "page": 0,
                    "size": 10
                }
            }

        """
        result = ReturnStruct()
        spot = eval(self.get_argument("spot"))
        max_distance = float(self.get_argument("max_distance"))
        page = int(self.get_argument('page'))
        size = int(self.get_argument('size'))
        # temp for web request.
        jquery = ''
        try:
            jquery = str(self.get_argument('jsoncallback'))
        except Exception as e:
            pass
        # get the formal cases by size and spot range.
        person_info = self.message_model.get_lastest_message(spot, max_distance, page, size)
        result.data['message_list'] = person_info
        result.data['page'] = page
        result.data['size'] = size
        self.return_to_client(result, jquery)
        self.finish()


class GetMissingPersonDetailHandler(BaseHandler):
    def __init__(self, *argc, **argkw):
        super(GetMissingPersonDetailHandler, self).__init__(*argc, **argkw)
    
    @throw_base_exception    
    def post(self):
        """Get all of information of a specific missing person, 
        include person's detail information adn his camera track list and person track list.

        Args:
            person_id:

        Returns:
            {
                "message": "default message",
                "code": 0,
                "data": {
                    "person_info": {
                        "last_update_time": 1482912276,
                        "lost_time": 1482893944,
                        "relation_telephone": "15195861108",
                        "description": "please help me dear!!!!",
                        "name": "俞敏洪",
                        "lost_spot": [
                            22.9,
                            22.9
                        ],
                        "picture_key_list": [
                            "http://cloudeye.oss-cn-shanghai.aliyuncs.com/reporter%3A48%3A%3A1482893949.95.jpg?OSSAccessKeyId=LTAIkY3jD1E5hu8z&Expires=1482912353&Signature=tPpR%2FNFaDVN2cyg%2FmflSpZcZ4Lo%3D",
                            "http://cloudeye.oss-cn-shanghai.aliyuncs.com/reporter%3A48%3A%3A1482893950.13.jpg?OSSAccessKeyId=LTAIkY3jD1E5hu8z&Expires=1482912353&Signature=Jsn00mREm%2BxF0p2n69Jgjn3qfO4%3D"
                        ],
                        "age": 20,
                        "last_update_spot": [
                            22.9,
                            22.9
                        ],
                        "sex": 0,
                        "relation_name": "chenxionghui",
                        "relation_id": 48,
                        "_id": "58632a7e16b2d67fa66fa9e9",
                        "formal": 0
                    },
                    "machine_track": [
                        {
                            "date": 1482911879,
                            "coordinate": [
                                22.9,
                                22.9
                            ],
                            "confidence": 89.421,
                            "pic_key": "http://cloudeye.oss-cn-shanghai.aliyuncs.com/camera1%3A%3A1482911881.05.jpg?OSSAccessKeyId=LTAIkY3jD1E5hu8z&Expires=1482912353&Signature=3PJal3HamwECLCeUWS2ivVHU2Uw%3D"
                        },
                        {
                            "date": 1482912135,
                            "coordinate": [
                                22.9,
                                22.9
                            ],
                            "confidence": 89.421,
                            "pic_key": "http://cloudeye.oss-cn-shanghai.aliyuncs.com/camera1%3A%3A1482912138.35.jpg?OSSAccessKeyId=LTAIkY3jD1E5hu8z&Expires=1482912353&Signature=yvIfz1Rj6spblpQy5g0n%2Fz%2FiPGY%3D"
                        }
                    ],
                    "person_track": [
                        {
                            "confidence": 89.543,
                            "pic_key": "http://cloudeye.oss-cn-shanghai.aliyuncs.com/user48%3A%3A1482912281.63.jpg?OSSAccessKeyId=LTAIkY3jD1E5hu8z&Expires=1482912353&Signature=f4gzXa%2B1UwfKTVMSQBaiihkBPbI%3D",
                            "user_id": 48,
                            "description": "maybe I find this missing child!",
                            "coordinate": [
                                22.9,
                                22.9
                            ],
                            "user_nick_name": "burningbear",
                            "date": 1482912276
                        }
                    ]
                }
            }
        """
        result = ReturnStruct()
        person_id = self.get_argument("person_id")
        person_info = self.person_model.get_person_detail(person_id)
        result.data = person_info
        self.return_to_client(result)
        self.finish()



class GetMissingPersonDetailWebHandler(BaseHandler):
    def __init__(self, *argc, **argkw):
        super(GetMissingPersonDetailWebHandler, self).__init__(*argc, **argkw)

    @throw_base_exception    
    def get(self):
        """Get all of information of a specific missing person, 
        include person's detail information adn his camera track list and person track list.

        Args:
            person_id:

        Returns:
            {
                "message": "default message",
                "code": 0,
                "data": {
                    "person_info": {
                        "last_update_time": 1482912276,
                        "lost_time": 1482893944,
                        "relation_telephone": "15195861108",
                        "description": "please help me dear!!!!",
                        "name": "俞敏洪",
                        "lost_spot": [
                            22.9,
                            22.9
                        ],
                        "picture_key_list": [
                            "http://cloudeye.oss-cn-shanghai.aliyuncs.com/reporter%3A48%3A%3A1482893949.95.jpg?OSSAccessKeyId=LTAIkY3jD1E5hu8z&Expires=1482912353&Signature=tPpR%2FNFaDVN2cyg%2FmflSpZcZ4Lo%3D",
                            "http://cloudeye.oss-cn-shanghai.aliyuncs.com/reporter%3A48%3A%3A1482893950.13.jpg?OSSAccessKeyId=LTAIkY3jD1E5hu8z&Expires=1482912353&Signature=Jsn00mREm%2BxF0p2n69Jgjn3qfO4%3D"
                        ],
                        "age": 20,
                        "last_update_spot": [
                            22.9,
                            22.9
                        ],
                        "sex": 0,
                        "relation_name": "chenxionghui",
                        "relation_id": 48,
                        "_id": "58632a7e16b2d67fa66fa9e9",
                        "formal": 0
                    },
                    "machine_track": [
                        {
                            "date": 1482911879,
                            "coordinate": [
                                22.9,
                                22.9
                            ],
                            "confidence": 89.421,
                            "pic_key": "http://cloudeye.oss-cn-shanghai.aliyuncs.com/camera1%3A%3A1482911881.05.jpg?OSSAccessKeyId=LTAIkY3jD1E5hu8z&Expires=1482912353&Signature=3PJal3HamwECLCeUWS2ivVHU2Uw%3D"
                        },
                        {
                            "date": 1482912135,
                            "coordinate": [
                                22.9,
                                22.9
                            ],
                            "confidence": 89.421,
                            "pic_key": "http://cloudeye.oss-cn-shanghai.aliyuncs.com/camera1%3A%3A1482912138.35.jpg?OSSAccessKeyId=LTAIkY3jD1E5hu8z&Expires=1482912353&Signature=yvIfz1Rj6spblpQy5g0n%2Fz%2FiPGY%3D"
                        }
                    ],
                    "person_track": [
                        {
                            "confidence": 89.543,
                            "pic_key": "http://cloudeye.oss-cn-shanghai.aliyuncs.com/user48%3A%3A1482912281.63.jpg?OSSAccessKeyId=LTAIkY3jD1E5hu8z&Expires=1482912353&Signature=f4gzXa%2B1UwfKTVMSQBaiihkBPbI%3D",
                            "user_id": 48,
                            "description": "maybe I find this missing child!",
                            "coordinate": [
                                22.9,
                                22.9
                            ],
                            "user_nick_name": "burningbear",
                            "date": 1482912276
                        }
                    ]
                }
            }
        """
        result = ReturnStruct()
        person_id = self.get_argument("person_id")
        # temp for web request.
        jquery = ''
        try:
            jquery = str(self.get_argument('jsoncallback'))
        except Exception as e:
            pass
        person_info = self.person_model.get_person_detail(person_id)
        result.data = person_info
        self.return_to_client(result, jquery)
        self.finish()
