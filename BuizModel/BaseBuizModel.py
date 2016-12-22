#!/usr/bin/env python
# coding=utf-8
# BaseBuizModel.py

from CoreModels.UserCoreModel import UserCoreModel
class BaseBuizModel(object):
    def __init__(self, *argc, **argkw):
        # argkw['mongodb']
        # argkw['sqldb']
        self.user_model = UserCoreModel(*argc, **argkw)