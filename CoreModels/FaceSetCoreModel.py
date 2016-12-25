#!/usr/bin/env python
# coding=utf-8
# FaceSetCoreModel.py
import functools
import logging
from BaseCoreModel import BaseCoreModel
from _exceptions.http_error import DBError
from facepp_sdk.facepp import APIError, File
import time
def repeat_send(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        again = True
        count = 0
        while again :
            again = False
            count +=1
            try:
                return method(self, *args, **kwargs)
            except APIError as e:
                logging.info("error happen:%s"%str(e.body))
                again = True
                if count > 10:
                    raise DBError("face plus plus databases error!")
                else:
                    time.sleep(2)
    return wrapper

class FaceSetCoreModel(BaseCoreModel):
    def __init__(self, *argc, **argkw):
        super(FaceSetCoreModel, self).__init__(*argc, **argkw)  
        self.temp_faceset_token='468d4f8ba70bddbf41aa9b3d2deeb04a'
        self.fade_file_path = './demo.jpeg'

    @repeat_send
    def search_face(self, face_token):
        return self.facepp.search(face_token=face_token,
            faceset_token=self.temp_faceset_token)

    @repeat_send
    def detect_faces(self,imgBytes):
        """ detect faces from an byte image, return faces information dictories

        Args:
            imgBytes:[list]

        Returns:
            return a list, the following is the element of the array:
            {
                'attributes': 
                    {
                        'facequality': # if value is bigger than threshold, the image is suitable to detect. 
                            {
                                'threshold': 70.1,
                                'value': 90.778
                            }
                    },
                'face_rectangle':# image size. 
                    {
                        'height': 180,
                        'left': 99,
                        'top': 88,
                        'width': 180
                    },
              'face_token': '24f7e27d20113c0d398a33486260e348'# face identify
            }
        """
        result = self.facepp.detect(image_file=File(path=self.fade_file_path, content=imgBytes), return_attributes='facequality')
        result = result['faces']
        if result != []:
            count = 0
            # filter all of face which is low quality.
            for item in result:
                facequality = item['attributes']['facequality']
                if facequality['threshold'] > facequality['value']:
                    del result[count]
                else:
                    result[count]['attributes']['facequality'] = facequality['value'] - facequality['threshold']
                    count += 1
        return result

    def insert_faces_info(self, pic_key, detect_result):
        """Intert face information into mongodb.

        Args:
            pic_key: oss key list.
            detect_result:
                'face_rectangle':# image size. 
                        {
                            'height': 180,
                            'left': 99,
                            'top': 88,
                            'width': 180
                        },
                  'face_token': '24f7e27d20113c0d398a33486260e348'# face identify
        Returns:
            [ObjectId('...'), ObjectId('...')]
        """
        for index, item in enumerate(detect_result):
            detect_result[index]['picture_key'] = pic_key[index]

        logging.info("detect_result is %s"%detect_result)
        result = self.mongodb.face.info.insert_many(detect_result)
        logging.info("insert faces info result is %s "%result.inserted_ids)
        return result.inserted_ids

    @repeat_send
    def set_person_id_to_face(self,person_id,face_token):
        """label face with person_id.

        Args:
            person_id
            face_token

        Returns:
        {
            "user_id": "234723hgfd",
            "request_id": "1470481019,fd7c8a99-93fc-45d4-9eb6-9aaf6fb59f32",
            "time_used": 15,
            "face_token": "4dc8ba0650405fa7a4a5b0b5cb937f0b"
        }
        """
        result = self.facepp.face.setuserid(face_token=face_token,user_id=person_id)
        logging.info("set person_id to face:%s \n"%result)
        return result

        
    @repeat_send
    def add_faces_to_faceset(self,face_tokens):
        """Add face tokens to faceset;

        Args:
            face_tokens list.

        Returns:
        {
            "faceset_token": "42fb0d5bf81c5ac57c52344dddc3e7c9",
            "time_used": 479,
            "face_count": 1,
            "face_added": 1,
            "request_id": "1470293555,78637cd1-f773-47c6-8ba4-5af7153e4e00",
            "outer_id": "uabREDWZvshpHISwVsav",
            "failure_detail": []
        } 
        """
        string_token=''
        for item in face_tokens:
            string_token = string_token+item+','
        string_token = string_token[0:-1]
        result = self.facepp.faceset.addface(faceset_token=self.temp_faceset_token,face_tokens=string_token)
        return result