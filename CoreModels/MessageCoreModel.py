#!/usr/bin/env python
# coding=utf-8
# MessageCoreModel.py
import logging
from BaseCoreModel import BaseCoreModel

class MessageCoreModel(BaseCoreModel):
    def __init__(self, *argc, **argkw):
        super(MessageCoreModel, self).__init__(*argc, **argkw)


    def get_message_detail(self, mes_type,info):
        pass
    
    def insert_message_detail(self, mes_type, info):
        insert_data = {
            "type": mes_type,
            "person_id": info['person_id'],
            "name": info['name'],
            "std_pic_key": info['std_pic_key'],
            "spot": info['spot'],
            "date": info['date'],
            'age': info['age'],
            'sex': info['sex'],
            'formal': info['formal']
        }
        try:
            return self.mongodb.message.info.insert_one(insert_data).inserted_id
        except Exception as e:
            raise DBError("内部错误，插入mongodb.message过程出错")

    def add_to_single_user(self, user, info):
        self.add_to_users([user], info)

    def add_to_users(self,users,info):
        """
        Args:
            info:
                date:
                type:
                message_id
        """
        if users != []:
            for user_id in users:
                # logging.info("user:message:"+str(user_id))
                # logging.info("info : %s"%str(info))
                self.redis.lpush("user:message:"+str(user_id), info)