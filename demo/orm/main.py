#!/usr/bin/env python
# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DB_CONNECT_STRING = 'mysql+mysqldb://root:zp19950310@localhost'
engine = create_engine(DB_CONNECT_STRING, echo=True)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()

# session.execute('create database zedtestorm')
print session.execute('show databases').fetchall()
session.execute('use testorm')
# 建 user 表的过程略
print session.execute('select * from user where id = 1').first()
print session.execute('select * from user where id = :id', {'id': 1}).first()

