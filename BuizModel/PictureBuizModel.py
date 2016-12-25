#!/usr/bin/env python
# coding=utf-8
# PictureBuizModel.py
import time
import logging

from BaseBuizModel import BaseBuizModel
from config.globalVal import ReturnStruct

class PictureBuizModel(BaseBuizModel):
    def __init__(self, *argc, **argkw):
        super(PictureBuizModel, self).__init__(*argc, **argkw)   

    def _gen_key(self,prefix):
        currentTime = time.time()
        return prefix + "::" + str(currentTime) + '.jpeg'

    def store_pictures(self,imgBytes_list, pic_key, detect_result, callback):
        """Upload pictures (pass as binary stream file) to OSS databases and mongodb[face.info]

        Args:
            imageBytes_list: a list of bianry stream file
            pic_key: set as the key prefix [int]
        Returns:
            key_list: OSS key list which correcpongding every image input
                example:['string','string']
        """
        key_list = []
        if imgBytes_list != []:
            for imgBytes in imgBytes_list:
                key = self._gen_key(str(pic_key))
                logging.info("key is : %s"%key)
                success = self.pic_model.upload_picture(key, imgBytes)
                # add to faceset
                if not success:
                    raise DBError("oss服务器出错！")
                else:
                    key_list.append(key)
        self.face_model.insert_faces_info(key_list, detect_result)
        callback(key_list)
            # [todo] error handler.