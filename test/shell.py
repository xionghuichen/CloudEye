#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.3.8
# Modified    :   2017.3.8
# Version     :   1.0




from test_data_creator import user_info_list
from testClient import cj,login, prefix
from user_map import Location
import json
import urllib
import random
import base64
location = Location()
login_id = 3
data = urllib.urlencode(user_info_list[login_id])
    # camera search person
login(user_info_list[login_id])
for item in cj:
    print item.name
    if item.name == 'user_id':
        print "in"
        user_id = item.value


# import os
# dir="./missing_person"
# missing_list = []

# name = '安琪儿'
# upload_number = random.randint(7,7)
# random_person = random.randint(0,8)
# with open(unicode('./missing_person/%s/%s.jpg'%(name,upload_number),'utf8'), 'rb') as f:
#     content = base64.b64encode(f.read())    
#     data = {
#         'id':1, # arbitrary number
#         'search_picture':content,
#         'pic_type':'jpg',
#         'coordinate':[location.u_latitude[random_person-1],location.u_longitude[random_person-1]],
#         'type':'reporter'

#     }
# encode_data = urllib.urlencode(data)
# f= open('body.json','w')
# f.write(encode_data)

api = '/find/searchperson/'
import commands
# (status, output) = commands.getstatusoutput("siege -c 2 -r 10 -b -H 'Content-Type:application/json' 'http://139.196.207.155:9000/user/login POST < body.json'")
host = prefix
(status, output) = commands.getstatusoutput("ab -n 30 -c 30 -b 2048 -p body.json -C user_id=%s -T 'application/x-www-form-urlencoded' '%s/find/searchperson'"%(user_id,host))
api = '/sleep'
# (status, output) = commands.getstatusoutput("ab -n 800 -c 400 -b 2048 -C user_id=%s -T 'application/x-www-form-urlencoded' 'http://139.196.207.155:9000/sleep'"%user_id)

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

'''
Concurrency Level:      100
Time taken for tests:   98.176 seconds
Complete requests:      100
Failed requests:        56
   (Connect: 0, Receive: 0, Length: 56, Exceptions: 0)
Total transferred:      60064 bytes
Total body sent:        11073200
HTML transferred:       45464 bytes
Requests per second:    1.02 [#/sec] (mean)
Time per request:       98176.105 [ms] (mean)
Time per request:       981.761 [ms] (mean, across all concurrent requests)
Transfer rate:          0.60 [Kbytes/sec] received
                        110.15 kb/s sent
                        110.74 kb/s total

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:       13 28872 15273.2  29560   54145  
Processing: 20544 35805 8541.1  35387   56220
Waiting:    20040 35184 8365.1  34806   55717
Total:      54664 64677 14005.2  54665   98175

Percentage of the requests served within a certain time (ms)
  50%  54665
  66%  66074
  75%  75034
  80%  79890
  90%  89451
  95%  94402
  98%  97249
  99%  98175
 100%  98175 (longest request)

 7
down vote
  

By looking at the source code we find these timing points:

apr_time_t start,           /* Start of connection */
           connect,         /* Connected, start writing */
           endwrite,        /* Request written */
           beginread,       /* First byte of input */
           done;            /* Connection closed */

And when request is done some timings are stored as:

        s->starttime = c->start;
        s->ctime     = ap_max(0, c->connect - c->start);
        s->time      = ap_max(0, c->done - c->start);
        s->waittime  = ap_max(0, c->beginread - c->endwrite);

And the 'Processing time' is later calculated as

s->time - s->ctime;

So if we translate this to a timeline:

t1: Start of connection
t2: Connected, start writing
t3: Request written
t4: First byte of input
t5: Connection closed

Then the definitions would be:

Connect:      t1-t2   Most typically the network latency
Processing:   t2-t5   Time to receive full response after connection was opened
Waiting:      t3-t4   Time-to-first-byte after the request was sent
Total time:   t1-t5


'''

