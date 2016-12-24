# passpara.py

def test(dic):
    for item in dic:
        del item['a']

a = [{'a':1,'b':1},{'a':1,'b':1}]
test(a)
print a