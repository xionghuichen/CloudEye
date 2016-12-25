# passpara.py

def test1(dic):
    for item in dic:
        del item['a']

def test2(dic):
    for item in dic:
        item['a'] =2

a = [{'a':1,'b':1},{'a':1,'b':1}]
# test1(a)
test2(a)
print a

def _filter_user(users,user):
    """Delete user_id from users if user_id in users.

    Args:
        users: user_id list
        user: user_id to be deleted.

    Returns:
        new_user_list
    """
    index = 0
    for item in users:
        print index,item
        if item == user:
            del users[index]
        else:
            index+=1
    return users
users = [1,2,3,4,5,6,6,7,7,8,9]

def list_filter(list_unit):
    if list_unit != 7:
        return list_unit

print filter(list_filter, users)