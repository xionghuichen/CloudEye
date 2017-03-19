#!/usr/bin/env python
# coding=utf-8


from testClient import *
# from user_map import u_latitude,u_longitude,c_latitude,c_longitude
import random
import json
import logging
import os


u_latitude = []
u_longitude = []
c_latitude = []
c_longitude = []


user_info_list=[
{
    "telephone":"15195861001",
    "password":"zp123456",
    "real_name":"王小萍",
    "nick_name":"MiaoMiaoMiao",
    "id_number":"350623199503100001"
},{
    "telephone":"15195861002",
    "password":"zp123456",
    "real_name":"吴正凡",
    "nick_name":"彩虹直至黑白",
    "id_number":"350623199503100002"
},{
    "telephone":"15195861003",
    "password":"zp123456",
    "real_name":"陈辉",
    "nick_name":"机智如我",
    "id_number":"35062319950310003"
},{
    "telephone":"15195861004",
    "password":"zp123456",
    "real_name":"赵旖",
    "nick_name":"UU妹",
    "id_number":"350623199503100004"
},{
    "telephone":"15195861005",
    "password":"zp123456",
    "real_name":"曾博辉",
    "nick_name":"绩点不上４不睡觉",
    "id_number":"350623199503100005"
},{
    "telephone":"15195861006",
    "password":"zp123456",
    "real_name":"王雷",
    "nick_name":"北京北京",
    "id_number":"350623199503100006"
},{
    "telephone":"15195861007",
    "password":"zp123456",
    "real_name":"林琴",
    "nick_name":"琴声悠悠",
    "id_number":"350623199503100007"
},{
    "telephone":"15195861008",
    "password":"zp123456",
    "real_name":"崔月",
    "nick_name":"Call me Maybe",
    "id_number":"350623199503100008"
},{
    "telephone":"15195861009",
    "password":"zp123456",
    "real_name":"吴凡",
    "nick_name":"6666666",
    "id_number":"350623199503100009"
}
# ,{
#     "telephone":"15195861010",
#     "password":"zp123456",
#     "real_name":"余军",
#     "nick_name":"Sadddd~",
#     "id_number":"350623199503100010"
# },{
#     "telephone":"15195861011",
#     "password":"zp123456",
#     "real_name":"明凯",
#     "nick_name":"ClearLove",
#     "id_number":"350623199503100011"
# },{
#     "telephone":"15195861012",
#     "password":"zp123456",
#     "real_name":"陶研",
#     "nick_name":"Insec",
#     "id_number":"350623199503100012"
# },{
#     "telephone":"15195861013",
#     "password":"zp123456",
#     "real_name":"赵磊",
#     "nick_name":"吼吼吼吼",
#     "id_number":"350623199503100013"
# },{
#     "telephone":"15195861014",
#     "password":"zp123456",
#     "real_name":"刘畅",
#     "nick_name":"Original",
#     "id_number":"350623199503100014"
# },{
#     "telephone":"15195861015",
#     "password":"zp123456",
#     "real_name":"吴雪萍",
#     "nick_name":"等一个人",
#     "id_number":"350623199503100015"
# },{
#     "telephone":"15195861016",
#     "password":"zp123456",
#     "real_name":"毛天天",
#     "nick_name":"泪的痛述",
#     "id_number":"350623199503100016"
# },{
#     "telephone":"15195861017",
#     "password":"zp123456",
#     "real_name":"李子龙",
#     "nick_name":"翻墙斗地主",
#     "id_number":"350623199503100017"
# },{
#     "telephone":"15195861018",
#     "password":"zp123456",
#     "real_name":"章结",
#     "nick_name":"One By One",
#     "id_number":"350623199503100018"
# },{
#     "telephone":"15195861019",
#     "password":"zp123456",
#     "real_name":"许旖旎",
#     "nick_name":"旖旎",
#     "id_number":"350623199503100019"
# },{
#     "telephone":"15195861020",
#     "password":"zp123456",
#     "real_name":"张小凡",
#     "nick_name":"鬼厉",
#     "id_number":"350623199503100020"
# }
]


# register

# for item in user_info_list:
#     print register(item)


# login

# for index,item in enumerate(user_info_list):
#     login(item)
#     data = {
#         'coordinates':[u_latitude[index],u_longitude[index]]
#     }
#     print updatestatus(data)


# call help

dir="./missing_person"
count = 0
missing_list = {}
for root,dirs,files in os.walk(dir):
    name = root[len(dir)+1:]
    random_parent = random.randint(0,len(user_info_list)-1)
    if name != '':
        print random_parent
        print "times: %s"%count 
        count =count + 1
        if count <= 11:
            continue
        user_id = eval(login(user_info_list[random_parent]))['data']['user_id']
        data = child_creator(3,name,name,random_parent,user_id)
        if missing_list.has_key(user_info_list[random_parent]['real_name']):
            missing_list[user_info_list[random_parent]['real_name']].append(name)
        else:
            missing_list[user_info_list[random_parent]['real_name']]=[name]
        print "new call help :%s,parent is %s"%(name,user_info_list[random_parent]['real_name'])
        result = eval(callhelp(data))
        print result
        if result['code'] !=1:
            print "error import ! %s"%result
print json.dumps(missing_list,indent=2,ensure_ascii=False)