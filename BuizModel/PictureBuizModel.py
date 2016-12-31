#!/usr/bin/env python
# coding=utf-8
# PictureBuizModel.py
import time
import os
import logging
import Image, ImageDraw
from BaseBuizModel import BaseBuizModel
from config.globalVal import ReturnStruct, AP



class PictureBuizModel(BaseBuizModel):
    def __init__(self, *argc, **argkw):
        super(PictureBuizModel, self).__init__(*argc, **argkw)   
        self._pic_type = 'jpeg'

    def gen_key(self, prefix):
        current_time = time.time()
        return prefix + "::" + str(current_time) + '.' + self._pic_type

    def _add_box_to_picture(self, key, detect_info, binary_picture):
        """ add the box with the detect picture.

        Args:
            detect_info:
            binary_picture:

        Returns:
            content: binary file
        """
        path = AP+'static/temp_img/'+key
        top = detect_info['face_rectangle']['top']
        left = detect_info['face_rectangle']['left']
        buttom = detect_info['face_rectangle']['height'] + top
        right = detect_info['face_rectangle']['width'] + left
        box = [(left, top),(right, buttom)]
        file = open(path,'wb')
        file.write(binary_picture)
        file.close()
        file = open(path,'r+b')
        im = Image.open(file)
        draw = ImageDraw.Draw(im)
        draw.rectangle(box,outline=(0,255,0,0))
        im.save(path)
        file.close()
        file = open(path,'r+b')
        content = file.read()
        file.close()
        os.remove(path)
        return content

    def store_pictures(self,binary_picture_list, pic_key, pic_type, detect_result, callback):
        """Upload pictures (pass as binary stream file) to OSS databases and mongodb[face.info]

        Args:
            imageBytes_list: a list of bianry stream file
            pic_key: set as the key prefix [int] + picture_type
            
        Returns:
            key_list: OSS key list which correcpongding every image input
                example:
                    ['camera1::1482730528.67.jpeg']
        """
        key_list = []
        self._pic_type = str(pic_type)
        if binary_picture_list != []:
            for index, binary_picture in enumerate(binary_picture_list):
                key = self.gen_key(str(pic_key))
                # add detect part in origin picture.
                binary_picture = self._add_box_to_picture(key, detect_result[index], binary_picture)
                success = self.pic_model.upload_picture(key, binary_picture)
                # add to faceset
                if not success:
                    raise DBError("oss服务器出错！")
                else:
                    key_list.append(key)
        self.face_model.insert_faces_info(key_list, pic_type, detect_result)
        logging.info("result in store_pictures function is %s"%key_list)
        callback(key_list)
            # [todo] error handler.

    def get_url(self, key):
        logging.info("get url key is :%s"%key)
        return self.pic_model.get_url(key)

    def delete_pictures(self, key, pic_type):
        """delete picture from oss database and face.info in mongodb.

        Args:
            key: picture's key, format:'uploadtype'+id, example:'camera::1'
            pic_type: picture's type, example: 'jpg','jpeg'

        Returns:
            None.
        """
        self._pic_type = pic_type
        key = self.gen_key(str(key))
        self.pic_model.delete_picture_by_key(key)
        self.face_model.delete_faces_info_by_key(key)
        