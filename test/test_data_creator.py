#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.1.5
# Modified    :   2017.1.5
# Version     :   1.0


# test_data_creator.py
from testClient import *
from user_map import u_latitude,u_longtitude,c_latitude,c_longtitude
import random
import json
user_info_list=[
{
    "telephone":"15195861001",
    "password":"zp123456",
    "real_name":"1王小萍",
    "nick_name":"1可爱的WXP",
    "id_number":"350623199503100001"
},{
    "telephone":"15195861002",
    "password":"zp123456",
    "real_name":"2吴小凡",
    "nick_name":"2帅气的WXF",
    "id_number":"350623199503100002"
},{
    "telephone":"15195861003",
    "password":"zp123456",
    "real_name":"3陈小辉",
    "nick_name":"3机智的CXH",
    "id_number":"35062319950310003"
},{
    "telephone":"15195861004",
    "password":"zp123456",
    "real_name":"4赵小一",
    "nick_name":"4可爱的WXP",
    "id_number":"350623199503100004"
},{
    "telephone":"15195861005",
    "password":"zp123456",
    "real_name":"5刘小志",
    "nick_name":"5勇猛的LXZ",
    "id_number":"350623199503100005"
},{
    "telephone":"15195861006",
    "password":"zp123456",
    "real_name":"6许小涵",
    "nick_name":"6可爱的WXP",
    "id_number":"350623199503100006"
},{
    "telephone":"15195861007",
    "password":"zp123456",
    "real_name":"7林小婧",
    "nick_name":"4可爱的LXJ",
    "id_number":"350623199503100007"
},{
    "telephone":"15195861008",
    "password":"zp123456",
    "real_name":"8蓝小火",
    "nick_name":"8勇猛的LXH",
    "id_number":"350623199503100008"
},{
    "telephone":"15195861009",
    "password":"zp123456",
    "real_name":"9学小好",
    "nick_name":"9可爱的XXH",
    "id_number":"350623199503100009"
}
]
def child_creator(upload_number,abbreviated,name,parent_id,user_id=0):
    picture_list = []
    for index in range(1,upload_number+1):
        with open('./missing_person/%s/%s.jpg'%(abbreviated,upload_number), 'rb') as f:
            picture_list.append(base64.b64encode(f.read()))

    # random_spot = random.randint(0,len(c_longtitude))
    data = {
        'picture_list':picture_list,
        'pic_key':'jpg',
        'name':name,
        'sex':random.randint(0,1),
        'age':random.randint(0,15),
        'relation_telephone':user_info_list[parent_id]['telephone'],
        'relation_name':user_info_list[parent_id]['real_name'],
        'lost_time':time.mktime(datetime.datetime.now().timetuple()),
        'lost_spot':[u_latitude[parent_id],u_longtitude[parent_id]],
        'description':'please help me, dear!!!!',
        'relation_id':user_id
        }
    return data





# import missing person data.
# count = 0
# import os
# dir="./missing_person"
# missing_list = {}
# for root,dirs,files in os.walk(dir):
#     name = root[len(dir)+1:]
#     random_parent = random.randint(0,len(user_info_list)-1)
#     if name != '':
#         print "times: %s"%count 
#         count =count + 1
#         if count > 11:
#             break
#         print random_parent
#         data = child_creator(3,name,name,random_parent)
#         if missing_list.has_key(user_info_list[random_parent]['real_name']):
#             missing_list[user_info_list[random_parent]['real_name']].append(name)
#         else:
#             missing_list[user_info_list[random_parent]['real_name']]=[name]
#         print "new import :%s,parent is %s"%(name,user_info_list[random_parent]['real_name'])
#         result = eval(importperson(data))
#         print result
#         if result['code'] !=1:
#             raise Exception("error import ! %s"%result)
# print json.dumps(missing_list,indent=2,ensure_ascii=False)

# register
# for item in user_info_list:
#     print register(item)

# login
# 在不同的地理位置登录这几个用户
# for index,item in enumerate(user_info_list):
#     login(item)
#     data = {
#         'coordinates':[u_latitude[index],u_longtitude[index]]
#     }
#     print updatestatus(data)


