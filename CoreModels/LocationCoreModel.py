#!/usr/bin/env python
# coding=utf-8
# LocationCoreModel.py

from BaseCoreModel import BaseCoreModel
import logging
class LocationCoreModel(BaseCoreModel):
    def __init__(self, *argc, **argkw):
        super(LocationCoreModel, self).__init__(*argc, **argkw)

    def find_user_in_range(self, coordinate,latitude, longitude):
        cursor = self.mongodb.user.online.find({
                'coordinate':{
                    '$geoWithin':{
                        '$box':[[coordinate[0]+latitude,coordinate[1]+longitude],[coordinate[0]-latitude,coordinate[1]-longitude]]
                    }
                }
            })
        user_id_list = []
        if cursor != None:
            for item in cursor:
                user_id_list.append(item['user_id'])
        return user_id_list

    def update_user_location(self, corrdinate, user_id):
        """Update user's location by user_id.

        Args:
            corrdinate: [23.9,23.9]
            user_id:

        Returns:
            1 for success 0 for failed
        """
        update_filter = {'user_id':user_id}
        update_data = {"$set":{'coordinate':corrdinate}}
        self.mongodb.user.online.update_one(update_filter, update_data, upsert=True)


    def clear_user_location(self, user_id):
        result = self.mongodb.user.online.delete_one({"user_id":user_id})
        return result.deleted_count