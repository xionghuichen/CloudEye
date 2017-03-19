#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2917.1.5
# Modified    :   2917.1.5
# Version     :   1.0

import matplotlib.pyplot as plt
import random
# user_map.py
            #   1       2       3   4       5       6   7     8       9

o_u_latitude = [32.1017,32.0924,32.0753,32.1247,32.0263,31.9739,31.8826,31.7393,31.9430]
o_u_longitude = [118.7511,118.8064,118.6511,118.8977,118.8063,118.8040,118.7678,118.8839,118.9046]
def random_coordiante(origin):
    for index, item in enumerate(origin):
        plus = random.randint(0,1)
        if plus == 0:
            plus = -1
        origin[index] = round(item + (plus*random.randint(0,30)/1000.0),4)
    return origin
u_latitude = random_coordiante(o_u_latitude)
u_longitude = random_coordiante(o_u_longitude)

o_c_latitude = [31.88,31.89]
o_c_longitude = [118.815,118.90]
c_latitude = random_coordiante(o_c_latitude)
c_longitude = random_coordiante(o_c_longitude)
# if __name__ == "__main__":
#     plt.plot(u_longitude,u_latitude,'bo')
#     plt.plot(c_longitude,c_latitude,'go')
#     for index,item in enumerate(c_longitude):
#         plt.annotate('c:%s[%s,%s]'%(index+1,str(c_longitude[index]),str(c_latitude[index])),xy=(c_longitude[index],c_latitude[index]),xytext=(c_longitude[index],c_latitude[index]))


#     for index,item in enumerate(u_latitude):
#         plt.annotate('u%s[%s,%s]'%(index+1,str(u_longitude[index]),str(u_latitude[index])),xy=(u_longitude[index],u_latitude[index]),xytext=(u_longitude[index],u_latitude[index]))

#     plt.title("user map")
#     plt.ylabel("latitude")
#     plt.xlabel("longitude")
#     plt.show()
