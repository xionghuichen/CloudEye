#!/usr/bin/env python
# coding=utf-8
from sqlalchemy import Column
from sqlalchemy.types import CHAR, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_CONNECT_STRING = 'mysql+mysqldb://root:zp19950310@localhost/testorm'
engine = create_engine(DB_CONNECT_STRING, echo=True)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()

BaseModel = declarative_base()

def init_db():
    BaseModel.metadata.create_all(engine)# 会找到 BaseModel 的所有子类，并在数据库中建立这些表

def drop_db():
    BaseModel.metadata.drop_all(engine)# 会找到 BaseModel 的所有子类，删除这些表。


class User(BaseModel):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(CHAR(30)) # or Column(String(30))

init_db()


user = User(name='ab')
session.add(user)
user = User(name='bb')
session.add(user)
user = User(name='ab')
session.add(user)
#user = User()
#session.add(user)
session.commit()
