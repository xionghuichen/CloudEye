#urllibtest.py
# coding=utf-8
import urllib2
import urllib
import cookielib
import json
import random
import hashlib
import base64
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

_xsrf = json.loads(the_page)['Data']['_xsrf']

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
        "telephone":"15195861109",
        "password":"zp19950310",
        "real_name":"chenxionghui",
        "nick_name":"burningbear",
        "id_number":"350623199503100053"
    }
    req = set_resquest("/user/register",data,"POST")
    response = urllib2.urlopen(req)
    the_page = response.read()
    print the_page

def login():
    data = {
        "telephone":"15195861109",
        "password":"zp19950310"
    }
    req = set_resquest("/user/login",data,"POST")
    response = urllib2.urlopen(req)
    the_page = response.read()
    print the_page

def upload():
    data = {
        "url":'http://bj-mc-prod-asset.oss-cn-beijing.aliyuncs.com/mc-official/images/face/demo-pic11.jpg',
    }
    req = set_resquest("/find/searchperson",data,"POST")
    response = urllib2.urlopen(req)
    the_page = response.read()
    print the_page

def callhelp():
    with open('./demo.jpeg', 'rb') as f:
        content = f.read()
    
    data = {
        'base64ImgStr_list':[base64.b64encode(content)],
    }
    print data
    req = set_resquest("/find/callhelp",data,"POST")
    response = urllib2.urlopen(req)
    the_page = response.read()
    print the_page

callhelp()
# register()
# login()
# upload()
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
