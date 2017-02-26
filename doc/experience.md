### 一个方法的灵活性和封装性是可能存在冲突的，如何解决这个冲突？
eg. def find_user_in_range(self, coordinate, distance),这个接口，用来获取一定经纬度范围的用户，
我这里使用了distance的参数，让用户自己标定查找范围，这样就可以适应不同distance的查找需求，
- 方案一，使用distance参数，封装性下降，灵活性上升：
比如我修改了find_user_in_range的实现机制，我发现需要使用类似椭圆的形式进行查找，那么这个函数的输入参数就需要修改，由原本的distance变成长轴和短轴两个参数，所有用到这个方法的地方都要进行修改
- 方案二，不使用distance参数，封装性上升，灵活性下降：
如果我之前设计的时候假设distance使用固定的距离，那么这个时候他的封装性就提升了，当我需要修改其实现机制，变成椭圆的时候，此时我不需要修改所有用到这个方法的地方，只需要修改这个方法的内部实现就行。
- 解决方案：
在我的应用中，find_user_in_range()这个方法涉及到的distance是需要被提出来的，因为不同的用户组，使用的range是不一样的(警察和普通用户)，方法改成find_user_in_range(self, coordinate, length,width)
- 结论：
不要盲目的增加一个方法的灵活性，因为这样的代价就是损失他的封装性，逻辑设计的变动可能导致一系列的改动，也就是耦合性也会提高；但是适当的考虑方法的通用性是必要的，它能够提高代码重用率。我的方法论是，考虑一个方法所可能的灵活程度是怎么样的，在满足灵活度需求的基础上最大限度提高其封装性

### matplotlib 使用注释
for index,item in enumerate(c_longtitude):
    plt.annotate('c:%s[%s,%s]'%(index+1,str(c_longtitude[index]),str(c_latitude[index])),xy=(c_longtitude[index],c_latitude[index]),xytext=(c_longtitude[index],c_latitude[index]))
- 第一个参数是注释内容
- xy 参数是注释所在坐标
- xytext是注释文本所在位置

### 报错 UnicodeEncodeError: 'latin-1' codec can't encode character

    "UnicodeEncodeError:'latin-1' codec can't encode character ..."

    This is because MySQLdb normally tries to encode everythin to latin-1. This can be fixed by executing the following commands right after you've etablished the connection:

    db.set_character_set('utf8')
    dbc.execute('SET NAMES utf8;') dbc.execute('SET CHARACTER SET utf8;')
    dbc.execute('SET character_set_connection=utf8;')

        "db" is the result of MySQLdb.connect, and "dbc" is the result of db.cursor().

    意思就是MySQLdb正常情况下会尝试将所有的内容转为latin1字符集处理

    所以处理方法就是，设置连接和游标的charset为你所希望的编码，如utf8

    db是connection连接，dbc是数据库游标

    对于 sqlachemy： 把connstr修改为connstr = 'mysql://uid:pwd@localhost/mydb?charset=utf8'
### 图片格式批量转化：
mogrify -format jpg *.jpeg
将该目录中所有jpeg的文件转化成jpg文件
### json输出中文
print json.dumps(missing_list,indent=2,ensure_ascii=False)
### 防火墙配置规则
    - 掩码： 
        - 对地址做与操作，都为1则为1，否则为0
        - 表示法： 192.168.1.0/24 表示一个C类地址，24表示前面有24个1，也就是255.255.255.0
    - 博文：
        - http://blog.csdn.net/wlzx120/article/details/52300793
        - http://www.jb51.net/LINUXjishu/155175.html
    - 家里使用路由器上网，使用ifconfig 获得的是局域网ip，使用局域网ip配置的防火墙是不能用的
        - 获取公网ip的方法
            - 百度 ip地址
            - wget http://members.3322.org/dyndns/getip
            - wget http://ifconfig.me/ip 

### 放弃本地修改，同步远程更新
1. git reset -hard origin/对应分支
2. git pull origin/对应分支