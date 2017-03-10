#-*- coding: utf-8 -*-


# 您需要先注册一个App，并将得到的API key和API secret写在这里。
# You need to register your App first, and enter you API key/secret.
API_KEY = "qZAdC0nEQDEDgC4tdvLiHjwnZWlw08Bm"
API_SECRET = "fd0uEymgpqkdrhZCc-h5QLBYavDD0g0j"

# 网络图片的URL地址,调用demo前请填上内容
# The url of network picture, please fill in the contents before calling demo
face_one = 'http://bj-mc-prod-asset.oss-cn-beijing.aliyuncs.com/mc-official/images/face/demo-pic11.jpg'
# 本地图片的地址,调用demo前请填上内容
# Local picture location, please fill in the contents before calling demo
face_two = './demo.jpeg'
# 本地图片的地址,调用demo前请填上内容
# Local picture location, please fill in the contents before calling demo
face_search = './demo.jpeg'


# Import system libraries and define helper functions
# 导入系统库并定义辅助函数
from pprint import pformat


def print_result(hit, result):
    def encode(obj):
        if type(obj) is unicode:
            return obj.encode('utf-8')
        if type(obj) is dict:
            return {encode(v): encode(k) for (v, k) in obj.iteritems()}
        if type(obj) is list:
            return [encode(i) for i in obj]
        return obj
    print hit
    result = encode(result)
    print '\n'.join("  " + i for i in pformat(result, width=75).split('\n'))


# First import the API class from the SDK
# 首先，导入SDK中的API类
from facepp import API, File
import time
api = API(API_KEY, API_SECRET)

# 创建一个Faceset用来存储FaceToken
# create a Faceset to save FaceToken
# f524168cdcdeec57b2298ac6026e95ac
ret = api.faceset.removeface(outer_id='formal_cloudeye',face_tokens='RemoveAllFaceTokens')
print_result("faceset create", ret)
# time.sleep(1)
# # 对图片进行检测
# # detect image

# Face = {}
# # res = api.detect(image_url=face_one)
# # print_result("person_one", res)
# # Face['person_one'] = res["faces"][0]["face_token"]
# # time.sleep(2)
# # res = api.detect(image_file=File(face_two))
# # print_result("person_two", res)
# # Face['person_two'] = res["faces"][0]["face_token"]
# # time.sleep(1)
# # 将得到的FaceToken存进Faceset里面
# # save FaceToken in Faceset
# # api.faceset.addface(outer_id='test1', face_tokens=Face.itervalues())
# # time.sleep(5)
# # 对待比对的图片进行检测，再搜索相似脸
# # detect image and search same face
# ret = api.detect(image_file=File(face_search))
# print_result("detect", ret)

# time.sleep(10)
# search_result = api.search(face_token=ret["faces"][0]["face_token"], outer_id='test1')

# # 输出结果
# # print result
# print_result('search', search_result)
# print '=' * 60
# for k, v in Face.iteritems():
#     if v == search_result['results'][0]['face_token']:
#         print 'The person with highest confidence:', k
#         break


# # 删除无用的人脸库
# # delect faceset because it is no longer needed
# api.faceset.delete(outer_id='test', check_empty=0)

# 恭喜！您已经完成了本教程，可以继续阅读我们的API文档并利用Face++ API开始写您自
# 己的App了！
# 旅途愉快 :)
# Congratulations! You have finished this tutorial, and you can continue
# reading our API document and start writing your own App using Face++ API!
# Enjoy :)
