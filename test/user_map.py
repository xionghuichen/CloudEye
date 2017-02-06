#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2917.1.5
# Modified    :   2917.1.5
# Version     :   1.0

import matplotlib.pyplot as plt
# user_map.py
            #   1       2       3   4       5       6   7     8       9
u_latitude = [31.885,31.895,31.89,31.88,31.875,31.885,31.88,31.901,32.00]
u_longtitude = [118.79,118.80,118.82,118.86,118.88,118.895,118.94,118.895,119]
c_latitude = [31.88,31.89]
c_longtitude = [118.815,118.90]
if __name__ == "__main__":
    plt.plot(u_longtitude,u_latitude,'bo')
    plt.plot(c_longtitude,c_latitude,'go')
    for index,item in enumerate(c_longtitude):
        plt.annotate('c:%s[%s,%s]'%(index+1,str(c_longtitude[index]),str(c_latitude[index])),xy=(c_longtitude[index],c_latitude[index]),xytext=(c_longtitude[index],c_latitude[index]))


    for index,item in enumerate(u_latitude):
        plt.annotate('u%s[%s,%s]'%(index+1,str(u_longtitude[index]),str(u_latitude[index])),xy=(u_longtitude[index],u_latitude[index]),xytext=(u_longtitude[index],u_latitude[index]))

    plt.title("user map")
    plt.ylabel("latitude")
    plt.xlabel("longtitude")
    plt.show()
