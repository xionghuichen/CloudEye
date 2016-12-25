#!/usr/bin/env python
# coding=utf-8
# LocationCoreModel.py

from BaseCoreModel import BaseCoreModel

class LocationCoreModel(BaseCoreModel):
    def __init__(self, *argc, **argkw):
        super(LocationCoreModel, self).__init__(*argc, **argkw)

    def find_user_in_range(self, coordinate):
        pass

    def update_user_location(self, corrdinate, user_id):
        """Update user's location by user_id.

        Args:
            corrdinate: [23.9,23.9]
            user_id:

        Returns:
            1 for success 0 for failed
        """
        update_filter = {'user_id':user_id}
        update_data = {"$set":{'corrdinate':corrdinate}}
        self.mongodb.user.online.update_one(update_filter, update_data, upsert=True)


    def clear_user_location(self, corrdinate):
        pass
    