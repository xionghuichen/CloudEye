#!/usr/bin/env python
# coding=utf-8
# Web.py

import tornado.web
import logging
class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class FilePageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('file.html')


class DetailPageHandler(tornado.web.RequestHandler):
    def get(self):
        person_id = self.get_argument("person_id")
        logging.info("person_id: %s"%person_id)
        self.render('details.html',person_id=person_id)

class DownloadHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("download.html")