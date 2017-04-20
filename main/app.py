# app.py
import sys
import os
reload(sys)
sys.setdefaultencoding('utf8')

location = str(os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.pardir))) + '/'
sys.path.append(location)

# inner model
import ConfigParser
import logging
# database
import oss2
import redis
import pymongo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# tornado
import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options
# thirdpart sdk
from facepp_sdk.facepp import API, File
import TencentYoutuyun
# my model.
from config.globalVal import AP
from Handlers.Index import IndexHandler,SleepHandler
from Handlers.User import RegisterHandler, LoginHandler, UpdateStatusHandler, ConfirmHandler, LogoutHandler, MyPersonListHandler
from Handlers.FindPerson import SearchPersonHandler, CallHelpHandler, ComparePersonHandler, ImportPersonHandler
from Handlers.MissPerson import GetAllTracksHandler,LastestUpdatePersonHandler, LastestUpdateMessageHandler, GetMissingPersonDetailHandler, GetMissingPersonDetailWebHandler,GetPersonTracksHandler
from Handlers.Web import IndexPageHandler, DetailPageHandler, DownloadHandler

define("port", default=9000, help="run on the given port", type=int)
define("host", default="127.0.0.1", help="community database host")
define("mysql_database", default="cloudeye",
       help="community database name")
define("mysql_user", default="root", help="community mysql user")
define("mysql_password", default="",
       help="community database password")
define("mongo_user",default="burningbear", help="community mongodb  user")
define("mongo_password",default='',help="commuity mongodb password")
define("flush_redis",default=0,help='flush redis all data')
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
        template_path = os.path.join(AP + "templates")
        static_path = os.path.join(AP + "static")
        appid = config.get("YOUTU","APPID")
        secret_id = config.get("YOUTU","SECRET_ID")
        secret_key = config.get("YOUTU","SECRET_KEY")
        userid = config.get("YOUTU","USERID")
        logging.info("start server.")
        settings = dict(
            cookie_secret=COOKIE_SECRET,
            xsrf_cookies=False,
            template_path=template_path,
            static_path=static_path
        )

        handlers = [
            # test
            (r'/', IndexHandler),
            (r'/sleep',SleepHandler),
            (r'/user/register', RegisterHandler),
            (r'/user/login', LoginHandler),
            (r'/user/logout', LogoutHandler),
            (r'/user/confirm', ConfirmHandler),
            (r'/user/peronlistinfo',MyPersonListHandler),
            (r'/user/updatestatus', UpdateStatusHandler),
            (r'/find/searchperson', SearchPersonHandler),
            (r'/find/callhelp', CallHelpHandler),
            (r'/find/compare', ComparePersonHandler),
            (r'/get/updateperson',LastestUpdatePersonHandler),
            (r'/get/updatemessage',LastestUpdateMessageHandler),
            (r'/get/persondetail',GetMissingPersonDetailHandler),
            (r'/get/persondetail/web',GetMissingPersonDetailWebHandler),
            (r'/get/trackinfo/web',GetPersonTracksHandler),
            (r'/get/alltrack/web',GetAllTracksHandler),
            (r'/web/index',IndexPageHandler),
            (r'/web/details',DetailPageHandler),
            (r'/download',DownloadHandler),
            (r'/admin/import',ImportPersonHandler)
            
        ]

        tornado.web.Application.__init__(self, handlers, **settings)
        # use SQLachemy to connection to mysql.
        DB_CONNECT_STRING = 'mysql+mysqldb://%s:%s@%s/%s?charset=utf8'%(options.mysql_user, options.mysql_password, options.host, options.mysql_database)
        engine = create_engine(DB_CONNECT_STRING, echo=False,pool_size=1000)
        self.sqldb = sessionmaker(
                bind=engine,
                autocommit=False, 
                autoflush=True,
                expire_on_commit=False)
        base_model = declarative_base()
        # create all of model inherit from BaseModel 
        base_model.metadata.create_all(engine) 
        # use pymongo to connectino to mongodb
        logging.info("connect mongodb ..")
        client = pymongo.MongoClient(options.host,27017)
        client.cloudeye.authenticate(options.mongo_user,options.mongo_password)
        self.mongodb = client.cloudeye
        # bind face++ cloud service
        logging.info("connect mongodb successfully..")
        # self.facepp = API(FACE_API_KEY, FACE_API_SECRET)
        end_point = TencentYoutuyun.conf.API_YOUTU_END_POINT
        self.youtu = TencentYoutuyun.YouTu(appid, secret_id, secret_key, userid, end_point)
        # bind ali cloud service
        auth = oss2.Auth(ALIYUN_KEY,ALIYUN_SECRET)
        endpoint = r'http://oss-cn-shanghai.aliyuncs.com'
        bucket_name = 'cloudeye'
        self.ali_service = oss2.Service(auth, endpoint)
        self.ali_bucket = oss2.Bucket(auth, endpoint, bucket_name)
        # bind redis service
        logging.info("connect redis..")
        self.redis = redis.Redis(host='localhost',port=6379)
        logging.info("connect redis successfully..")
        if options.flush_redis==1:
            self.redis.flushall()
        logging.info("start completed..")
        
def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
