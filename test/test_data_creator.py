#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.1.5
# Modified    :   2017.1.5
# Version     :   1.0


# test_data_creator.py
from testClient import *
from user_map import Location 
import random
import json
import logging
# user_info_list=[
# {
#     "telephone":"15195861001",
#     "password":"zp123456",
#     "real_name":"王小萍",
#     "nick_name":"MiaoMiaoMiao",
#     "id_number":"350623199503100001"
# },{
#     "telephone":"15195861002",
#     "password":"zp123456",
#     "real_name":"吴正凡",
#     "nick_name":"彩虹直至黑白",
#     "id_number":"350623199503100002"
# },{
#     "telephone":"15195861003",
#     "password":"zp123456",
#     "real_name":"陈辉",
#     "nick_name":"机智如我",
#     "id_number":"35062319950310003"
# },{
#     "telephone":"15195861004",
#     "password":"zp123456",
#     "real_name":"赵旖",
#     "nick_name":"UU妹",
#     "id_number":"350623199503100004"
# },{
#     "telephone":"15195861005",
#     "password":"zp123456",
#     "real_name":"曾博辉",
#     "nick_name":"绩点不上４不睡觉",
#     "id_number":"350623199503100005"
# },{
#     "telephone":"15195861006",
#     "password":"zp123456",
#     "real_name":"王雷",
#     "nick_name":"北京北京",
#     "id_number":"350623199503100006"
# },{
#     "telephone":"15195861007",
#     "password":"zp123456",
#     "real_name":"林琴",
#     "nick_name":"琴声悠悠",
#     "id_number":"350623199503100007"
# },{
#     "telephone":"15195861008",
#     "password":"zp123456",
#     "real_name":"崔月",
#     "nick_name":"Call me MayBe",
#     "id_number":"350623199503100008"
# },{
#     "telephone":"15195861009",
#     "password":"zp123456",
#     "real_name":"吴凡",
#     "nick_name":"6666666",
#     "id_number":"350623199503100009"
# }
# ]add_new_person
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
]
def child_creator(upload_number,abbreviated,name,parent_id,user_id=0):
    picture_list = []
    for index in range(1,upload_number+1):
        with open('./missing_person/%s/%s.jpg'%(abbreviated,index), 'rb') as f:
            picture_list.append(base64.b64encode(f.read()))

    # random_spot = random.randint(0,len(location.c_longitude))
    data = {
        'picture_list':picture_list,
        'pic_key':'jpg',
        'name':name,
        'sex':random.randint(0,1),
        'age':random.randint(0,15),
        'relation_telephone':user_info_list[parent_id]['telephone'],
        'relation_name':user_info_list[parent_id]['real_name'],
        'lost_time':time.mktime(datetime.datetime.now().timetuple()),
        # random
        'lost_spot':[location.u_latitude[parent_id],location.u_longitude[parent_id]],
        'description':'please help me, dear!!!!',
        'relation_id':user_id
        }
    return data

# initial location
location = Location()


