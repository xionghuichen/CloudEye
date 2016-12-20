import pymongo
import datetime
# conenction
client = pymongo.MongoClient("139.196.207.155",27017)

# get a database
db = client.test
# login in with user.
client.admin.authenticate("admin","zp19950310")

# save a record.
# db.my_collection.save({"x":10})

# post
post = {"author": "Mike",
         "text": "My first blog post!",
         "tags": ["mongodb", "python", "pymongo"],
         "date": datetime.datetime.utcnow()}
posts = db.posts

post_id = posts.insert(post)

