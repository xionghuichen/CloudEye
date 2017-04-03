#!/usr/bin/env python
# coding=utf-8
# FaceSetCoreModel.py
import time
import logging
from bson import ObjectId
from BaseCoreModel import BaseCoreModel,repeat_send
from _exceptions.http_error import DBError
from facepp_sdk.facepp import APIError, File
from config.globalVal import FACESET_TOKEN,GROUP_ID, ReturnStruct



class FaceSetCoreModel(BaseCoreModel):
    def __init__(self, *argc, **argkw):
        super(FaceSetCoreModel, self).__init__(*argc, **argkw)  
        self.temp_faceset_token=FACESET_TOKEN
        self.group_id = GROUP_ID
        # 改成group_id
        self.fade_file_path = './demo.jpeg'

    @repeat_send
    def search_person(self, image_path):
        '''
        1. face_token: search由两步变成一步，face_token不用存储了。
        2. search的参数变成base64编码的二进制字符
        {
            "session_id":"session_id",
            "candidates":[
                {
                    "person_id":"person3",
                    "face_id":"1031567119985213439",
                    "confidence":54.90695571899414,
                    “tag”: “new tag”
                },
                {
                    "person_id":"person1",
                    "face_id":"1031587105968553983",
                    "confidence":54.86775207519531,
                    “tag”: “new tag”
                },
                …
                ],
            "errorcode":0,
            "errormsg":"OK"
        }

        '''
        return self.youtu.FaceIdentify(self.group_id, image_path, data_type = 2)

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
                # logging.info("[detect face] threshold is %s, value is %s"%(facequality['threshold'], facequality['value']))
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
        # logging.info("detect_result is %s"%detect_result)
        result = self.mongodb.face.info.insert_many(detect_result)
        # logging.info("insert faces info result is %s "%result.inserted_ids)
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
    def add_new_person(self,person_id,person_name,picture_list):
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
        {   
            u'added': 1, 
            u'errormsg': u'OK', 
            u'face_ids': [u'1989390683606093797', u'1989390686576709605',
            u'1989390689447710693'],
            u'session_id': u'', 
            u'errorcode': 0, 
            u'ret_codes': [-1312, 0, -1312]
        }
        {
            u'group_ids': [], 
            u'suc_face': 0, 
            u'errormsg': u'SDK_IMAGE_FACEDETECT_FAILED', 
            u'session_id': u'', 
            u'errorcode': -1101,
            u'suc_group': 0, 
            u'person_id': u'3'
         }
        """
        mapping = [
            'insert success',
            'has low qualitity picture',
            'insert failed',
        ]
        if type(person_id) == ObjectId:
            person_id = str(person_id)
        to_return = ReturnStruct(mapping)
        picture = picture_list[0]
        result = self.youtu.NewPerson(person_id, picture, [self.group_id], person_name= person_name, tag='', data_type = 2)
        logging.info("new person result is %s"%result)
        # string_token=''
        # for item in face_tokens:
        #     string_token = string_token+item+','
        # string_token = string_token[0:-1]
        if result['errorcode'] == 0 :
            # first picture detect success.
            del picture_list[0]
            if picture_list != []:
                result2 = self.youtu.AddFace(person_id, picture_list, tag='', data_type = 2)
                logging.info("add face result is %s"%result2)
                if result2['errorcode'] == 0:
                    if result2['added'] != len(picture_list):
                        # some picture detect failed
                        def find_all_index(arr,item):
                            return [i for i,a in enumerate(arr) if a != item]
                        invalid_index = find_all_index(result2['ret_codes'],0)

                        def find_all_index_item(arr,arr_index):
                            return [arr[a] for a in arr_index]
                        invalid_msg = find_all_index_item(result2['ret_codes'],invalid_index)
                        to_return.code = 1
                        to_return.data = {'invalid_msg':invalid_msg,'invalid_index':[x + 1 for x in invalid_index]}
                    else:
                        to_return.code = 0
                else:
                    # insert failed
                    to_return.code = 2
                    to_return.data = {'errorcode':result2['errorcode'],'errormsg':result2['errormsg']} 
            else:
                # only one picture.
                to_return.code = 0
        else:
            to_return.code = 2
            to_return.data = {'errorcode':result['errorcode'],'errormsg':result['errormsg']} 
        if to_return.code != 0:
            # delete add new person.
            self.youtu.DelPerson(person_id)
        return to_return

    @repeat_send
    def compare_face(self, person_id, face_content):
        """Compare two face token.

        Args:
            person_id
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
        result = self.youtu.FaceVerify(person_id, face_content,2)
        # result = self.facepp.compare(face_token1=std_face_token, face_token2=detect_face_token)
        # logging.info("result of compare face is %s"%result)
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
