#!/usr/bin/env python
# coding=utf-8
# PersonCoreModel.py
import datetime
from BaseCoreModel import BaseCoreModel
class PersonCoreModel(BaseCoreModel):
    def __init__(self, *argc, **argkw):
        super(PersonCoreModel, self).__init__(*argc, **argkw)

    def insert_person_info(self,pic_key, info_data):
        info_data['picture_key_list'] = pic_key
        info_data['formal'] = 0
        info_data['track_list'] = []
        info_data['last_updata_time'] = info_data['lost_time']
        info_data['last_update_spot'] = info_data['lost_spot']
        return self.mongodb.person.info.insert_one(info_data).inserted_id
