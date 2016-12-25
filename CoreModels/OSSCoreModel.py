#!/usr/bin/env python
# coding=utf-8
# OSSCoreModel.py

from BaseCoreModel import BaseCoreModel
import time
class OSSCoreModel(BaseCoreModel):
    def __init__(self, *argc, **argkw):
        super(OSSCoreModel, self).__init__(*argc, **argkw)  

    def upload_picture(self,key,imgBytes):
        """Upload single picture to OSS databases.

        Args:
            imageBytes: a bianry stream file
        
        Returns:
            true for success, false for failed.
        """
        result = self.ali_bucket.put_object(key, imgBytes)
        if result.status != 200:
            return False
        return True