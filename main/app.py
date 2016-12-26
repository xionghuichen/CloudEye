# app.py
import sys
import os
reload(sys)
sys.setdefaultencoding('utf8')

location = str(os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.pardir))) + '/'
sys.path.append(location)

import ConfigParser
import logging
import oss2
import redis

import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pymongo
from facepp_sdk.facepp import API, File

from config.globalVal import AP
from Handlers.Index import IndexHandler
from Handlers.User import RegisterHandler, LoginHandler, UpdateStatusHandler
from Handlers.FindPerson import SearchPersonHandler, CallHelpHandler, ComparePersonHandler
define("port", default=9000, help="run on the given port", type=int)
define("host", default="139.196.207.155", help="community database host")
define("mysql_database", default="cloudeye",
       help="community database name")
define("mysql_user", default="root", help="community mysql user")
define("mysql_password", default="zp19950310",
       help="community database password")
define("mongo_user",default="burningbear", help="community mongodb  user")
define("mongo_password",default='zp19950310',help="commuity mongodb password")
logging.basicConfig(level=logging.INFO)
                    #filename='log.log',
                    #filemode='w')


class Application(tornado.web.Application):
    def __init__(self, *argc, **argkw):
        config = ConfigParser.ConfigParser()
        config.readfp(open(AP + "config/config.ini"))
        COOKIE_SECRET = config.get("app", "COOKIE_SECRET")
        FACE_API_KEY = config.get("app", "FACE_API_KEY")
        FACE_API_SECRET = config.get("app","FACE_API_SECRET")
        ALIYUN_KEY = config.get("app","ALIYUN_KEY")
        ALIYUN_SECRET = config.get("app","ALIYUN_SECRET")
        template_path = os.path.join(AP + "template")
        static_path = os.path.join(AP + "static")
        logging.info("start server.")
        settings = dict(
            cookie_secret=COOKIE_SECRET,
            xsrf_cookies=True,
            template_path=template_path,
            static_path=static_path
        )

        handlers = [
            # test
            (r'/', IndexHandler),
            (r'/user/register', RegisterHandler),
            (r'/user/login', LoginHandler),
            (r'/user/updatestatus', UpdateStatusHandler),
            (r'/find/searchperson', SearchPersonHandler),
            (r'/find/callhelp', CallHelpHandler),
            (r'/find/compare', ComparePersonHandler)
        ]

        tornado.web.Application.__init__(self, handlers, **settings)
        # use SQLachemy to connection to mysql.
        DB_CONNECT_STRING = 'mysql+mysqldb://%s:%s@%s/%s'%(options.mysql_user, options.mysql_password, options.host, options.mysql_database)
        engine = create_engine(DB_CONNECT_STRING, echo=True)
        self.sqldb = sessionmaker(
                bind=engine,
                autocommit=False, 
                autoflush=True,
                expire_on_commit=False)
        base_model = declarative_base()
        # create all of model inherit from BaseModel 
        base_model.metadata.create_all(engine) 
        # use pymongo to connectino to mongodb
        client = pymongo.MongoClient(options.host,27017)
        client.cloudeye.authenticate(options.mongo_user,options.mongo_password)
        self.mongodb = client.cloudeye
        # bind face++ cloud service
        self.facepp = API(FACE_API_KEY, FACE_API_SECRET)
        # bind ali cloud service
        auth = oss2.Auth(ALIYUN_KEY,ALIYUN_SECRET)
        endpoint = r'http://oss-cn-shanghai.aliyuncs.com'
        bucket_name = 'cloudeye'
        self.ali_service = oss2.Service(auth, endpoint)
        self.ali_bucket = oss2.Bucket(auth, endpoint, bucket_name)
        # bind redis service
        self.redis = redis.Redis(host='localhost',port=6379)
def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
