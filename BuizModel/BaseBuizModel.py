#!/usr/bin/env python
# coding=utf-8
# BaseBuizModel.py

from CoreModels.UserCoreModel import UserCoreModel
from CoreModels.FaceSetCoreModel import FaceSetCoreModel
from CoreModels.OSSCoreModel import OSSCoreModel
from CoreModels.PersonCoreModel import PersonCoreModel
class BaseBuizModel(object):
    def __init__(self, *argc, **argkw):
        self.user_model = UserCoreModel(*argc, **argkw)
        self.face_model = FaceSetCoreModel(*argc, **argkw)
        self.pic_model = OSSCoreModel(*argc, **argkw)
        self.person_model = PersonCoreModel(*argc, **argkw)