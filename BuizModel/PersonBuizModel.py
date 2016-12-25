#!/usr/bin/env python
# coding=utf-8
# PersonBuizModel.py

from BaseBuizModel import BaseBuizModel
from config.globalVal import ReturnStruct

class PersonBuizModel(BaseBuizModel):
    def __init__(self, *argc, **argkw):
        super(PersonBuizModel, self).__init__(*argc, **argkw) 

    def store_new_person(self,pic_key,detect_result,info_data, user_id):
        """after upload all of resourse, We should store those record into databases.

        Args:
            pic_key: missing person' picture key list
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
            None
        """
        # add person_info in mongodb.[get person_id]
        person_id = self.person_model.insert_person_info(pic_key, info_data)
        # add to faceset
        self.face_model.insert_faces_info(pic_key, detect_result)
        # add setUserId
        face_token_list = []
        for item in detect_result:
            self.face_model.set_person_id_to_face(person_id,item['face_token'])
            face_token_list.append(item['face_token'])
        self.face_model.add_faces_to_faceset(face_token_list)
        # add missing_person_id into person.missing collection
        self.user_model.insert_missing_person_by_uid(user_id,[person_id])