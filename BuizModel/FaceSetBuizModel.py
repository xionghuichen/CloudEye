#!/usr/bin/env python
# coding=utf-8
# FaceSetBuizModel.py

import tornado.web
import tornado.gen

from BaseBuizModel import BaseBuizModel
class FaceSetBuizModel(BaseBuizModel):
    def __init__(self, *argc, **argkw):
        super(FaceSetBuizModel, self).__init__(*argc, **argkw)   
    
    def search_person(self,url,callback):
        """ Use face++ to search a person by url.
        Args:
            url: image's url!

        Returns:
            if don't search a possbile face, return None,
            else, return:
            dictory{
                'confidence': probility of these two picture are the same,range[0,100]
                'face_token': the token store in face plus plus databases.
            }
        """
        result = self.face_model.search_person(url)
        if result.has_key('results'):
            del result['results'][0]['user_id']
            callback(result['results'][0])
        else:
            # do not search an possible face
            callback(None)
            