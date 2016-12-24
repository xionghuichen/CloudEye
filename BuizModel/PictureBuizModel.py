#!/usr/bin/env python
# coding=utf-8
# PictureBuizModel.py
import time

from BaseBuizModel import BaseBuizModel
from config.globalVal import ReturnStruct

class PictureBuizModel(BaseBuizModel):
    def __init__(self, *argc, **argkw):
        super(PictureBuizModel, self).__init__(*argc, **argkw)   

    def _gen_key(self,prefix):
        currentTime = time.time()
        return prefix + "::" + str(currentTime) + '.jpeg'

    def store_pictures(self,imgBytes_list,user_id,callback):
        """Upload pictures (pass as binary stream file) to OSS databases.

        Args:
            imageBytes_list: a list of bianry stream file
            user_id: set as the key prefix
        Returns:
            key_list: OSS key list which correcpongding every image input
                example:['string','string']
        """
        key_list = []
        if imgBytes_list != []:
            for imgBytes in imgBytes_list:
                key = self._gen_key(user_id)
                success = self.pic_model.upload_picture(key,imgBytes)
                if not success:
                    raise DBError("oss服务器出错！")
                else:
                    key_list.append(key)
        callback(key_list)
            # [todo] error handler.