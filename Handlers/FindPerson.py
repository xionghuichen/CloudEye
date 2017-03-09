#!/usr/bin/env python
# coding=utf-8
# FindPerson.py
import json
import base64
import logging
import time
import datetime
from bson import ObjectId
import tornado.web
import tornado.gen

from _exceptions.http_error import MyMissingArgumentError, ArgumentTypeError, InnerError
from Base import BaseHandler
from config.globalVal import ReturnStruct, PLICEMAN_ID


class FindPersonHandler(BaseHandler):
    def __init__(self, *argc, **argkw):
        super(FindPersonHandler, self).__init__(*argc, **argkw)
        self.type_map = {
            "camera":"camera:",
            "reporter":"reporter:",
        }

class SearchPersonHandler(FindPersonHandler):
    def __init__(self, *argc, **argkw):
        super(SearchPersonHandler, self).__init__(*argc, **argkw)
        self.confidence_threshold = 95

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        """Find if there are high confidence face in face databses.

        Args:
            search_picture: single picture encode in base64
            coordinate: location of the place shoot the picture,
            searcher_id: device id.
            pic_type: example:'jpg','jpeg'

        Returns:
            needn't return to client. But there are three status:
                'search success and confidence higher than level 2: 
                'search success but confidence does not higher than level:2'
                'search failed'
        """
        message_mapping = [
            'search success and confidence higher than level: %s'%self.confirm_level,
            'search success but confidence does not higher than level:%s'%self.confirm_level,
            'search failed'
        ]
        result = ReturnStruct(message_mapping)
        # 1. upload
        try:
            search_picture = self.get_argument("search_picture")
            coordinate = eval(self.get_argument("coordinate"))
            searcher_id = int(self.get_argument("id"))
            search_type = self.get_argument("type")
            pic_type = self.get_argument('pic_type')
        except tornado.web.MissingArgumentError, e:
            raise MyMissingArgumentError(e.arg_name)   
        # change base64 to binary file
        try:
            binary_picture = base64.b64decode(search_picture)
        except TypeError as e:
            raise ArgumentTypeError('search_picture')
        
        event_happen_date = float(time.mktime(datetime.datetime.now().timetuple()))
        
        # configure type parameters
        if search_type == 'camera':
            search_mode = self.person_model.CAMERA
            message_mode = self.message_model.SEARCH
            shooter_info = None
        elif search_type == 'reporter':
            searcher_id = self.get_secure_cookie('user_id')
            search_mode = self.person_model.PERSON_SEARCH
            shooter_info = {
                'user_id':searcher_id,
            }
            message_mode = self.message_model.PERSON_SEARCH
            
        # 2. search_person
        result_detect_struct = yield tornado.gen.Task(self.face_model.detect_img_list, [binary_picture], False)
        result.merge_info(result_detect_struct)
        if result_detect_struct.code == 0:
            # has high quality picture:
            for item in result_detect_struct.data['detect_result_list']:
                face_token = item['face_token']
                searchResult = yield tornado.gen.Task(self.face_model.search_person, face_token)
                if searchResult != None:
                    # has search result.
                    if searchResult['level'] >= self.confirm_level:
                        # has high confidence
                        result.code = 0
                        # 3. get missing person_detail.
                        person_id = searchResult['info']['user_id']
                        result.data['person_id']=person_id
                        result.data['confidence']=searchResult['confidence']
                        del result.data['detect_result_list']
                        brief_info_list = self.person_model.get_person_brief_info([ObjectId(person_id)])[0]
                        result.data['std_photo_key'] = brief_info_list['std_photo_key']
                        result.data['name']=brief_info_list['name']
                        result.data['description']=brief_info_list['description']
                        result.data['sex']=brief_info_list['sex']
                        result.data['lost_time']=brief_info_list['lost_time']
                        result.data['age']=brief_info_list['age']
                        # upload picture
                        detect_result = item
                        # [todo] delete unreadable '[]'
                        pic_key_list = yield tornado.gen.Task(
                            self.picture_model.store_pictures,
                            [binary_picture], 
                            self.type_map[search_type]+str(searcher_id), 
                            pic_type, 
                            [detect_result])
                        # 4. update track　and person information
                        event_info = {
                            'coordinate':coordinate,
                            'confidence':searchResult['confidence'],
                            'pic_key':pic_key_list[0],
                            'person_id':person_id,
                            'date':event_happen_date
                        }
                        try:
                            track_id = self.person_model.update_person_status(search_mode, event_info,shooter_info)
                        except Exception as e:
                            logging.info("infomation of exception %s"%str(e))
                            key = "camera"+str(searcher_id)
                            self.picture_model.delete_pictures("camera"+str(searcher_id), pic_type)
                            raise InnerError("正在search请求中更新用户信息时")

                        # 5. send message
                        message_data = {
                            'person_id':person_id,
                            'spot':coordinate,
                            'date':event_happen_date,
                            'confidence':searchResult['confidence'],
                            'pic_key':pic_key_list[0]
                        }
                        if message_mode == self.person_model.PERSON_SEARCH:
                            message_data['upload_user_id'] = searcher_id
                        try:
                            self.message_model.send_message_factory(message_mode, message_data)
                        except Exception as e:
                            logging.info("infomation of exception %s"%str(e))
                            key = "camera"+str(searcher_id)
                            self.picture_model.delete_pictures("camera"+str(searcher_id), pic_type)
                            raise InnerError("正在search请求中发送消息时，%s"%str(e))
                        break
                    else:
                        result.code = 1
                        result.data = {}
                else:
                    result.code = 2
                    result.data = {}
        self.return_to_client(result)
        self.finish()


