import pymongo
import datetime
# conenction
client = pymongo.MongoClient("139.196.207.155",27017)

# get a database
db = client.cloudeye
# login in with user.
client.cloudeye.authenticate("burningbear","zp19950310")

# save a record.
# db.my_collection.save({"x":10})

# post
# post = {"author": "Mike",
#          "text": "My first blog post!",
#          "tags": ["mongodb", "python", "pymongo"],
#          "date": datetime.datetime.utcnow()}
# posts = db.posts

# post_id = posts.insert(post)


results = db.person.info.find({"parent_telephone":"15195861108"})
# if results == None:
#     for result in results:
#         print 'hello'
# else:
#     print '2'
for result in results:
    print result['_id']