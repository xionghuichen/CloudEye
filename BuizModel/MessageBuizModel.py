#!/usr/bin/env python
# coding=utf-8
# MessageBuizModel.py
import logging
import datetime
import time
from BaseBuizModel import BaseBuizModel
class MessageBuizModel(BaseBuizModel):
    def __init__(self, *argc, **argkw):
        super(MessageBuizModel, self).__init__(*argc,**argkw)
        self.CALL_HELP = 0
        self.SEARCH = 1
        self.COMPARE = 2
        self._inform_distance = 4

    def send_message_factory(self, message_type, info):
        factory = [
            self._send_call_help_message,# CALL_HELP
            self._send_search_message,#SEARCH
            self._send_compare_message#COMPARE
        ]
        result = factory[message_type](info)

    def _filter_user(self,users,user):
        """Delete user_id from users if user_id in users.

        Args:
            users: user_id list
            user: user_id to be deleted.

        Returns:
            new_user_list
        """
        def list_filter(list_unit):
            if list_unit != user:
                return list_unit
        return filter(list_filter,users)

    def _send_compare_message(self,info):
        """send message to nearby person and reporter, except the upload user.

        Args:
            info:
                'person_id':
                'spot':
                'date':
                'upload_user_id':
        Returns:
        """
        person_detail_info = self.person_model.get_person_detail(info['person_id'])
        message_info = {
            'formal':0,
            'date':info['date'],
            'spot':info['spot'],
            'name':person_detail_info['name'],
            'sex':person_detail_info['sex'],
            'age':person_detail_info['age'],
            'person_id':info['person_id'],
            'formal':person_detail_info['formal'],
            'std_pic_key':person_detail_info['picture_key_list'][0]

        }
        message_id = self.message_model.insert_message_detail(self.COMPARE, message_info)
        reporter_user_id = person_detail_info['relation_id']
        if reporter_user_id == None:
            # this is a formal case and the relation user has not reigster our system yet.
            pass
        else:
            self.user_model.update_reporter_status(reporter_user_id)
            # message_queue_info = {
            #     "message_id":message_id,
            #     "date":message_info['date'],
            #     "type":self.SEARCH 
            # }
            # self.message_model.add_to_single_user(reporter_user_id, message_queue_info)
        # find the users in range.
        user_id_list = self.location_model.find_user_in_range(info['spot'], self._inform_distance)
        user_id_list = self._filter_user(user_id_list, reporter_user_id)
        user_id_list = self._filter_user(user_id_list, info['upload_user_id'])
        message_queue_info = {
            "message_id":message_id,
            "date":message_info['date'],
            "type":self.CALL_HELP # this is call help type message to user in range.
        }
        self.message_model.add_to_users(user_id_list, message_queue_info)


    def _send_search_message(self, info):
        """send message to nearby person and reporter.
        
            info:
                'person_id'
                'spot'
                'date'

        """
        person_detail_info = self.person_model.get_person_detail(info['person_id'])
        message_info = {
            'formal':0,
            'date':info['date'],
            'spot':info['spot'],
            'name':person_detail_info['name'],
            'sex':person_detail_info['sex'],
            'age':person_detail_info['age'],
            'person_id':info['person_id'],
            'formal':person_detail_info['formal'],
            'std_pic_key':person_detail_info['picture_key_list'][0]

        }
        message_id = self.message_model.insert_message_detail(self.SEARCH, message_info)
        reporter_user_id = person_detail_info['relation_id']
        if reporter_user_id == None:
            # this is a formal case and the relation user has not reigster our system yet.
            pass
        else:
            self.user_model.update_reporter_status(reporter_user_id)
            # message_queue_info = {
            #     "message_id":message_id,
            #     "date":message_info['date'],
            #     "type":self.SEARCH 
            # }
            # self.message_model.add_to_single_user(reporter_user_id, message_queue_info)
        # find the users in range.
        user_id_list = self.location_model.find_user_in_range(info['spot'], self._inform_distance)
        user_id_list = self._filter_user(user_id_list, reporter_user_id)
        message_queue_info = {
            "message_id":message_id,
            "date":message_info['date'],
            "type":self.CALL_HELP # this is call help type message to user in range.
        }
        self.message_model.add_to_users(user_id_list, message_queue_info)


    def _send_call_help_message(self, info):
        """send message to nearby person and police. 
        
        Args:
            info:
                'name': 
                'std_pic_key': missing person's primary picture
                'spot': the place the person has been found
                'date': the time [unix time] the person has been found
                'age'
                'sex'
                'person_id'
                'reporter_user_id': the user who report the call help information.
        """
        # add to message.info collection
        # find the users in range.
        message_info = {
            'formal':0,
            'date':info['date'],
            'spot':info['spot'],
            'name':info['name'],
            'sex':info['sex'],
            'age':info['age'],
            'person_id':info['person_id'],
            'formal':0,# default value, 0 for not formal 
            'std_pic_key':info['std_pic_key']

        }
        message_id = self.message_model.insert_message_detail(self.CALL_HELP, message_info)
        user_id_list = self.location_model.find_user_in_range(info['spot'], self._inform_distance)
        reporter_user_id = info['reporter_user_id']
        # take apart report user by user_id
        user_id_list = self._filter_user(user_id_list, reporter_user_id)
        # add to user message queue  
        logging.info("user_id_list is %s"%user_id_list)  
        message_queue_info = {
            "message_id":message_id,
            "date":info['date'],
            "type":self.CALL_HELP
        }
        self.message_model.add_to_users(user_id_list, message_queue_info)
        