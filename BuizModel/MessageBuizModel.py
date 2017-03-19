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
        self.PERSON_SEARCH = 3
        self._inform_latitude = 0.02
        self._inform_longitude = 0.05

    def send_message_factory(self, message_type, info):
        """factory function to create several message information and send it.

        Args:
            message_type:
            infomation: dictory, the key-values depend on different type message.
        """
        factory = [
            self._send_call_help_message,# CALL_HELP
            self._send_camera_search_message,# SEARCH
            self._send_compare_message,# COMPARE
            self._send_person_search_message # PERSON SEARCH
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

    def _send_camera_search_message(self,info):
        self._send_search_message(info,self.SEARCH)

    def _send_person_search_message(self,info):
        self._send_search_message(info,self.PERSON_SEARCH)

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
            'date':info['date'],
            'spot':info['spot'],
            'name':person_detail_info['name'],
            'sex':person_detail_info['sex'],
            'age':person_detail_info['age'],
            'person_id':info['person_id'],
            'formal':person_detail_info['formal'],
            'std_pic_key':person_detail_info['picture_key_list'][0],
            'pic_key':info['pic_key'],
            'confidence':info['confidence'],
            'type':self.COMPARE
        }
        message_id = self.message_model.insert_message_detail( message_info)
        reporter_user_id = person_detail_info['relation_id']
        if reporter_user_id == None:
            # this is a formal case and the relation user has not reigster our system yet.
            pass
        else:
            self.user_model.update_reporter_status(reporter_user_id, True)
        # find the users in range.
        user_id_list = self.location_model.find_user_in_range(info['spot'], self._inform_latitude, self._inform_longitude)
        user_id_list = self._filter_user(user_id_list, reporter_user_id)
        user_id_list = self._filter_user(user_id_list, info['upload_user_id'])
        message_queue_info = {
            "message_id":message_id,
            "date":message_info['date'],
            "type":self.CALL_HELP # this is call help type message to user in range.
        }
        self.message_model.add_to_users(user_id_list, message_queue_info)

    def _send_search_message(self, info, search_type):
        """send search　message to nearby person and reporter.
        
        Args:
            info:
                'person_id'
                'spot'
                'date'
        
        Returns:
        """
        
        person_detail_info = self.person_model.get_person_detail(info['person_id'])
        message_info = {
            'date':info['date'],
            'spot':info['spot'],
            'name':person_detail_info['name'],
            'sex':person_detail_info['sex'],
            'age':person_detail_info['age'],
            'person_id':info['person_id'],
            'formal':person_detail_info['formal'],
            'std_pic_key':person_detail_info['picture_key_list'][0],
            'pic_key':info['pic_key'],
            'confidence':info['confidence'],
            'type':search_type

        }
        message_id = self.message_model.insert_message_detail(message_info)
        reporter_user_id = person_detail_info['relation_id']
        if reporter_user_id == None:
            # this is a formal case and the relation user has not reigster our system yet.
            pass
        else:
            self.user_model.update_reporter_status(reporter_user_id, True)
            # message_queue_info = {
            #     "message_id":message_id,
            #     "date":message_info['date'],
            #     "type":self.SEARCH 
            # }
            # self.message_model.add_to_single_user(reporter_user_id, message_queue_info)
        # find the users in range.
        user_id_list = self.location_model.find_user_in_range(info['spot'], self._inform_latitude, self._inform_longitude)
        user_id_list = self._filter_user(user_id_list, reporter_user_id)
        if search_type == self.PERSON_SEARCH:
            user_id_list = self._filter_user(user_id_list, info['upload_user_id'])
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

        Returns:

        """
        # add to message.info collection
        # find the users in range.
        message_info = {
            'date':info['date'],
            'spot':info['spot'],
            'name':info['name'],
            'sex':info['sex'],
            'age':info['age'],
            'person_id':info['person_id'],
            'formal':0,# default value, 0 for not formal 
            'std_pic_key':info['std_pic_key'],
            'pic_key':'empty',
            'type':self.CALL_HELP
        }
        message_id = self.message_model.insert_message_detail(message_info)
        user_id_list = self.location_model.find_user_in_range(info['spot'], self._inform_latitude, self._inform_longitude)
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
        
    def get_lastest_message(self,spot, max_distance, page, size):
        """Get the lastes update message list filter by spot and max_distance.

        Args:
            spot[list]
            max_distance:[float]
            page:
            size
            
        Returns:
        """
        filter_info = {
            'spot':spot,
            'max_distance':max_distance
        }
        offset = {
            'page':page,
            'size':size
        }
        person_info = self.person_model.get_person_info_by_date(filter_info,offset,2)
        result = []
        for item in person_info:
            person_id = item['_id']
            message = self.message_model.get_message_by_person_id(person_id)
            append_item = {
            'std_pic_key':message['std_pic_key'],# this is just a key, not a list.
            'person_id':message['person_id'],
            'name':message['name'],
            'type':message['type'],
            'date':message['date'],
            'spot':message['spot']
            }
            if not message.has_key('pic_key'):
                append_item['pic_key']= 'empty'
            else:
                append_item['pic_key']=message['pic_key']
            result.append(append_item)
                
        # message_info = self.message_model.get_message_timeline(filter_info,offset)
        # result = []
        # for item in message_info:
        #     logging.info("item in lastest message is %s"%item)
        #     append_item = {
        #     'std_pic_key':item['std_pic_key'],# this is just a key, not a list.
        #     'person_id':item['person_id'],
        #     'name':item['name'],
        #     'type':item['type'],
        #     'date':item['date'],
        #     'spot':item['spot']
        #     }
        #     if not item.has_key('pic_key'):
        #         append_item['pic_key']= 'empty'
        #     else:
        #         append_item['pic_key']=item['pic_key']
        #     result.append(append_item)

        return result