#!/usr/bin/env python
# coding=utf-8
# OSSCoreModel.py
import logging
from BaseCoreModel import BaseCoreModel
import time
class OSSCoreModel(BaseCoreModel):
    def __init__(self, *argc, **argkw):
        super(OSSCoreModel, self).__init__(*argc, **argkw)  
        self._sign_time = 3600
    
    def upload_picture(self,key,binary_picture):
        """Upload single picture to OSS databases.

        Args:
            imageBytes: a bianry stream file
        
        Returns:
            true for success, false for failed.
        """
        logging.info("uploading picture...")
        result = self.ali_bucket.put_object(key, binary_picture)
        if result.status != 200:
            return False
        return True

    def delete_picture_by_key(self,key):
        """Delete picture which key is parameter 'key'

        Args:

        Returns:
        """
        result = self.ali_bucket.delete_object(key)
        if result.status != 200:
            return False
        return True

    def get_url(self,key):
        return self.ali_bucket.sign_url('GET', key, self._sign_time)