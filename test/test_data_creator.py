#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.1.5
# Modified    :   2017.1.5
# Version     :   1.0


# test_data_creator.py
from testClient import *
from user_map import u_latitude,u_longtitude,c_latitude,c_longtitude
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
# for item in user_info_list:
#     register(item)
# 在不同的地理位置登录这几个用户
# for index,item in enumerate(user_info_list):
#     login(item)
#     data = {
#         'coordinates':[u_latitude[index],u_longtitude[index]]
#     }
#     updatestatus(data)
with open('./missing_person/aqe/1.jpg', 'rb') as f:
    content1 = f.read()
with open('./missing_person/aqe/2.jpg', 'rb') as f:
    content2 = f.read()
data = {
    'picture_list':[base64.b64encode(content1), base64.b64encode(content2)],
    'pic_key':'jpg',
    'name':'小米电饭煲',
    'sex':0,
    'age':20,
    'relation_telephone':'15195861108',
    'relation_name':'chenxionghui',
    'lost_time':time.mktime(datetime.datetime.now().timetuple()),
    'lost_spot':[22.9,22.9],
    'description':'please help me dear!!!!'
    }
# importperson(data)
# import os
# dir="./missing_person"
# for root,dirs,files in os.walk(dir):
#     for file in files:
#         print os.path.join(root,file)

data = {
    "telephone":"15195891108",
    "password":"zp123456",
    "real_name":"10学小好",
    "nick_name":"10可爱的XXH",
    "id_number":"350623199503100009"
}
register(data)