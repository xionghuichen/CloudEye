#!/usr/bin/env python
# coding=utf-8
# Index.py

from Handlers.Base import BaseHandler
from tornado import httputil, stack_context
from tornado.concurrent import TracebackFuture
from tornado.httpclient import HTTPResponse, HTTPError
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
import json
import tornado.gen
import tornado.web
import time
MAX_WORKERS = 5000

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

class BackHandler(object):
    executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

    @run_on_executor
    def background_task(self):
        sm = 0
        time.sleep(2)
        for i in range(0,8):
            sm = sm + 1
        return sm


class SleepHandler(BaseHandler):
    executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)
    # @tornado.gen.coroutine
    #  @tornado.web.asynchronous
    # @tornado.gen.engine
    @tornado.gen.coroutine
    def get(self):
        # query = self.get_argument('q')
	        
	# client = tornado.httpclient.AsyncHTTPClient()
        # response = yield tornado.gen.Task(client.fetch,
        #         "http://search.twitter.com/search.json?" + \
        #         urllib.urlencode({"q": query, "result_type": "recent", "rpp": 100}))
        # body = json.loads(response.body)
        # result_count = len(body['results'])
        # now = datetime.datetime.utcnow()
        # raw_oldest_tweet_at = body['results'][-1]['created_at']
        # oldest_tweet_at = datetime.datetime.strptime(raw_oldest_tweet_at,
        #         "%a, %d %b %Y %H:%M:%S +0000")
        # seconds_diff = time.mktime(now.timetuple()) - \
        #         time.mktime(oldest_tweet_at.timetuple())
        # tweets_per_second = float(result_count) / seconds_diff
        # self.write("""
        # <div style="text-align: center">
        #     <div style="font-size: 72px">%s</div>
        #     <div style="font-size: 144px">%.02f</div>
        #     <div style="font-size: 24px">tweets per second</div>
        # </div>""" % (query, tweets_per_second))
        b = BackHandler()
        response = yield b.background_task() #yield tornado.gen.Task(self.sleep_task,5)
        self.write(str(response))
        # self.finish()    
    '''
    def sleep_task(self,t,callback):
        time.sleep(5)
        #  callback('test')
        future = TracebackFuture()
        if callback is not None:
            callback = stack_context.wrap(callback)
            def handle_future(future):
                exc = future.exception()
                if isinstance(exc, HTTPError) and exc.response is not None:
                    response = exc.response
                elif exc is not None:
                    pass
                    #response = HTTPResponse(
                    #    request, 599, error=exc,
                    #    request_time=time.time() - request.start_time)
                else:
                    response = future.result()
                self.io_loop.add_callback(callback, response)
            future.add_done_callback(handle_future)
    '''

    @run_on_executor
    def background_task(self):
        sm = 0
        time.sleep(2)
        for i in range(0,8):
            sm = sm + 1
        return sm
