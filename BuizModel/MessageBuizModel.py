#!/usr/bin/env python
# coding=utf-8
# MessageBuizModel.py

from BaseBuizModel import BaseBuizModel
class MessageBuizModel(BaseBuizModel):
    def __init__(self, *argc, **argkw):
        super(MessageBuizModel, self).__init__(*argc,**argkw)

    def send_message_factory(self, message_type, coordinate ,info, user_id):
        factory = {
            "call_help":_send_call_help_message
        }
        try:
            result = factory[message_type]
        except KeyError as e:

    def _send_call_help_message(self, info, user_id):
        pass
        # add to message.detail collection
        # find the users in range.
        # take apart report user by user_id
        # add to user message queue
