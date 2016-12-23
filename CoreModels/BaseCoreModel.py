#!/usr/bin/env python
# coding=utf-8
# BaseCoreModel.py

class BaseCoreModel(object):
    def __init__(self, *argc, **argkw):
        self.mongodb = argkw['mongodb']
        self.session = argkw['sqlsession']
        self.facepp = argkw['facepp']
