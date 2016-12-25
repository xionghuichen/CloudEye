#!/usr/bin/env python
# coding=utf-8
# PersonCoreModel.py
import datetime
from BaseCoreModel import BaseCoreModel
from bson import ObjectId
class PersonCoreModel(BaseCoreModel):
    def __init__(self, *argc, **argkw):
        super(PersonCoreModel, self).__init__(*argc, **argkw)
        self.CAMERA = 0
        self.PERSON = 1

    def insert_person_info(self,pic_key, info_data):
        info_data['picture_key_list'] = pic_key
        info_data['formal'] = 0
        info_data['track_list'] = []
        info_data['last_update_time'] = info_data['lost_time']
        info_data['last_update_spot'] = info_data['lost_spot']

        return self.mongodb.person.info.insert_one(info_data).inserted_id

    def get_person_detail(self,person_id):
        """get missing person information by person_id

        Args:
            person_id:

        Returns:
        """
        person_id = ObjectId(person_id)
        result = self.mongodb.person.info.find_one({'_id':person_id})
        return result

    def insert_new_track(self, shoot_type, track_info):
        """ Insert track list into mongodb.
        """
        inserted_id = None
        if shoot_type == self.CAMERA:
           inserted_id = self.mongodb.tracklist.insert_one(track_info).inserted_id
        return inserted_id

    def update_person_info(self, track_id, person_id, coordinate, date):
        update_filter = {'_id':person_id}
        update_data = {
            '$push':{'track_list':track_id},
            '$set':{'last_update_spot':coordinate,'last_update_time':date},
            }
        self.mongodb.person.info.update_one(update_filter, update_data)