#!/usr/bin/env python
# coding=utf-8
# Index.py

from Handlers.Base import BaseHandler


class IndexHandler(BaseHandler):
    """
     Client will access IndexHandler when he open his app.
     Server will set a _xsrf as cookie to client.
     All of access after it, client should post _xsrf as a parameter to server,
     tornado will check it automatic.
    """
    def get(self):
        try:
            Data = {"_xsrf":self.xsrf_token}
            # Data = json.dumps(Data)
            result = json.dumps({"code": 100,"message":self.xsrf_token,"Data":Data})
            self.write(result)
        except Exception, e:
            result = json.dumps({"code": 99,"message":"fail set cookie","Data":{}})
            self.write(result)
            raise