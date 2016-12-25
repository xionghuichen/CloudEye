#!/usr/bin/env python
# coding=utf-8
# MessageBuizModel.py
import logging
from BaseBuizModel import BaseBuizModel
class MessageBuizModel(BaseBuizModel):
    def __init__(self, *argc, **argkw):
        super(MessageBuizModel, self).__init__(*argc,**argkw)
        self.CALL_HELP = 0
        self._inform_distance = 4

    def send_message_factory(self, message_type, coordinate ,info, user_id):
        factory = [
            self._send_call_help_message,# CALL_HELP
        ]
        result = factory[message_type](info, user_id)

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

    def _send_call_help_message(self, info, user_id):
        """send message to nearby person and police. 
        
        Args:
            info:
                'name': 
                'std_pic_key': missing person's primary picture
                'spot': the place the person has been found
                'date': the time [unix time] the person has been found
        """
        # add to message.info collection
        message_id = self.message_model.insert_message_detail(self.CALL_HELP, info)
        # find the users in range.
        user_id_list = self.location_model.find_user_in_range(info['spot'], self._inform_distance)

        # take apart report user by user_id
        user_id_list = self._filter_user(user_id_list, user_id)
        # add to user message queue  
        logging.info("user_id_list is %s"%user_id_list)  
        message_queue_info = {
            "message_id":message_id,
            "date":info['date'],
            "type":self.CALL_HELP
        }
        self.message_model.add_to_users(user_id_list, message_queue_info)
        