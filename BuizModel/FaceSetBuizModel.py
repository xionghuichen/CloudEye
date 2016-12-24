#!/usr/bin/env python
# coding=utf-8
# FaceSetBuizModel.py


from BaseBuizModel import BaseBuizModel
from config.globalVal import ReturnStruct

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
        result = self.face_model.search_face(url)
        if result.has_key('results'):
            # del result['results'][0]['user_id']
            callback(result['results'][0])
        else:
            # do not search an possible face
            callback(None)
    

    def detect_img_list(self, imgBytes_list,callback):
        """detect face of a image list through face++, get face_token list as a result.

        Args:
            imgBytes_list

        Returns:
            ReturnStruct.
                if code == 1: detect error, return low quality picture number in data['count']
                if code == 0: return the face token list in data. 
        """
        message_mapping =[
            'detect success',
            'low quality picture'
        ]
        to_return = ReturnStruct(message_mapping)
        detect_result_list = []
        count = 0
        for imgBytes in imgBytes_list:
            # detect.
            detect_result = self.face_model.detect_faces(imgBytes)
            if detect_result == []:
                # the quality of pictures is too to detect any faces
                to_return.code = 1
                to_return.data = {'count':count}
                break
            else:
                max_index = 0
                max_quality = 0
                item_count = 0
                # get the highest quality face.
                for item in detect_result:
                    if item['attributes']['facequality'] > max_quality:
                        max_index = item_count
                        max_quality = item['attributes']['facequality']
                    item_count += 1
                detect_result = detect_result[max_index]
                # appends. 
                detect_result_list.append(detect_result)
            count +=1

        if to_return.code != 1:
            to_return.data = {'detect_result_list':detect_result_list}        
        callback(to_return)