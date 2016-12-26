#!/usr/bin/env python
# coding=utf-8
# PictureBuizModel.py
import time
import logging

from BaseBuizModel import BaseBuizModel
from config.globalVal import ReturnStruct


def gen_key(prefix):
    current_time = time.time()
    return prefix + "::" + str(current_time) + '.jpeg'

class PictureBuizModel(BaseBuizModel):
    def __init__(self, *argc, **argkw):
        super(PictureBuizModel, self).__init__(*argc, **argkw)   

    def store_pictures(self,binary_picture_list, pic_key, detect_result, callback):
        """Upload pictures (pass as binary stream file) to OSS databases and mongodb[face.info]

        Args:
            imageBytes_list: a list of bianry stream file
            pic_key: set as the key prefix [int]
        Returns:
            key_list: OSS key list which correcpongding every image input
                example:
                    ['camera1::1482730528.67.jpeg']
        """
        key_list = []
        if binary_picture_list != []:
            for binary_picture in binary_picture_list:
                key = gen_key(str(pic_key))
                success = self.pic_model.upload_picture(key, binary_picture)
                # add to faceset
                if not success:
                    raise DBError("oss服务器出错！")
                else:
                    key_list.append(key)
        self.face_model.insert_faces_info(key_list, detect_result)
        logging.info("result in store_pictures function is %s"%key_list)
        callback(key_list)
            # [todo] error handler.

    def get_url(self, key):
        return self.pic_model.get_url(key)