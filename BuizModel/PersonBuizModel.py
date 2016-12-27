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

    def update_person_status(self,shoot_type, event_info, shooter_info = None):
        """update databases infomastion of person_id
        1. update track list infomation 
        2. update person.info [last track list; last update time and last update spot]
        
        Args:
            person_id: missing person id
            shoot_type: camera or person
            coordinate: location of shoot spot
            confidence: 
            pic_key:
            shooter_info:
                user_id:
                description:
        """
        # result = self.person_model.get_person_detail(person_id_obj)
        # if result != None:
        person_id_obj = ObjectId(event_info['person_id'])
        info_data = {}
        info_data['confidence'] = event_info['confidence']
        info_data['coordinate'] = event_info['coordinate']
        info_data['person_id'] = person_id_obj
        info_data['pic_key'] = event_info['pic_key']
        info_data['date'] = event_info['date']
        user_info = self.user_model.get_user_info(shooter_info['user_id'])
        shooter_info['user_nick_name'] = user_info['nick_name']
        track_id = self.person_model.insert_new_track(shoot_type, info_data, shooter_info)
        self.person_model.update_person_info(track_id, person_id_obj, event_info['coordinate'], event_info['date'])

    def get_person_std_pic(self, person_id):
        """get a messing person's standard picture [upload by reporter] by person_id.

        Args:
            person_id:

        Returns:
            face_token:
        """
        person_info = self.person_model.get_person_detail(person_id)
        pri_picture_key = person_info['picture_key_list'][0]
        face_info = self.face_model.get_face_info(pri_picture_key)
        return face_info['face_token']

    def get_lastest_case(self, spot, max_distance):
        """Get the lastes case filter by spot and max_distance.

        Args:
            spot[list]
            max_distance:[float]
        Returns:
        """
        filter_info = {
            'spot':spot,
            'max_distance':max_distance
        }
        self.person_model.get_tracks_detail(self, self.POLICE, filter_info)
