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

class LastestCaseHandler(BaseHandler):
    def __init__(self, *argc, **argkw):
        super(SearchPersonHandler, self).__init__(*argc, **argkw)

    def post(self):
        """
        Args:
            spot:
            max_distance:

        """
        spot = self.get_argument("spot")
        max_distance = self.get_argument("max_distance")
        self.person_model.get_lastest_case(sopt, max_distance)
        # get the formal cases by size and spot range.
        # self.person_model.get_cases_message(formal = True, )
        # get the unformal cases by size and spot range.
        # get lastest case by spot range