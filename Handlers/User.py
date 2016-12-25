#!/usr/bin/env python
# coding=utf-8
# User.py


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
            result.mergeInfo(result2)
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
        telephone = self.get_argument("telephone")
        password = self.get_argument("password")
        
        result = ReturnStruct()
        result = self.user_model.identify_check(telephone,password)
        if result.code == 0:
            # identify_check success.
            result.data['missing_person_list'] = self.user_model.get_missing_person_list(result.data['user_id'])
            print "result.data is ", result.data
            self.set_secure_cookie('user_id',str(result.data['user_id']))
        self.return_to_client(result)
        self.finish()   


class UpdateStatusHandler(BaseHandler):
    def __init__(self, *argc, **argkw):
        super(UpdateStatusHandler, self).__init__(*argc, **argkw)

    @throw_base_exception
    def post(self):
        message_mapping = [
            'update status success'
        ]
        result = ReturnStruct(message_mapping)
        corrdinate = eval(self.get_argument("corrdinate"))
        user_id = self.get_secure_cookie("user_id")
        # update location.
        self.user_model.update_location(corrdinate, user_id)
        # check message.
        self.return_to_client(result)
        self.finish()