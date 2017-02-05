#!/usr/bin/env python
# coding=utf-8

from sqlalchemy import Column
from sqlalchemy.types import CHAR, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

BaseModel = declarative_base()

class UserInfo(BaseModel):
    __tablename__ = 'user_info_table'

    user_id = Column(Integer, primary_key=True)
    telephone = Column(CHAR(11)) # or Column(String(30))   
    real_name = Column(CHAR(16))
    nick_name = Column(CHAR(16))
    password = Column(CHAR(64))
    has_update = Column(Boolean())
    id_number = Column(CHAR(18))