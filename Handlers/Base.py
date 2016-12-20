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


class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *argc, **argkw):
        super(BaseHandler, self).__init__(*argc, **argkw)
        self._db = self.application.db
        # self._redis_dict = self.application._redis_dict
        # # load all of variable needed into BaseHandler.
        # config = ConfigParser.ConfigParser()
        # config.readfp(open(AP + '/common/conf.ini'))
        # self._aes_key = config.get('app', 'secret')
        # self._appkey = config.get('app', 'appkey')
        # self._prefix = config.get('url', 'prefix')
        # self._public_access = config.get('app', 'public_access')
        # self._virtual_access = config.get('app', 'virtual_access')
        # # load all of module operate into BaseHandler.
        # self._user_module = modules.user.UserInfoModule(self._db)
        # self._user_list_module = modules.user.UserListModule(self._db)
        # self._user_detail_module = modules.user.UserDetailModule(self._db)
        # self._user_message_module = modules.message.UserMessageModule(self._db)
        # self._code_dict = CODE_DICT
        # self._elastic_user_module = modules.ec_user.ElasticUserModule(
        #     self.application.es)
        # logging.info("request is : %s \n \n" % self.request)
        # args = self.request.arguments
        # logging.info("request arguments: %s" % args)

