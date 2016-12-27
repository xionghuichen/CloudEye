#!/usr/bin/env python
# coding=utf-8
# UserCoreModel.py
import logging

from BaseCoreModel import BaseCoreModel
from ORMClass import UserInfo
from sqlalchemy.sql.expression import and_
from sqlalchemy.exc import IntegrityError
from _exceptions.http_error import DBError 
class UserCoreModel(BaseCoreModel):
    def __init__(self, *argc, **argkw):
        super(UserCoreModel, self).__init__(*argc, **argkw)  
        
    def is_telephone_exist(self, telephone):
        """check if the input telephone has been used in mysql.

        Args:
            telephone: input telephone

        Returns:
            True: telephone exist
            False: telehpone not exist.
        """
        query = self.session.query(UserInfo)
        
        if query.filter(UserInfo.telephone==telephone).first():
            return True
        else:
            return False

    def get_uid_by_telephone(self,telephone):
        """query user id from telephone in mysql databases.

        Args:
            telephone: user's telephone.

        Returns:
            user_id: user's user_id.
        """
        query = self.session.query(UserInfo)
        userinfo = query.filter(UserInfo.telephone==telephone).first()       
        if userinfo is None:
            raise DBError('数据查找异常')
        else:
            return userinfo.user_id

    def get_user_info(self,user_id):
        """get user infomation by user_id

        Args:
            user_id
        
        Returns:
                user_id:
                telephone:
                real_name:
                nick_name:
                password:
                id_number:
                has_update:[acid]:

        """
        userinfo = self.session.query(UserInfo).filter(UserInfo.user_id==user_id).first()
        result = {
            'telephone':userinfo.telephone,
            'real_name':userinfo.real_name,
            'nick_name':userinfo.nick_name,
            'id_number':userinfo.id_number
        }
        return result

    def get_missing_person_list(self,user_id):
        """get missing person list from mongodb by user_id.

        Args:
            user_id

        Returns:

        """
        result = self.mongodb.user.personlist.find_one({'user_id':user_id})
        return result['missing_person_list']

    def identify_check(self, telephone, password):
        """check the telephone and password in mysql databases.

        Args:
            telephone
            passowrd

        Returns:
            result: UserInfo object or None
        """
        result = self.session.query(UserInfo).\
        filter(and_(UserInfo.telephone == telephone, UserInfo.password == password)).\
        scalar() 
        return result

    def find_persons_by_tele(self,telephone):
        """query from person.info by telephone.

        Args && example:
            "telephone":"15195861110",
            
        Returns:
            person_list: missing person list identify by '_id'
        """
        cursor = self.mongodb.person.info.find({'relation_telephone':telephone})
        person_list = []
        if cursor != None:
            for item in cursor:
                person_list.append(item['_id'])
        return person_list


    def insert_missing_person_by_uid(self, user_id,person_list):
        """ Insert messing person list by uid into mongodb.

        Args:
            uid: user's id in mysql.
            person_list: missing person list in mongodb[person.info]
                if just want to push single person, just pass as ['person_id']
        Returns:
            result : true for insert success, false otherwise.

        Exception:
            DBError: when insert error.
        """
        update_filter = {'user_id':user_id}
        update_data = {"$pushAll":{'missing_person_list':person_list}}
        # try:
        self.mongodb.user.personlist.update_one(update_filter,update_data,upsert=True)
        # except BaseException as e:
        #     result = False
        #     raise DBError('mongodb数据插入出现异常，insert_missing_person_by_uid')
        return True

    def insert_record_to_sql(self,telephone, password, real_name, nick_name, id_number):
        """insert a new record to mysql.

        Args && example:
            "telephone":"15195861110",
            "password":"zp19950310",
            "real_name":"chenxionghui",
            "nick_name":"burningbear",
            "id_number":"350623199503100053"
        
        Returns:
            result: true or false
            message: a readable message to return to client
        """
        userinfo = UserInfo(
            telephone=telephone,
            real_name=real_name,
            nick_name=nick_name,
            password=password,
            id_number = id_number,
            has_update=False
            )
        self.session.add(userinfo)
        result = True
        message = 'success reigster'
        try:
            self.session.commit()
        except IntegrityError as e:
             message =  e.message
             result = False
        return result, message


    def remove_user_by_telephone(self,telephone):
        """Remove user by telephone.

        Args:
            telephone: the user's telephone to be removed.
        """
        self.session.query(UserInfo).filter(UserInfo.telephone == telephone).\
            delete(synchronize_session=False)
        self.session.commit()

    def update_reporter_status(self, reporter_user_id, status = True):
        """user's misssing person [identify by person_id] has upadated

        Args:
            reporter_user_id
            person_id[ObjectId] --- did not use it now
        """
        self.session.query(UserInfo).filter(UserInfo.user_id == int(reporter_user_id)).\
            update({UserInfo.has_update: status})
        self.session.commit()
        
    def check_update(self, user_id):
        """check if there are new missing person messsage reporter by user_id 

        Args:
            user_id:

        Returns:
        """
        result = self.session.query(UserInfo.has_update).\
        filter(UserInfo.user_id==user_id).\
        first()
        logging.info("result of check update query from sql is %s"%str(result))
        return result.has_update