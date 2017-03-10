#!/usr/bin/env python
# coding=utf-8
# FaceSetBuizModel.py

import logging
from BaseBuizModel import BaseBuizModel
from config.globalVal import ReturnStruct

class FaceSetBuizModel(BaseBuizModel):
    def __init__(self, *argc, **argkw):
        super(FaceSetBuizModel, self).__init__(*argc, **argkw)   
        self.LOW_CONFIDENCE = 0
        self.MIDDLE_CONFIDENCE = 1
        self.HIGH_CONFIDENCE = 2
        self.VERY_HIGH_CONFIDENCE = 3
        self.SUPER_HIGH_CONFIDENCE = 4

    def _calculate_level(self,levels,confidence):
        """Calculate confidence level

        Args:
            levels: should has following keys (actually, this parameter come from face++):
                le-3:low confidence
                le-4:middle confidence
                le-5: high confidence
            confidence: a float stand for confidence value.
        Returns:
            level: confidence level.
        """
        level1 = float(levels['1e-3'])
        level2 = float(levels['1e-4'])
        level3 = float(levels['1e-5'])
        level4 = level3 + (level3 - level2)/2
        level = self.LOW_CONFIDENCE
        if confidence >= level4:
            level = self.SUPER_HIGH_CONFIDENCE
        elif confidence >= level3:
            level =  self.VERY_HIGH_CONFIDENCE
        elif confidence >= level2:
            level = self.HIGH_CONFIDENCE
        elif confidence >= level1:
            level = self.MIDDLE_CONFIDENCE
        return level

    def search_person(self,face_token, callback):
        """ Use face++ to search a person by url.
        Args:
            face_token: image's url!

        Returns:
            if don't search a possbile face, return None,
            else, return:
                {
                        "confidence": 96.46,
                        "user_id": "234723hgfd",
                        "face_token": "4dc8ba0650405fa7a4a5b0b5cb937f0b"
                }
        """
        result = self.face_model.search_face(face_token)
        if result.has_key('results'):
            confidence = result['results'][0]['confidence']
            level = self._calculate_level(result['thresholds'],confidence)
            to_return = {
                'level':level, 
                'confidence':confidence,
                'info':result['results'][0]
            }
            
            logging.info("result of search, %s"%to_return)
            callback(to_return)
        else:
            # do not search an possible face
            callback(None)
    
    def detect_img_list(self, binary_picture_list, only, callback):
        """detect face of a image list through face++, get face_token list as a result.

        Args:
            binary_picture_list

        Returns:
            ReturnStruct.
                if code == 1: detect error, return low quality picture number in data['count']
                if code == 0: return the faces list in data. 
                    example: 
                        [
                            {
                                u'attributes': {
                                    u'facequality': 20.67800000000001
                                },
                                u'face_token': u'44f2a168abdb7770203ae924f3bfaa6c',
                                u'face_rectangle': {
                                    u'width': 180,
                                    u'top': 88,
                                    u'height': 180,
                                    u'left': 99
                                }
                            },
                            {
                                u'attributes': {
                                    u'facequality': 12.599000000000004
                                },
                                u'face_token': u'6eb1852aceb54bb1f69cd66863e0718a',
                                u'face_rectangle': {
                                    u'width': 138,
                                    u'top': 176,
                                    u'height': 138,
                                    u'left': 252
                                }
                            }
                        ]
        """
        message_mapping =[
            'detect all pictures successful',
            'has low quality picture'
        ]
        to_return = ReturnStruct(message_mapping)
        detect_result_list = []
        count = 0
        for binary_picture in binary_picture_list:
            # detect.
            detect_result = self.face_model.detect_faces(binary_picture)
            if detect_result == []:
                # the quality of pictures is too to detect any faces
                to_return.code = 1
                to_return.data = {'failed_detect_count':count}
                break
            else:
                if only:
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
                else:
                    detect_result_list.extend(detect_result)
            count +=1

        if to_return.code != 1:
            to_return.data = {'detect_result_list':detect_result_list}        
        logging.info("[detect result list] detect img list function : %s"%detect_result_list)
        callback(to_return)

    def compare_face(self, std_face_token, detect_face_token, callback):
        """Compare two face token.

        Args:
            std_face_token
            detect_face_token

        Returns:
            confidence: 
                level:
                    self.LOW_CONFIDENCE = 0
                    self.MIDDLE_CONFIDENCE = 1
                    self.HIGH_CONFIDENCE = 2
                    self.VERY_HIGH_CONFIDENCE = 3

                confidence: float
        """
        result = self.face_model.compare_face(std_face_token, detect_face_token)
        confidence = result['confidence']
        level = self._calculate_level(result['thresholds'],confidence)
        logging.info("result of compare, the confidence is %s"%confidence)
        callback({'level':level,'confidence':confidence})