class CallHelpHandler(FindPersonHandler):
    def __init__(self, *argc, **argkw):
        super(CallHelpHandler, self).__init__(*argc, **argkw)

    @tornado.gen.coroutine
    def post(self):
        """ Upload person information which is missing recently. 
        Syetem will push message to police and person around this person.

        Args:

        Returns:
        """
        message_mapping = [
        'empty image'
        ]
        result =ReturnStruct(message_mapping)
        try:
            picture_list = eval(self.get_argument('picture_list'))
            user_id = int(self.get_secure_cookie("user_id"))
            pic_type = self.get_argument('pic_key')
            info_data={
                'name':self.get_argument('name'),
                'sex':int(self.get_argument('sex')),
                'age':int(self.get_argument('age')),
                'relation_telephone':self.get_argument('relation_telephone'),
                'relation_name':self.get_argument('relation_name'),
                'relation_id': user_id,
                'formal':0,
                'lost_time':float(self.get_argument('lost_time')),
                'lost_spot':eval(self.get_argument('lost_spot')),
                'description':self.get_argument('description'),
            }
        except tornado.web.MissingArgumentError, e:
            raise MyMissingArgumentError(e.arg_name)     

        if user_id == None or user_id == '':
            raise MyMissingArgumentError("cookie: user_id [maybe did not login yet]")
        binary_picture_list = []
        if picture_list == []:
            result.code = 0
        else:
            # has image
            for image_str in picture_list:
                # decode base64 to binary file
                try:
                    binary_picture_list.append(base64.b64decode(image_str))
                except TypeError as e:
                    raise ArgumentTypeError('picture_list')

            # get face_token _list
            result_detect = yield tornado.gen.Task(self.face_model.detect_img_list, binary_picture_list, True)
            result.merge_info(result_detect)
            if result_detect.code == 0:
                # upload pictures.
                detect_result_list = result_detect.data['detect_result_list']
                result_pic_key = yield tornado.gen.Task(
                    self.picture_model.store_pictures,binary_picture_list, self.type_map['reporter']+str(user_id), pic_type, detect_result_list)
                # todo, error handler
                # store information.[track and person]

                person_id = self.person_model.store_new_person(result_pic_key, detect_result_list, info_data, user_id)
                message_data = {
                    'name': info_data['name'],
                    'std_pic_key':result_pic_key[0],
                    'spot':info_data['lost_spot'],
                    'date':info_data['lost_time'],
                    'age':info_data['age'],
                    'sex':info_data['sex'],
                    'person_id':person_id,
                    'reporter_user_id':user_id
                }
                self.message_model.send_message_factory(self.message_model.CALL_HELP, message_data)
                result.data = {}
            # send message
        self.return_to_client(result)
        self.finish()


