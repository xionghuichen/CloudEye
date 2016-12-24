# globalVal.py
import os
AP = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))+'/'
regex_dict = {
'telephone':ur"^13[\d]{9}$|^14[5,7]{1}\d{8}$|^15[^4]{1}\d{8}$|^17[0,6,7,8]{1}\d{8}$|^18[\d]{9}$\Z",
'real_name':ur"[\u4e00-\u9fa5\w\s]{1,16}$",
'nick_name':ur"[\u4e00-\u9fa5\w\s]{4,16}$", 
'id_number':ur"/^[1-9]\d{7}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}$|^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}([0-9]|X)$/",
}        
class ReturnStruct(object):
    def __init__(self, message_mapping = []):
        self.max_code = len(message_mapping)
        self.code = 0
        self.message_mapping = message_mapping
        self.data = {}

    def mergeInfo(self,new_struct):
        self.code = self.max_code + new_struct.code
        self.max_code = self.max_code + new_struct.max_code
        self.data = new_struct.data
        self.message_mapping.extend(new_struct.message_mapping)

    def print_info(self,tag ='default'):
        print "print return struct, tag = %s...."%tag
        print "max_code:",self.max_code
        print "code:",self.code
        print "message_mapping:",self.message_mapping
        print "data:",self.data