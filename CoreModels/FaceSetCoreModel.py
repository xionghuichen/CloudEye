#!/usr/bin/env python
# coding=utf-8
# FaceSetCoreModel.py
import functools

from BaseCoreModel import BaseCoreModel
from _exceptions.http_error import DBError
from facepp_sdk.facepp import APIError, File
import time
def repeat_send(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        again = True
        count = 0
        while(again):
            again = False
            count +=1
            try:
                return method(self, *args, **kwargs)
            except APIError as e:
                print "error happen:",str(e.body)
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
    def search_face(self,url):
        return self.facepp.search(image_url=url,faceset_token=self.temp_faceset_token)

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