class ImportPersonHandler(FindPersonHandler):
    def __init__(self, *argc, **argkw):
        super(ImportPersonHandler, self).__init__(*argc, **argkw)

    @tornado.gen.coroutine
    def post(self):
        """ Upload person information which is missing recently. 
        Syetem will push message to police and person around this person.

        Args:

        Returns:

        [todo]:
        this api can only called by ploiceman

        """
        message_mapping = [
        'empty image'
        ]
        user_id = PLICEMAN_ID
        result =ReturnStruct(message_mapping)
        try:
            picture_list = eval(self.get_argument('picture_list'))
            pic_type = self.get_argument('pic_key')
            info_data={
                'name':self.get_argument('name'),
                'sex':int(self.get_argument('sex')),
                'age':int(self.get_argument('age')),
                'relation_id':user_id,
                'formal':1,
                'relation_telephone':self.get_argument('relation_telephone'),
                'relation_name':self.get_argument('relation_name'),
                'lost_time':float(self.get_argument('lost_time')),
                'lost_spot':eval(self.get_argument('lost_spot')),
                'description':self.get_argument('description')
            }
        except tornado.web.MissingArgumentError, e:
            raise MyMissingArgumentError(e.arg_name)     
        binary_picture_list = []
        if picture_list == []:
            result.code = 0
        else:
            # has image
            for image_str in picture_list:
                # decode base64 to binary file
                try:
                    binary_picture_list.append(base64.b64decode(image_str))
                except TypeError as e:
                    raise ArgumentTypeError('picture_list')

            # get face_token _list
            result_detect = yield tornado.gen.Task(self.face_model.detect_img_list, binary_picture_list, True)
            result.merge_info(result_detect)
            if result_detect.code == 0:
                # upload pictures.
                detect_result_list = result_detect.data['detect_result_list']
                result_pic_key = yield tornado.gen.Task(
                    self.picture_model.store_pictures,binary_picture_list, self.type_map['reporter']+str(user_id), pic_type, detect_result_list)
                # todo, error handler
                # store information.[track and person]
                person_id = self.person_model.store_new_person(result_pic_key, detect_result_list, info_data, user_id)
                result.data = {}
            # send message
        self.return_to_client(result)
        self.finish()

class ComparePersonHandler(FindPersonHandler):
    def __init__(self, *argc, **argkw):
        super(ComparePersonHandler, self).__init__(*argc, **argkw)
   
    @tornado.gen.coroutine
    def post(self):
        """User can upload a picture for a specific person_id. 
        System will compare it and tell user if this is a high confidence face.
        Besides, if it is a high confidence face, we should store this new message and pugh this message though LBS and pilice man.

        Args:

            person_id:
            picture:
            coordinate:
            user_id

        Returns:

        """
        try:
            person_id = self.get_argument('person_id')
            coordinate = eval(self.get_argument('coordinate'))
            picture = self.get_argument('picture')
            description = self.get_argument('description')
            user_id = int(self.get_secure_cookie('user_id'))
            pic_type = self.get_argument('pic_type')
        except tornado.web.MissingArgumentError as e:
            raise MyMissingArgumentError(e.arg_name)     
        try:
            binary_picture = base64.b64decode(picture)
        except TypeError as e:
            raise ArgumentTypeError('picture')
        message_mapping = [
            'find high confidence person',
            'the person maybe not the missing one'

        ]
        result =ReturnStruct(message_mapping)
        event_happen_date = float(time.mktime(datetime.datetime.now().timetuple()))
        # 1. get person's std picture. personid--> -->face_token
        std_face_token = self.person_model.get_person_std_pic(person_id)
        # 2. detect picture --> face_token2
        result_detect_struct = yield tornado.gen.Task(self.face_model.detect_img_list, [binary_picture], True)
        result.merge_info(result_detect_struct)
        # 3. compare face_token.
        if result_detect_struct.code == 0:
            # the result just one element
            detect_result = result_detect_struct.data['detect_result_list']
            confidence = yield tornado.gen.Task(self.face_model.compare_face, std_face_token, detect_result[0]['face_token'])
            result.data = confidence
            # logging.info("result of compare, the confidence is %s"%confidence)
            if confidence['level'] >= self.confirm_level:    
                # 4. update info
                result.code = 0
                pic_key_list = yield tornado.gen.Task(self.picture_model.store_pictures,[binary_picture], "user"+str(user_id), pic_type, detect_result)
                # 4. update track　and person information
                shooter_info = {
                    'user_id':user_id,
                    'description':description
                }
                event_info = {
                    'coordinate':coordinate,
                    'confidence':confidence['confidence'],
                    'pic_key':pic_key_list[0],
                    'person_id':person_id,
                    'date':event_happen_date
                }
                self.person_model.update_person_status(self.person_model.PERSON, event_info, shooter_info)
                # 5. send message.
                message_data = {
                    'spot':coordinate,
                    'date':event_happen_date,
                    'person_id':person_id,
                    'upload_user_id':user_id,
                    'confidence':confidence['confidence'],
                    'pic_key':pic_key_list[0]
                }
                self.message_model.send_message_factory(self.message_model.COMPARE, message_data)
            else:
                result.code = 1
        self.return_to_client(result)
        self.finish()