'''

Server Software:        TornadoServer/4.4.1
Server Hostname:        139.196.207.155
Server Port:            9000

Document Path:          /find/searchperson
Document Length:        457 bytes

Concurrency Level:      10
Time taken for tests:   9.042 seconds
Complete requests:      10
Failed requests:        5
   (Connect: 0, Receive: 0, Length: 5, Exceptions: 0)
Total transferred:      6020 bytes
Total body sent:        240830
HTML transferred:       4560 bytes
Requests per second:    1.11 [#/sec] (mean)
Time per request:       9042.478 [ms] (mean)
Time per request:       904.248 [ms] (mean, across all concurrent requests)
Transfer rate:          0.65 [Kbytes/sec] received
                        26.01 kb/s sent
                        26.66 kb/s total

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:       13 1243 1028.5   1208    2953
Processing:  2969 4344 1098.1   4357    6090
Waiting:     2817 3987 965.1   3916    5470
Total:       3572 5586 2067.2   5589    9042

Percentage of the requests served within a certain time (ms)
  50%   5589
  66%   6472
  75%   7308
  80%   8170
  90%   9042
  95%   9042
  98%   9042
  99%   9042
 100%   9042 (longest request)



 # 使用yield c = 20
Concurrency Level:      20
Time taken for tests:   16.012 seconds
Complete requests:      20
Failed requests:        10
   (Connect: 0, Receive: 0, Length: 10, Exceptions: 0)
Total transferred:      11964 bytes
Total body sent:        480640
HTML transferred:       9084 bytes
Requests per second:    1.25 [#/sec] (mean)
Time per request:       16011.714 [ms] (mean)
Time per request:       800.586 [ms] (mean, across all concurrent requests)
Transfer rate:          0.73 [Kbytes/sec] received
                        29.31 kb/s sent
                        30.04 kb/s total

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    1   0.8      2       2
Processing:  4702 9312 2966.9   9149   16009
Waiting:     4702 9312 2966.9   9149   16009
Total:       4704 9313 2966.8   9151   16011
WARNING: The median and mean for the initial connection time are not within a normal deviation
        These results are probably not that reliable.

Percentage of the requests served within a certain time (ms)
  50%   9151
  66%  11240
  75%  11966
  80%  12205
  90%  12807
  95%  16011
  98%  16011
  99%  16011
 100%  16011 (longest request)




Server Software:        TornadoServer/3.1
Server Hostname:        127.0.0.1
Server Port:            9000

Document Path:          /find/searchperson
Document Length:        455 bytes

Concurrency Level:      1
Time taken for tests:   1.467 seconds
Complete requests:      1
Failed requests:        0
Total transferred:      599 bytes
Total body sent:        24032
HTML transferred:       455 bytes
Requests per second:    0.68 [#/sec] (mean)
Time per request:       1466.882 [ms] (mean)
Time per request:       1466.882 [ms] (mean, across all concurrent requests)
Transfer rate:          0.40 [Kbytes/sec] received
                        16.00 kb/s sent
                        16.40 kb/s total

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.0      0       0
Processing:  1467 1467   0.0   1467    1467
Waiting:     1467 1467   0.0   1467    1467
Total:       1467 1467   0.0   1467    1467





Server Software:        TornadoServer/3.1
Server Hostname:        127.0.0.1
Server Port:            9000

Document Path:          /find/searchperson
Document Length:        453 bytes

Concurrency Level:      30
Time taken for tests:   25.070 seconds
Complete requests:      30
Failed requests:        13
   (Connect: 0, Receive: 0, Length: 13, Exceptions: 0)
Total transferred:      17942 bytes
Total body sent:        720960
HTML transferred:       13622 bytes
Requests per second:    1.20 [#/sec] (mean)
Time per request:       25069.754 [ms] (mean)
Time per request:       835.658 [ms] (mean, across all concurrent requests)
Transfer rate:          0.70 [Kbytes/sec] received
                        28.08 kb/s sent
                        28.78 kb/s total

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        1    1   0.1      1       1
Processing:  8223 14670 4619.2  14251   25069
Waiting:     8223 14670 4619.2  14251   25069
Total:       8224 14670 4619.2  14252   25069

Percentage of the requests served within a certain time (ms)
  50%  14252
  66%  15601
  75%  17005
  80%  17410
  90%  22648
  95%  23180
  98%  25069
  99%  25069
 100%  25069 (longest request)


Server Software:        TornadoServer/3.1
Server Hostname:        127.0.0.1
Server Port:            9000

Document Path:          /find/searchperson
Document Length:        455 bytes

Concurrency Level:      50
Time taken for tests:   38.157 seconds
Complete requests:      50
Failed requests:        35
   (Connect: 0, Receive: 0, Length: 35, Exceptions: 0)
Total transferred:      29948 bytes
Total body sent:        1201600
HTML transferred:       22748 bytes
Requests per second:    1.31 [#/sec] (mean)
Time per request:       38157.321 [ms] (mean)
Time per request:       763.146 [ms] (mean, across all concurrent requests)
Transfer rate:          0.77 [Kbytes/sec] received
                        30.75 kb/s sent
                        31.52 kb/s total

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        2    2   0.1      2       2
Processing:  9541 24337 6418.0  24980   38154
Waiting:     9540 24337 6418.0  24980   38154
Total:       9542 24339 6418.0  24982   38156

Percentage of the requests served within a certain time (ms)
  50%  24982
  66%  27489
  75%  28644
  80%  29570
  90%  30496
  95%  37268
  98%  38156
  99%  38156
 100%  38156 (longest request)
'''