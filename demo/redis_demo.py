# redis_demo.py
import redis
r = redis.Redis(host='localhost',port=6379)
# r.lpush("user",{'12':1})
# print r.lindex("user",1)
# r.delete('user')