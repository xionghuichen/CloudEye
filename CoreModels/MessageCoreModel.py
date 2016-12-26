#!/usr/bin/env python
# coding=utf-8
# MessageCoreModel.py
import logging
from bson import ObjectId
from BaseCoreModel import BaseCoreModel
def key_gen(prefix_key):
    return "user:message:"+str(prefix_key)

class MessageCoreModel(BaseCoreModel):
    def __init__(self, *argc, **argkw):
        super(MessageCoreModel, self).__init__(*argc, **argkw)


    def get_message_detail(self,message_id):
        return self.mongodb.message.info.find_one({"_id":message_id})
    
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
        Returns:
            None
        """
        if users != []:
            for user_id in users:
                # logging.info("user:message:"+str(user_id))
                # logging.info("info : %s"%str(info))
                self.redis.lpush(key_gen(user_id), info)

    def get_user_message_queue(self,user_id):
        """Get user's location push message by user id.

        Args:
            user_id:
        Returns:
             [
                {
                    "_id" : ObjectId("586008b616b2d61d785e0e93"),
                    "date" : 1482688694.0,
                    "formal" : 0,
                    "name" : "chenxionghui",
                    "person_id" : "585f770e16b2d67f300ec3d8",
                    "std_pic_key" : "43::1482651406.11.jpeg",
                    "age" : 20,
                    "sex" : 0,
                    "type" : 1,
                    "spot" : [ 
                        22.9, 
                        22.9
                    ]
                }
            ]
        """
        key = key_gen(user_id)
        result = self.redis.lrange(key,0,-1)
        if result != []:
            for index, item in enumerate(result):
                item = eval(item)
                result[index] = self.get_message_detail(item['message_id'])
        return result
 