if __name__ == '__main__':
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
    #             print "error import ! %s"%result
    # print json.dumps(missing_list,indent=2,ensure_ascii=False)

    # register
    # for item in user_info_list:
    #     print register(item)

    # login
    # 在不同的地理位置登录这几个用户
    # for index,item in enumerate(user_info_list):
    #     login(item)
    #     data = {
    #         'coordinates':[location.u_latitude[index],location.u_longitude[index]]
    #     }
    #     print updatestatus(data)

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
    #             print "error import ! %s"%result
    # print json.dumps(missing_list,indent=2,ensure_ascii=False)

    # camera search person
    # camera_count = 0
    # import os
    # while camera_count < 10:
    #     dir="./missing_person"
    #     missing_list = []
    #     for root,dirs,files in os.walk(dir):
    #         name = root[len(dir)+1:]
    #         random_camera = random.randint(1,len(location.c_latitude))
    #         if name != '':
    #             upload_number = random.randint(4,6)
    #             print "use camera :%s, search %s of picture %s"%(random_camera,name,upload_number)
    #             with open('./missing_person/%s/%s.jpg'%(name,upload_number), 'rb') as f:
    #                 content = base64.b64encode(f.read())
    #                 data = {
    #                     'search_picture':content,
    #                     'pic_type':'jpg',
    #                     'coordinate':[location.c_latitude[random_camera-1],location.c_longitude[random_camera-1]],
    #                     'id':random_camera,
    #                     'type':'camera'
    #                 }
    #                 try:
    #                     result = eval(search(data))
    #                     print result
                        
    #                     person_id = result['data']['person_id']
    #                     data = {'person_id':person_id}
    #                     search_name = eval(getPersonDetail(data))['data']['person_info']['name']
    #                     print "origin name is %s, search name is %s, confidence is %s"%(name,search_name,result['data']['confidence'])
    #                 except Exception as e:
    #                     print "error:%s"%(str(e))
    #     camera_count = camera_count + 1

    # person search person
    # import os
    # count = 0 
    # while count < 1:
    #     dir="./missing_person"
    #     missing_list = []
    #     for index,item in enumerate(user_info_list):
    #         login(item)
    #         data = {
    #             'coordinates':[location.u_latitude[index],location.u_longitude[index]]
    #         }
    #         # print updatestatus(data)
    #     for root,dirs,files in os.walk(dir):
    #         name = root[len(dir)+1:]
    #         # select a random person to login
    #         random_person = random.randint(1,len(location.u_latitude)-1)
    #         login(user_info_list[random_person])
    #         data = {
    #             'coordinates':[location.u_latitude[random_person],location.u_longitude[random_person]]
    #         }
    #         # print updatestatus(data)

    #         if name != '':
    #             upload_number = random.randint(4,6)
    #             print "use user search :%s, search %s of picture %s"%(random_person,name,upload_number)
    #             with open('./missing_person/%s/%s.jpg'%(name,upload_number), 'rb') as f:
    #                 content = base64.b64encode(f.read())
    #                 data = {
    #                     'search_picture':content,
    #                     'pic_type':'jpg',
    #                     'coordinate':[location.u_latitude[random_person-1],location.u_longitude[random_person-1]],
    #                     'type':'reporter',
    #                     'id':1 # arbitrary number
    #                 }
    #                 try:
    #                     result = eval(search(data))
    #                     print result
    #                     person_id = result['data']['person_id']
    #                     data = {'person_id':person_id}
    #                     search_name = eval(getPersonDetail(data))['data']['person_info']['name']
    #                     print "origin name is %s, search name is %s, confidence is %s"%(name,search_name,result['data']['confidence'])
    #                 except Exception as e:
    #                     print "error:%s"%(str(e))
    #     count = count + 1


    # 用户跟踪拍摄
    # for index,item in enumerate(user_info_list):
    #     login(item)
    #     data = {
    #         'coordinates':[location.u_latitude[index],location.u_longitude[index]]
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
    #         'coordinate':[location.u_latitude[index],location.u_longitude[index]],
    #         'description':'maybe I find this missing child!'
    #     }
    #     try:
    #         result = eval(compare(data))
    #         print "compare result is %s"%json.dumps(result,indent=2,ensure_ascii=False)
    #     except Exception as e:
    #         print "error:%s"%(str(e))

    # test confirm
    # 在不同的地理位置登录这几个用户

    # confirm()

    # data = {
    #     'person_id':'589966e6af8add4f9beefdee'
    # }
    # print getPersonDetail(data)


    # compare for a specifical person

    # name = '安琪儿'
    # # select a random person to login
    # random_person = 3# random.randint(1,len(location.u_latitude)-1)
    # login(user_info_list[random_person])
    # data = {
    #     'coordinates':[location.u_latitude[random_person],location.u_longitude[random_person]]
    # }
    # # print updatestatus(data)

    # if name != '':
    #     upload_number = random.randint(3,3)
    #     print "use user search :%s, search %s of picture %s"%(random_person,name,upload_number)
    #     with open(unicode('./missing_person/%s/%s.jpg'%(name,upload_number),'utf8'), 'rb') as f:
    #         content = base64.b64encode(f.read())
    #         data = {
    #             'search_picture':content,
    #             'pic_type':'jpg',
    #             'coordinate':[location.u_latitude[random_person-1],location.u_longitude[random_person-1]],
    #             'type':'reporter',
    #             'id':1 # arbitrary number
    #         }
    #         try:
    #             result = eval(search(data))
    #             print result
    #             person_id = result['data']['person_id']
    #             data = {'person_id':person_id}
    #             search_name = eval(getPersonDetail(data))['data']['person_info']['name']
    #             print "origin name is %s, search name is %s, confidence is %s"%(name,search_name,result['data']['confidence'])
    #         except Exception as e:
    #             print "error:%s"%(str(e))


    # login_id = 1
    # login(user_info_list[login_id])
    # data = {
    #     'coordinates':[location.u_latitude[login_id],location.u_longitude[login_id]]
    # }
    # print updatestatus(data)
    # confirm()

    # data = {
    #     'person_id':"58994618af8add4a2da15c86"
    # }
    # print getTrackDetailforweb(data)

    # data = {
    #     'spot':[59,118.5],
    #     'range_longitude':30,
    #     'range_latitude':30

    # }
    # print get_all_track(data)