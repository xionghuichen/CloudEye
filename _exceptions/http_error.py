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
        self.reason = "参数名称:{} 没有被找到,请检查你的参数".format(arg_name)
        
class DBError(MyHTTPError):
    def __init__(self, reason):
        self.status_code = 500
        self.reason = "数据库相关错误，：{}".format(reason) 

class ArgumentTypeError(MyHTTPError):
    def __init__(self, arg_name):
        self.status_code = 404
        self.reason =  "参数类型传输错误，服务器无法解析: {}".format(arg_name)

class InnerError(MyHTTPError):
    def __init__(self, arg_name):
        self.status_code = 400
        self.reason =  "服务器内部出现错误: {}".format(arg_name)
