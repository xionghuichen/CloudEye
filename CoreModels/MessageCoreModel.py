#!/usr/bin/env python
# coding=utf-8
# MessageCoreModel.py

from BaseCoreModel import BaseCoreModel

class MessageCoreModel(BaseCoreModel):
    def __init__(self, *argc, **argkw):
        super(MessageCoreModel, self).__init__(*argc, **argkw)


    def get_message_detail(self,info):
        pass
    
    def insert_message_detail(self,info):
        pass
    
    def add_to_single_user(self, info, user):
        pass

    def add_to_users(self, info, users):
        pass