# camera search person
# import os
# dir="./missing_person"
# missing_list = []
# for root,dirs,files in os.walk(dir):
#     name = root[len(dir)+1:]
#     random_camera = random.randint(1,len(c_latitude))
#     if name != '':
#         upload_number = random.randint(4,6)
#         print "use camera :%s, search %s of picture %s"%(random_camera,name,upload_number)
#         with open('./missing_person/%s/%s.jpg'%(name,upload_number), 'rb') as f:
#             content = base64.b64encode(f.read())
#             data = {
#                 'search_picture':content,
#                 'pic_type':'jpg',
#                 'coordinate':[c_latitude[random_camera-1],c_longtitude[random_camera-1]],
#                 'camera_id':random_camera
#             }
#             try:
#                 result = eval(upload(data))
#                 print result
                
#                 person_id = result['data']['person_id']
#                 data = {'person_id':person_id}
#                 search_name = eval(getPersonDetail(data))['data']['person_info']['name']
#                 print "origin name is %s, search name is %s, confidence is %s"%(name,search_name,result['data']['confidence'])
#             except Exception as e:
#                 print "error:%s"%(str(e))

# call help.
# import os
# dir="./missing_person"
# count = 0
# missing_list = {}
# for root,dirs,files in os.walk(dir):
#     name = root[len(dir)+1:]
#     random_parent = random.randint(0,len(user_info_list)-1)
#     if name != '':
#         print random_parent
#         print "times: %s"%count 
#         count =count + 1
#         if count <=11:
#             continue
#         user_id = eval(login(user_info_list[random_parent]))['data']['user_id']
#         data = child_creator(3,name,name,random_parent,user_id)
#         if missing_list.has_key(user_info_list[random_parent]['real_name']):
#             missing_list[user_info_list[random_parent]['real_name']].append(name)
#         else:
#             missing_list[user_info_list[random_parent]['real_name']]=[name]
#         print "new call help :%s,parent is %s"%(name,user_info_list[random_parent]['real_name'])
#         result = eval(callhelp(data))
#         print result
#         if result['code'] !=1:
#             raise Exception("error import ! %s"%result)
# print json.dumps(missing_list,indent=2,ensure_ascii=False)

# 用户跟踪拍摄
# for index,item in enumerate(user_info_list):
#     login(item)
#     data = {
#         'coordinates':[u_latitude[index],u_longtitude[index]]
#     }
#     update_result = eval(updatestatus(data))
#     message_queue = update_result['data']['message_queue']
#     if message_queue == []:
#         continue
#     print message_queue
#     message = message_queue[random.randint(0,len(message_queue)-1)]
#     # print message
#     name = message['name'].decode('utf-8')
#     spot = message['spot']
#     # pic = message['pic_key']
#     std_pic = message['std_pic_key']
#     person_id = message['person_id']
#     # get random picture to detect.
#     print "now user %s, find sombody like %s"%(str(user_info_list[index]['real_name']),str(name.encode('utf-8')))
#     print "std picture is :%s"%std_pic
#     print "is formal %s"%message['formal']
#     # print "found picture is : %s"%pic
#     upload_number = random.randint(4,6)
#     with open('./missing_person/%s/%s.jpg'%(name,upload_number), 'rb') as f:
#         content = base64.b64encode(f.read())
#     data = {
#         'person_id':person_id,
#         'picture':content,
#         'pic_type':'jpg',
#         'coordinate':[u_latitude[index],u_longtitude[index]],
#         'description':'maybe I find this missing child!'
#     }
#     try:
#         result = eval(compare(data))
#         print "compare result is %s"%json.dumps(result,indent=2,ensure_ascii=False)
#     except Exception as e:
#         print "error:%s"%(str(e))

# test confirm
# 在不同的地理位置登录这几个用户
# login(user_info_list[3])
# data = {
#     'coordinates':[u_latitude[3],u_longtitude[3]]
# }
# print updatestatus(data)
# confirm()

data = {
    'person_id':'589966e6af8add4f9beefdee'
}
print getPersonDetail(data)