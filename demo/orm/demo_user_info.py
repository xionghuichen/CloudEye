#!/usr/bin/env python
# coding=utf-8
# demo_user_info.py

from sqlalchemy import Column
from sqlalchemy.types import CHAR, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import and_ 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_CONNECT_STRING = 'mysql+mysqldb://root:zp19950310@139.196.207.155/cloudeye?charset=utf8'
engine = create_engine(DB_CONNECT_STRING, echo=True)
DB_session = sessionmaker(bind=engine)


BaseModel = declarative_base()

class UserInfo(BaseModel):
    __tablename__ = 'user_info_table'

    user_id = Column(Integer, primary_key=True)
    telephone = Column(CHAR(11)) # or Column(String(30))   
    real_name = Column(CHAR(16))
    nick_name = Column(CHAR(16))
    password = Column(CHAR(64))
    has_update = Column(Boolean(False))

    id_number = Column(CHAR(18))

def init_db():
    BaseModel.metadata.create_all(engine)

init_db()

userinfo = UserInfo(
    telephone='15195861118',
    real_name="chenxionghui",
    nick_name="burningbear",
    password='zp19950310',
    id_number = '350623199503100099',
    has_update=False)
session = DB_session()
# ession.add(userinfo)
# query = session.query(UserInfo)
# print "=========================="
# result = query.filter(UserInfo.telephone=='15195861108').first()
# query = session.query(UserInfo)
# test = query.filter(UserInfo.telephone=='15195861108').first()

result = session.query(UserInfo).\
filter(and_(UserInfo.telephone == '15195861108', UserInfo.password == 'zp19950310')).\
scalar() 
print "result is ",result
# print(session.query(User).filter(and_(User.name.like("user%"), User.fullname.like("first%"))).all())    
# print "test is ",test.id
try:
    result  = session.commit()
except IntegrityError as e:
     print e.message

#　print result

session.close()