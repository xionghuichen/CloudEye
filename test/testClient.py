#urllibtest.py
# coding=utf-8
import urllib2
import urllib
import cookielib
import json
import random
import hashlib
import base64
import time
import datetime
# prefix ="http://139.196.207.155:9000"
prefix = "http://127.0.0.1:9000"
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
# get _xsrff
resp = urllib2.urlopen(prefix+'/')
the_page = resp.read()
print resp.getcode() == 200
print the_page

_xsrf = json.loads(the_page)['data']['_xsrf']
print "_xsrf:",_xsrf
def set_resquest(api,data,method):
    # data is dictory.
    # method can be get put delete post ?
    # get _xsrff
    for item in cj:
        if item.name == '_xsrf':
            _xsrf = item.value
    if method != 'GET':
        data['_xsrf'] = _xsrf
    data = urllib.urlencode(data)
    url = prefix + api
    if method == 'GET': 
        url = url + "?"+ data
    request = urllib2.Request(url,data)
    request.get_method = lambda: method # or 'DELETE' 
    return request

def register():
    data = {
        "telephone":"15195861111",
        "password":"zp19950310",
        "real_name":"chenxionghui",
        "nick_name":"burningbear",
        "id_number":"350623199503100053"
    }
    req = set_resquest("/user/register",data,"POST")
    response = urllib2.urlopen(req)
    the_page = response.read()
    print the_page
# db.tracklist.find().sort({_id:-1}).limit(1)
def login():
    data = {
        "telephone":"15195861108",
        "password":"zp19950310"
    }
    req = set_resquest("/user/login",data,"POST")
    response = urllib2.urlopen(req)
    the_page = response.read()
    print the_page

def upload():
    with open('./test_img/ymh3.jpg', 'rb') as f:
        content = f.read()
    data = {
        'search_picture':base64.b64encode(content),
        'pic_type':'jpg',
        'coordinate':[22.9,22.9],
        'camera_id':1
    }
    req = set_resquest("/find/searchperson",data,"POST")
    response = urllib2.urlopen(req)
    the_page = response.read()
    print the_page
# [todo]: if jpg ok?
def callhelp():
    with open('./test_img/zxc2.jpg', 'rb') as f:
        content1 = f.read()
    with open('./test_img/zxc3.jpg', 'rb') as f:
        content2 = f.read()
    data = {
        'picture_list':[base64.b64encode(content1), base64.b64encode(content2)],
        'pic_key':'jpg',
        'name':'如果有期限，一万年',
        'sex':0,
        'age':20,
        'relation_telephone':'15195861108',
        'relation_name':'chenxionghui',
        'lost_time':time.mktime(datetime.datetime.now().timetuple()),
        'lost_spot':[22.9,22.9],
        'description':'please help me dear!!!!'
        }
    req = set_resquest("/find/callhelp",data,"POST")
    response = urllib2.urlopen(req)
    the_page = response.read()
    print the_page

def updatestatus():
    data = {
        'coordinates':[23.9,23.9]# update
    }
    req = set_resquest("/user/updatestatus",data,"POST")
    response = urllib2.urlopen(req)
    the_page = response.read()
    print the_page

def compare():
    with open('./test_img/zxc2.jpg', 'rb') as f:
        content = f.read()
    data = {
        'person_id':'5867b81b16b2d6121d8d8c3d',
        'picture':base64.b64encode(content),
        'pic_type':'jpg',
        'coordinate':[22.9,22.9],
        'description':'maybe I find this missing child!'
    }
    req = set_resquest("/find/compare",data,"POST")
    response = urllib2.urlopen(req)
    the_page = response.read()
    print the_page

def confirm():
    req = set_resquest("/user/confirm",{},"POST")
    response = urllib2.urlopen(req)
    the_page = response.read()
    print the_page

def logout():
    req = set_resquest("/user/logout",{},"POST")
    response = urllib2.urlopen(req)
    the_page = response.read()
    print the_page

def getUpdatePersonList():
    data = {
        'spot':[22.9,22.9],
        'max_distance':3,
        'formal':1,
        'page':0,
        'size':10
    }
    req = set_resquest("/get/updateperson",data,"GET")
    response = urllib2.urlopen(req)
    the_page = response.read()
    print the_page

def getUpdateMessageList():
    data = {
        'spot':[22.9,22.9],
        'max_distance':3,
        'page':0,
        'size':10
    }
    req = set_resquest("/get/updatemessage",data,"GET")
    response = urllib2.urlopen(req)
    the_page = response.read()
    print the_page

def getPersonDetail():
    data = {
        'person_id':"58632a7e16b2d67fa66fa9e9"
    }
    req = set_resquest("/get/persondetail",data,"POST")
    response = urllib2.urlopen(req)
    the_page = response.read()
    print the_page


def getPersonDetailforweb():
    data = {
        'person_id':"58632a7e16b2d67fa66fa9e9"
    }
    req = set_resquest("/get/persondetail/web",data,"GET")
    response = urllib2.urlopen(req)
    the_page = response.read()
    print the_page

def get_personlist_info():
    req = set_resquest("/user/peronlistinfo",{},"POST")
    response = urllib2.urlopen(req)
    the_page = response.read()
    print the_page

# register()
login()
# updatestatus()
# confirm()
# compare()
# callhelp()
# upload()
# logout()
#getPersonDetail()
# for web 
getUpdatePersonList()
# getUpdateMessageList()
#getPersonDetailforweb()
#get_personlist_info()
# def setMessage(message,num,content):
#    message[num] = "No.%s "%num + content + "\r\n"

# def set_info_json(dic):
#     info_json = json.dumps

# def do_request(api,dic,message,method,otherPara):
#     count = 0
#     while count < len(dic):
#         info_json = json.dumps(dic[count])
#         para = otherPara[count]
#         para['info_json'] = info_json
#         # print "do request :" + str(para) + str(ot)
#         req = set_resquest(api,para,method)
#         response = urllib2.urlopen(req)
#         the_page = response.read()
#         print message[count] + the_page
#         count = count + 1   

# def leave_circle():
#     api = '/leave_circle'
#     info_json = {}
#     message = {}
#     otherPara = {}
#     num = 0
#     otherPara[num] = {
#         "umeng_circle_id":"57d79ab1d36ef3cdf599bd89",#the circle you want to leave. this is a string get from circle list.
#     }
#     info_json[num] = {
#     }
#     message[num] = "leave circle : \n"    
#     do_request(api,info_json,message,"POST",otherPara) 
