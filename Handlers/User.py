#!/usr/bin/env python
# coding=utf-8
# User.py

import logging

from Base import BaseHandler

from _exceptions.http_error import DBError
from Base import throw_base_exception
from tornado.web import MissingArgumentError
from config.globalVal import ReturnStruct


class RegisterHandler(BaseHandler):
    def __init__(self, *argc, **argkw):
        super(RegisterHandler, self).__init__(*argc, **argkw)
        
    @throw_base_exception        
    def post(self):
        """Register new user in system.

        Args:

        Returns:
        """
        telephone = self.get_argument("telephone")
        password = self.get_argument("password")
        real_name = self.get_argument("real_name")
        nick_name = self.get_argument("nick_name")
        id_number = self.get_argument("id_number")
        # telephone check
        result = self.user_model.unique_check(telephone)
        if result.code == 0: 
            # user register
            result2 = self.user_model.register_new_user(telephone, password, real_name, nick_name, id_number)
            result.merge_info(result2)
            try:
                self.user_model.import_missing_person(telephone)
            except Exception as e:
                self.user_model.remove_user(telephone)
                raise DBError('服务器内部出现错误了...')
            #[todo] import missing person list to user_collection.
        self.return_to_client(result)
        self.finish()


class LoginHandler(BaseHandler):
    def __init__(self, *argc, **argkw):
        super(LoginHandler, self).__init__(*argc, **argkw)    

    @throw_base_exception
    def post(self):
        """Login to system.

        Args:

        Returns:
        """
        telephone = self.get_argument("telephone")
        password = self.get_argument("password")
        result = self.user_model.identify_check(telephone,password)
        if result.code == 0:
            # identify_check success.
            result.data['missing_person_list'] = self.user_model.get_missing_person_list(result.data['user_id'])
            self.set_secure_cookie('user_id',str(result.data['user_id']))
        self.return_to_client(result)
        self.finish()   


class UpdateStatusHandler(BaseHandler):
    def __init__(self, *argc, **argkw):
        super(UpdateStatusHandler, self).__init__(*argc, **argkw)

    @throw_base_exception
    def post(self):
        """After user login successfully, 
        client should send request to update his location and check if there are new message in user's message queue in regular.

        Args:
            coordinates: user's location, pass format: [x,y]
            user_id:

        Returns:
        """
        coordinates = eval(self.get_argument("coordinates"))
        user_id = int(self.get_secure_cookie("user_id"))
        # update location.
        self.user_model.update_location(coordinates, user_id)
        # check message.
        result = self.user_model.check_message(user_id)
        self.return_to_client(result)
        self.finish()

class ConfirmHandler(BaseHandler):
    def __init__(self, * argc, ** argkw):
        super(ConfirmHandler, self).__init__(*argc, **argkw)

    @throw_base_exception
    def post(self):
        """If client has get his new message queue then it should send this request to clear message queue in server[redis].

        Args:

        Returns:

        """
        result = ReturnStruct()
        # get user_id
        user_id = int(self.get_secure_cookie("user_id"))
        # clear has_update_status
        self.user_model.clear_update_status(user_id)
        # clear message.
        self.user_model.clear_message(user_id)
        self.return_to_client(result)
        self.finish()

class LogoutHandler(BaseHandler):
    def __init__(self, * argc, ** argkw):
        super(LogoutHandler, self).__init__(*argc, **argkw)
    
    @throw_base_exception
    def post(self):
        """clear user's online status, user will not receive message after logout.

        Args:

        Returns:

        """
        result = ReturnStruct()
        # get user_id
        user_id = int(self.get_secure_cookie("user_id"))
        self.user_model.clear_online_status(user_id)
        self.return_to_client(result)
        self.finish()


class MyPersonListHandler(BaseHandler):
    def __init__(self, * argc, ** argkw):
        super(MyPersonListHandler, self).__init__(*argc, **argkw)
    
    @throw_base_exception    
    def post(self):
        """get user's reporter list.

        Args:
            user_id:
        
        Returns:
            {
                "message": "default message",
                "code": 0,
                "data": {
                    "peron_brief_info": [
                        {
                            "person_id": "5863140516b2d67b38f27f60",
                            "last_update_time": 1482888193,
                            "last_update_spot": [
                                22.9,
                                22.9
                            ],
                            "name": "chenxionghui",
                            "std_photo_key": "reporter:48::1482888196.89.jpeg"
                        },
                        {
                            "person_id": "58632a7e16b2d67fa66fa9e9",
                            "last_update_time": 1482912276,
                            "last_update_spot": [
                                22.9,
                                22.9
                            ],
                            "name": "俞敏洪",
                            "std_photo_key": "reporter:48::1482893949.95.jpg"
                        }
                    ]
                }
            }
        """
        result = ReturnStruct()
        user_id = int(self.get_secure_cookie('user_id'))
        person_id_list = self.user_model.get_missing_person_list(user_id)
        result.data['peron_brief_info'] = self.person_model.get_person_brief_info(person_id_list)
        self.return_to_client(result)
        self.finish()