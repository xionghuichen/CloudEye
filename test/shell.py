#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.3.8
# Modified    :   2017.3.8
# Version     :   1.0




from test_data_creator import user_info_list
import json
import urllib
import random
import base64
from user_map import u_latitude, u_longitude
login_id = 0
data = urllib.urlencode(user_info_list[login_id])
    # camera search person

import os
# dir="./missing_person"
# missing_list = []

# name = '王海萍'
# upload_number = random.randint(4,6)
# random_person = random.randint(0,8)
# with open(unicode('./missing_person/%s/%s.jpeg'%(name,upload_number),'utf8'), 'rb') as f:
#     content = base64.b64encode(f.read())    
#     data = {
#         'id':1, # arbitrary number
#         'search_picture':content,
#         'pic_type':'jpg',
#         'coordinate':[u_latitude[random_person-1],u_longitude[random_person-1]],
#         'type':'reporter'

#     }
# encode_data = urllib.urlencode(data)
# f= open('body.json','w')
# f.write(encode_data)

api = '/find/searchperson/'
import commands
# (status, output) = commands.getstatusoutput("siege -c 2 -r 10 -b -H 'Content-Type:application/json' 'http://139.196.207.155:9000/user/login POST < body.json'")
(status, output) = commands.getstatusoutput("ab -n 35 -c 35 -b 2048 -p body.json -T 'application/x-www-form-urlencoded' 'http://139.196.207.155:9000/find/searchperson'")
print output
'''
Transactions: 30000 hits //完成30000次处理
Availability: 100.00 % //100.00 % 成功率
Elapsed time: 68.59 secs //总共使用时间
Data transferred: 817.76 MB //共数据传输 817.76 MB
Response time: 0.04 secs //响应时间，显示网络连接的速度
Transaction rate: 437.38 trans/sec //平均每秒完成 437.38 次处理
Throughput: 11.92 MB/sec //平均每秒传送数据
Concurrency: 17.53 //实际最高并发连接数
Successful transactions: 30000 //成功处理次数
Failed transactions: 0 //失败处理次数
Longest transaction: 3.12 //每次传输所花最长时间
Shortest transaction: 0.00 //每次传输所花最短时间 
'''

'''

Server Software:        TornadoServer/4.4.1
Server Hostname:        139.196.207.155
Server Port:            9000

Document Path:          /find/searchperson
Document Length:        96 bytes

Concurrency Level:      35
Time taken for tests:   78.950 seconds
Complete requests:      35
Failed requests:        0
Total transferred:      8435 bytes
Total body sent:        11834795
HTML transferred:       3360 bytes
Requests per second:    0.44 [#/sec] (mean)
Time per request:       78949.779 [ms] (mean)
Time per request:       2255.708 [ms] (mean, across all concurrent requests)
Transfer rate:          0.10 [Kbytes/sec] received
                        146.39 kb/s sent
                        146.49 kb/s total

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:       13 37248 22752.1  38469   75042
Processing:  3907 40062 22671.4  41045   77250
Waiting:     1688 37855 22700.0  38793   75818
Total:      77262 77310 285.2  77262   78949

Percentage of the requests served within a certain time (ms)
  50%  77262
  66%  77262
  75%  77262
  80%  77262
  90%  7.7262
  95%  77262
  98%  78949
  99%  78949
 100%  78949 (longest request)
'''