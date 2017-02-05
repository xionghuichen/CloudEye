#!/usr/bin/env python
# coding=utf-8
# Index.py

from Handlers.Base import BaseHandler
import json

class IndexHandler(BaseHandler):
    """
     Client will access IndexHandler when he open his app.
     Server will set a _xsrf as cookie to client.
     All of access after it, client should post _xsrf as a parameter to server,
     tornado will check it automatic.
    """
    def get(self):
        try:
            data = {"_xsrf":self.xsrf_token}
            jquery = ''
            try:
                jquery = str(self.get_argument('jsoncallback'))
            except Exception as e:
                # do nothing.
                pass
            # Data = json.dumps(Data)
            result = json.dumps({"code": 100,"message":self.xsrf_token,"data":data})
            if jquery != '':
                result = jquery + '('+result+')'

            self.write(result)
        except Exception, e:
            result = json.dumps({"code": 99,"message":"fail set cookie","data":{}})
            self.write(result)
            raise
        self.finish()
