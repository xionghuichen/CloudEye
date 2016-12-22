#!/usr/bin/env python
# coding=utf-8
# UserBuizModel.py
 
import re

from BaseBuizModel import BaseBuizModel
from config.globalVal import regex_dict
from config.globalVal import ReturnStruct
from _exceptions.http_error import DBError
class UserBuizModel(BaseBuizModel):
    def __init__(self, *argc, **argkw):
        super(UserBuizModel, self).__init__(*argc, **argkw)   

    def unique_check(self, telephone):
        """Check if this telephone has exist in database.
        
        Args:
            telephone: register telephone.

        Retruns:
            result:
                0: success.
                1: telephone format error
                2: telephone has been registered.
        """
        message_mapping = [
        "has not been registered before",# 0
        "telephone format error",# 1
        "telephone has been registed"# 2
        ]
        result = ReturnStruct()
        if re.match(regex_dict['telephone'], telephone):
            if self.user_model.is_telephone_exist(telephone):
                result.code = 2
        else:
            result.code = 1
        result.message = message_mapping[result.code]
        result.max_code = len(message_mapping)
        return result

    def register_new_user(self, telephone, password, real_name, nick_name, id_number):
        """register new user to sql database

        Args && example:
            "telephone":"15195861110",
            "password":"zp19950310",
            "real_name":"chenxionghui",
            "nick_name":"burningbear",
            "id_number":"350623199503100053"
  
        Returns:
            ReturnStruct, look message_mapping for detail

        """
        result = ReturnStruct()
        message_mapping = [
        "success",# 0
        "real_name format error", # 1
        "nick_name format error",# 2
        "id_number format error",# 3
        "insert conflit: " # 4
        ]
        if not re.match(regex_dict['real_name'],real_name):
            result.code = 1 
        if re.match(regex_dict['nick_name'],nick_name):
            result.code = 2
        if re.match(regex_dict['id_number'],id_number):
            result.code = 3
        # type check finished.
        has_success, message = self.user_model.insert_record_to_sql(telephone, password, real_name, nick_name, id_number)
        if has_success:
            result.code = 0
        else:
            result.code = 4
            message_mapping[4] = message_mapping[4] + message
        result.message = message_mapping[result.code]
        return result
        # def import_missing_person_list(self,)

    def import_missing_person(self,telephone):
        """ Import missing person which has exist in mongodb databases.

        Args:
            telephone: new user's telephone

        Returns:
        """
        person_list = self.user_model.find_missing_person_list_by_telephone(telephone)
        uid = self.user_model.get_uid_by_telephone(telephone)
        self.user_model.insert_missing_person_by_uid(uid,person_list)

    def remove_user(self, telephone):
        """Remove user by telephone.

        Args:
            telephone: the user's telephone to be removed.


        """
        self.user_model.remove_user_by_telephone(telephone)

    def identify_check(self, telephone, password):
        """check the telephone and password in mysql databases.

        Args:
            telephone
            passowrd

        Returns:
            result: UserInfo object or None
        """
        message_mapping = {
            'login success',# 0
            "no such user",# 1
            "telephone format error", # 2
        }
        result = ReturnStruct()
        if re.match(regex_dict['telephone'], telephone):
            user_info = self.user_model.identify_check(telephone,password)
            if user_info is None:
                result.code = 1
            else:
                result.code = 0
                result.data['user_id'] = user_info.user_id
        else:
            result.code = 2
        result.message = message_mapping[result.code]
        return result

    def get_missing_person_list(self, user_id):
        try:
            return self.user_model.get_missing_person_list(user_id)
        except Exception as e:
            raise DBError("获取遗失用户id列表错误")