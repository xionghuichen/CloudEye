#!/usr/bin/env python
# coding=utf-8
# FaceSetCoreModel.py
import functools
import logging
from BaseCoreModel import BaseCoreModel
from _exceptions.http_error import DBError
from facepp_sdk.facepp import APIError, File
from config.globalVal import FACESET_TOKEN
import time
def repeat_send(method):
    """this decorator for face++ request. 
    Beacuse face++ free appkey often send high concurrency error.
    after add this decorator, request will send repeatly until response successfully.
    
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        again = True
        count = 0
        while again :
            again = False
            count +=1
            try:
                logging.info("trying connecting to face++")
                return method(self, *args, **kwargs)
            except APIError as e:
                logging.info("error happen:%s"%str(e.body))
                again = True
                if count > 10:
                    raise DBError("face plus plus database error!")
                else:
                    time.sleep(1)
    return wrapper

class FaceSetCoreModel(BaseCoreModel):
    def __init__(self, *argc, **argkw):
        super(FaceSetCoreModel, self).__init__(*argc, **argkw)  
        self.temp_faceset_token=FACESET_TOKEN
        self.fade_file_path = './demo.jpeg'

    @repeat_send
    def search_face(self, face_token):
        return self.facepp.search(face_token=face_token,
            faceset_token=self.temp_faceset_token)

    @repeat_send
    def detect_faces(self,binary_picture):
        """ detect faces from an byte image, return faces information dictories

        Args:
            binary_picture:[list]

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
        result = self.facepp.detect(image_file=File(path=self.fade_file_path, content=binary_picture), return_attributes='facequality')
        result = result['faces']
        sub_val = 60
        if result != []:
            count = 0
            # filter all of face which is low quality.
            for item in result:
                facequality = item['attributes']['facequality']
                logging.info("[detect face] threshold is %s, value is %s"%(facequality['threshold'], facequality['value']))
                if facequality['threshold'] - sub_val > facequality['value']:
                    # logging.info("low quality, threshold is %s, value is %s"%(threshold - sub_val, value))
                    del result[count]
                else:
                    result[count]['attributes']['facequality'] = facequality['value'] - facequality['threshold'] + sub_val
                    count += 1
        return result

    def insert_faces_info(self, pic_key, pic_type, detect_result):
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
            detect_result[index]['pic_type'] = pic_type
        logging.info("detect_result is %s"%detect_result)
        result = self.mongodb.face.info.insert_many(detect_result)
        logging.info("insert faces info result is %s "%result.inserted_ids)
        return result.inserted_ids

    def delete_faces_info_by_key(self, key):
        self.mongodb.face.info.delete_many({'picture_key':key})

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

    @repeat_send
    def compare_face(self, std_face_token, detect_face_token):
        """Compare two face token.

        Args:
            std_face_token
            detect_face_token

        Returns:
            {
              "time_used": 473,
              "confidence": 96.46,
              "thresholds": {
                "1e-3": 65.3,
                "1e-5": 76.5,
                "1e-4": 71.8
              },
              "request_id": "1469761507,07174361-027c-46e1-811f-ba0909760b18"
            }
        """
        result = self.facepp.compare(face_token1=std_face_token, face_token2=detect_face_token)
        logging.info("result of compare face is %s"%result)
        return result
        
    def get_face_info(self, pic_key):
        """

        Args:
            pic_key: picture_key
        Returns:
        {
            "_id" : ObjectId("5860bebb16b2d6496b363ab0"),
            "attributes" : {
                "facequality" : 20.678
            },
            "face_token" : "c16309f7c33738c59fad4044cd34c51c",
            "picture_key" : "camera1::1482735290.95.jpeg",
            "face_rectangle" : {
                "width" : 180,
                "top" : 88,
                "height" : 180,
                "left" : 99
            }
        }
        """
        return self.mongodb.face.info.find_one({'picture_key':pic_key})
