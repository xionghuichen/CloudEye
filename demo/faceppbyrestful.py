# faceppbyrestful.py
import urllib,urllib2
prefix = 'https://api-cn.faceplusplus.com/facepp/v3/'
import logging

logging.basicConfig(level=logging.INFO,
                    filename='log.log',
                    filemode='w')
from poster.encode import multipart_encode  
from poster.streaminghttp import register_openers 

def set_resquest(api,data,method):
    # data is dictory.
    # method can be get put delete post ?
    # get _xsrff
    # if method != 'GET':
        # data['_xsrf'] = _xsrf
    data = urllib.urlencode(data)
    url = prefix + api
    if method == 'GET':
        url = url + "?"+ data
    headers = { 'Content-type' : 'multipart/form-data'} 
    request = urllib2.Request(url,data,headers)
    request.get_method = lambda: method # or 'DELETE' 

    return request

def prn_obj(obj):
    result = '\n'.join(['%s:%s' % item for item in obj.__dict__.items()])
    logging.info("print obj %s"%result)


data= {
    'api_key':'qZAdC0nEQDEDgC4tdvLiHjwnZWlw08Bm',
    'api_secret':'fd0uEymgpqkdrhZCc-h5QLBYavDD0g0j',
    'image_file':open("./demo.jpeg", "rb")

}
prn_obj(open("./demo.jpeg", "rb"))
logging.info("file is : %s"%str(open("./demo.jpeg", "rb")))
register_openers() 
datagen, headers = multipart_encode(data)  
logging.info("datagen: %s"%datagen)
logging.info("headers:%s"%headers)

request = urllib2.Request(prefix+'detect', datagen, headers)
print eval(urllib2.urlopen(request).read())['faces']


# import time

# with open('./demo.jpeg', 'rb') as f:
#     content = f.read()
# boundary = '----------%s' % hex(int(time.time() * 1000))
# data = []
# data.append('--%s' % boundary)

# data.append('Content-Disposition: form-data; name="%s"\r\n' % 'username')
# data.append('jack')
# data.append('--%s' % boundary)

# data.append('Content-Disposition: form-data; name="%s"\r\n' % 'mobile')
# data.append('13800138000')
# data.append('--%s' % boundary)

# # fr=open(r'/var/qr/b.png','rb')
# data.append('Content-Disposition: form-data; name="%s"; filename="./demo.png"' % 'profile')
# data.append('Content-Type: %s\r\n' % 'image/jpeg')
# data.append(content)
# # data.append(fr.read())
# # fr.close()
# data.append('--%s--\r\n' % boundary)

# http_url=prefix+'detect'
# http_body='\r\n'.join(data)
# try:
#     #buld http request
#     req=urllib2.Request(http_url, data=http_body)
#     #header
#     req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
#     # req.add_header('User-Agent','Mozilla/5.0')
#     # req.add_header('Referer','http://remotserver.com/')
#     #post data to server
#     resp = urllib2.urlopen(req, timeout=5)
#     #get response
#     qrcont=resp.read()
#     print qrcont
    
    
# except Exception,e:
#     print e


# req = set_resquest('detect',data,"POST")
# try:
#     response = urllib2.urlopen(req)
#     the_page = response.read()
#     print the_page
# except Exception as e:
#     print e

