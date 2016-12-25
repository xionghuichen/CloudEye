#!/usr/bin/env python
# coding=utf-8
# PersonBuizModel.py
import time
import datetime
from bson import ObjectId
from BaseBuizModel import BaseBuizModel
from config.globalVal import ReturnStruct


class PersonBuizModel(BaseBuizModel):
    def __init__(self, *argc, **argkw):
        super(PersonBuizModel, self).__init__(*argc, **argkw) 

    def store_new_person(self,pic_key_list,detect_result,info_data, user_id):
        """after upload all of resourse, We should store those record into databases.

        Args:
            pic_key_list: missing person' picture key list
            detect_result: detect result dictory, include faces location and face_token.
            info_data:
                'name':self.get_argument('name'),
                'sex':int(self.get_argument('sex')),
                'age':int(self.get_argument('age')),
                'relation_telephone':self.get_argument('relation_telephone'),
                'relation_name':self.get_argument('relation_name'),
                'relation_id': user_id,
                'lost_time':self.get_argument('lost_time'),
                'lost_spot':self.get_argument('lost_spot'),
                'description':self.get_argument('description')
            user_id:
        Returns:
            person_id
        """
        # add person_info in mongodb.[get person_id]
        person_id = self.person_model.insert_person_info(pic_key_list, info_data)
        # add setUserId
        face_token_list = []
        for item in detect_result:
            self.face_model.set_person_id_to_face(person_id,item['face_token'])
            face_token_list.append(item['face_token'])
        self.face_model.add_faces_to_faceset(face_token_list)
        # add missing_person_id into person.missing collection
        self.user_model.insert_missing_person_by_uid(user_id,[person_id])
        return person_id

    def _track_info_creator(self, shoot_type, info_data):
        track_info = {}
        if shoot_type == self.CAMERA:
            track_info = {
                # 'name':info_data['name'],
                # 'sex':info_data['sex'],
                # 'age':info_data['age'],
                # 'person_'
                # 'shoot_user_id':person_id_obj,
                'pic_key':info_data['pic_key'],
                'type':self.CAMERA,
                'confidence':info_data['confidence'],
                'coordinate':info_data['coordinate'],
                'date':info_data['date']
            }
        return track_info

    def update_person_status(self, person_id, shoot_type, coordinate, confidence, pic_key, shoot_user_id = None):
        """update databases infomastion of person_id
        1. update track list infomation 
        2. update person.info [last track list; last update time and last update spot]
        """
        # result = self.person_model.get_person_detail(person_id_obj)
        # if result != None:
        person_id_obj = ObjectId(person_id)
        info_data = {}
        info_data['confidence'] = confidence
        info_data['coordinate'] = coordinate
        info_data['person_id'] = person_id_obj
        info_data['pic_key'] = pic_key
        info_data['date'] = float(time.mktime(datetime.datetime.now().timetuple()))

        track_info = self._track_info_creator(shoot_type, info_data)
        track_id = self.person_model.insert_new_track(shoot_type, track_info)
        self.person_model.update_person_info(track_id, person_id_obj, coordinate, info_data['date'])
