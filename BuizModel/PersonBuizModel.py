#!/usr/bin/env python
# coding=utf-8
# PersonBuizModel.py

from BaseBuizModel import BaseBuizModel
from config.globalVal import ReturnStruct

class PersonBuizModel(BaseBuizModel):
    def __init__(self, *argc, **argkw):
        super(PersonBuizModel, self).__init__(*argc, **argkw) 

    def store_new_person(self,pic_key,detect_result):
        # add person_info in mongodb.[get person_id]
        # add to faceset
        # add setUserId
        