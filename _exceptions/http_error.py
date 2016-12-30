#!/usr/bin/env python
# coding=utf-8
# http_error.py

from tornado.web import HTTPError
class MyHTTPError(HTTPError):
    @property
    def log_message(self):
        return self.reason
    def __str__(self):
        return self.reason
        
class MyMissingArgumentError(MyHTTPError):
    """请求参数丢失的时候返回这个error
    """
    def __init__(self, arg_name):
        self.res_name = arg_name
        self.status_code = 404
        self.reason = "parameter :{} can not been find, place check it.".format(arg_name)
        
class DBError(MyHTTPError):
    def __init__(self, reason):
        self.status_code = 500
        self.reason = "some error about databases in server，：{}".format(reason) 

class ArgumentTypeError(MyHTTPError):
    def __init__(self, arg_name):
        self.status_code = 404
        self.reason =  "you pass a parameter which type is error {}".format(arg_name)

class InnerError(MyHTTPError):
    def __init__(self, arg_name):
        self.status_code = 400
        self.reason =  "server inner error: {}".format(arg_name)
