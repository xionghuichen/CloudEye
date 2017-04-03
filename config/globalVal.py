# globalVal.py
import os
import logging
AP = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))+'/'
regex_dict = {
'telephone':ur"^13[\d]{9}$|^14[5,7]{1}\d{8}$|^15[^4]{1}\d{8}$|^17[0,6,7,8]{1}\d{8}$|^18[\d]{9}$\Z",
'real_name':ur"[\u4e00-\u9fa5\w\s]{1,16}$",
'nick_name':ur"[\u4e00-\u9fa5\w\s]{4,16}$", 
'id_number':ur"/^[1-9]\d{7}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}$|^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}([0-9]|X)$/",
}        
class ReturnStruct(object):
    def __init__(self, message_mapping = ['default message']):
        self.max_code = len(message_mapping)
        self.code = 0
        self.message_mapping = message_mapping
        self.data = {}

    def merge_info(self,new_struct):
        self.code = self.max_code + new_struct.code
        self.max_code = self.max_code + new_struct.max_code
        self.data = dict(self.data, **new_struct.data)
        self.message_mapping.extend(new_struct.message_mapping)

    def print_info(self,tag ='default'):
        logging.info("print return struct, tag = %s...."%tag)
        logging.info("max_code:%s"%self.max_code)
        logging.info("code: %s"%self.code)
        logging.info("message_mapping: %s"%self.message_mapping)
        logging.info("data: %s"%self.data)

PLICEMAN_ID = 0
GROUP_ID = 'group2'
FACESET_TOKEN='3448ba215c7d3933ed78f418aa85bb35'
MAX_WORKERS = 1000
