# -*- coding : utf-8 -*-
# @Time      : 2022/6/7 10:29
# @Author    : Zong
# @File      : Admin.py
# @Software  : PyCharm
# @Function  : 
# @ChangeLog :

import pymysql


# 连接
def Connect(user, pwd):
    try:
        content = pymysql.Connect(
            host = '120.48.57.129',  # mysql的主机ip
            port = 3306,  # 端口
            user = user,  # 用户名
            passwd = pwd,  # 数据库密码
            db = 'SubscribeNewspapers',  # 数据库名
            charset = 'utf8',  # 字符集
        )
        print("管理员登陆成功")
        return content

    except:
        print("管理员登陆失败")
        return None


# 初始化（执行一次）
def Start(content):
    cur = content.cursor()

    # 删除表
    try:
        #cur.execute("")
        cur.execute("DROP TABLE Subscribe;")
        cur.execute("DROP TABLE Newspapers;")
        cur.execute("DROP TABLE Users;")
        print("删除成功")
    except:
        print("删除失败")

    # Newspapers
    cur.execute("CREATE TABLE IF NOT EXISTS Newspapers( NewsID INT UNSIGNED AUTO_INCREMENT, NewsName CHAR(50) NOT NULL, Kind CHAR(20) NOT NULL, UpdateTime CHAR(10) NOT NULL, Price FLOAT UNSIGNED NOT NULL, Copies INT UNSIGNED NOT NULL, PRIMARY KEY ( NewsID )) CHARSET=utf8;")

    print("Newspapers建立成功")

    # 联合unique
    cur.execute("Alter table Newspapers add  UNIQUE key(NewsName,UpdateTime);")
    content.commit()

    # Peoples
    # cur.execute(
    #     "CREATE TABLE IF NOT EXISTS Users(UserName CHAR(50) NOT NULL, UserPwd CHAR(50) NOT NULL, PhoneNum CHAR(11) NOT NULL UNIQUE, PRIMARY KEY (UserName)) CHARSET=utf8;")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Users(UserName CHAR(50) NOT NULL, UserPwd CHAR(50) NOT NULL, PhoneNum CHAR(11) NOT NULL UNIQUE, PRIMARY KEY (UserName), Email CHAR(20), Address CHAR(20)) CHARSET=utf8;")
    content.commit()
    print("Users建立成功")

    # Records
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Subscribe(UserName CHAR(50) NOT NULL, NewsID INT UNSIGNED, Num INT UNSIGNED NOT NULL, FOREIGN KEY(UserName) REFERENCES Users(UserName) ON DELETE CASCADE, FOREIGN KEY(NewsID) REFERENCES Newspapers(NewsID) ON DELETE CASCADE, Primary KEY(Username, NewsID)) CHARSET=utf8;")
    content.commit()
    print("Subscribe建立成功")


# 测试用
# 查看所有表
def ViewTables(content):
    cur = content.cursor()
    cur.execute("show tables;")
    # 返回游标
    return cur

# 删除表
def DeleteTable(content, tableName):
    cur = content.cursor()

    cur.execute("DROP TABLE IF EXISTS " + tableName + ";")
    content.commit()
    print("删除" + tableName + "成功")


# Users
# 查看用户
def ViewUsers(content):
    cur = content.cursor()
    cur.execute("select * from Users;")
    return cur

def ViewSingleUser(content, name):
    cur = content.cursor()
    cur.execute("select * from Users where UserName={};".format(name))
    return cur

# 添加用户
def AddUser(content, userName, userPwd, phoneNum, email, address):
    cur = content.cursor()
    try:
        cur.execute("insert into Users values({}, {}, {}, {}, {});".format(userName, userPwd, phoneNum, email, address))
        content.commit()
        return True
    except:
        content.rollback()
        return False

# 删除用户
def DelUser(content, userName):
    cur = content.cursor()

    try:
        cur.execute("delete from Users where UserName={};".format(userName))
        content.commit()
        return True

    except:
        content.rollback()
        return False

# 修改
def UpdateUser(content, name, pwd, phoneNum):
    cur = content.cursor()
    try:
        cur.execute("update Users set UserName={}, UserPwd={}, PhoneNum={} where UserName={};".format(name, pwd, phoneNum, name))
        content.commit()
        return True

    except:
        content.rollback()
        return False


# Newspapers
# 查看
def ViewNewspapers(content):
    cur = content.cursor()
    cur.execute("select * from Newspapers;")
    return cur

# 添加
def AddNewspaper(content, newsName, kind, updateTime, price, copies):
    cur = content.cursor()
    try:
        cur.execute("insert into Newspapers(NewsName, Kind, UpdateTime, Price, Copies) values({}, {}, {}, {}, {});".format(newsName, kind, updateTime, price, copies))
        content.commit()
        return True
    except:
        content.rollback()
        return False

# 删除
def DelNewspaper(content, newsID):
    cur = content.cursor()

    try:
        cur.execute("delete from Newspapers where NewsID={};".format(newsID))
        content.commit()
        return True

    except:
        content.rollback()
        return False

# 修改
def UpdateNewspaper(content, newsName, kind, updateTime, price, copies, ID):
    cur = content.cursor()
    try:
        cur.execute("update Newspapers set NewsName={}, Kind={}, UpdateTime={}, Price={}, Copies={} where NewsID={};".format(newsName, kind, updateTime, price, copies, ID))
        content.commit()
        return True

    except:
        content.rollback()
        return False


# 订阅
def AddSubscribe(content, userName, newID):
    cur = content.cursor()
    try:
        # 获取旧数量
        cur.execute("select Copies from Newspapers where NewsID={};".format(newID))
        for i in cur:
            copies = i[0]

        # 判断是否>0
        if(copies <= 0):
            return False

        cur.execute("insert into Subscribe() values({}, {}, {});".format(userName, newID, 1))
        content.commit()

        cur.execute("update Newspapers set Copies={} where NewsID={};".format(int(copies) - 1, newID))
        content.commit()

        return True
    except:
        content.rollback()
        return False

def AddSubscribeByName(content, userName, newsName, updateTime):
    cur = content.cursor()
    try:
        # 获取旧数量
        cur.execute("select Copies from Newspapers where NewsName={} and UpdateTime={};".format(newsName, updateTime))
        for i in cur:
            copies = i[0]

        # 获取ID
        cur.execute(
            "select NewsID from Newspapers where NewsName={} and UpdateTime={};".format(newsName, updateTime))
        for i in cur:
            ID = i[0]

        # 判断是否>0
        if(copies <= 0):
            return False

        cur.execute("insert into Subscribe() values({}, {}, {});".format(userName, ID, 1))
        content.commit()

        cur.execute("update Newspapers set Copies={} where NewsName={} and UpdateTime={};".format(int(copies) - 1, newsName, updateTime))
        content.commit()
        return True
    except:
        content.rollback()
        return False

def UpdateSubscribeByName(content, userName, newsName, updateTime):
    cur = content.cursor()
    try:
        # 获取旧数量
        cur.execute("select Copies from Newspapers where NewsName={} and UpdateTime={};".format(newsName, updateTime))
        for i in cur:
            copies = i[0]

        # 获取ID
        cur.execute(
            "select NewsID from Newspapers where NewsName={} and UpdateTime={};".format(newsName, updateTime))
        for i in cur:
            ID = i[0]

        cur.execute("insert into Subscribe() values({}, {}, {});".format(userName, ID, 1))
        content.commit()

        cur.execute("update Newspapers set Copies={} where NewsName={} and UpdateTime={};".format(int(copies) - 1, newsName, updateTime))
        content.commit()
        return True
    except:
        content.rollback()
        return False

def DelSubscribe(content, userName, newsName, updateTime):
    cur = content.cursor()
    try:
        # 获取订阅数量
        cur.execute("select Num from Subscribe,Newspapers where NewsName={} and UpdateTime={};".format(newsName, updateTime))
        for i in cur:
            num = i[0]
        # 获取旧数量
        cur.execute(
            "select Copies from Newspapers where NewsName={} and UpdateTime={};".format(newsName, updateTime))
        for i in cur:
            copies = i[0]

        cur.execute("delete from Subscribe where UserName={} and NewsID in (select NewsID from Newspapers where NewsName={} and UpdateTime={});".format(userName, newsName, updateTime))
        content.commit()

        cur.execute(
            "update Newspapers set Copies={} where NewsName={} and UpdateTime={};".format(
                int(copies) + int(num), newsName, updateTime))
        content.commit()
        return True
    except:
        content.rollback()
        return False

def ViewSubscribe(content):
    cur = content.cursor()
    cur.execute("select * from Subscribe;")
    return cur

def ViewPartSubscribe(content, userName):
    cur = content.cursor()
    cur.execute("select * from Subscribe where UserName={};".format(userName))
    return cur

def ViewSubscribeAndNews(content):
    cur = content.cursor()
    cur.execute("select UserName,NewsName,Kind,UpdateTime,Price,Num from Subscribe,Newspapers where Subscribe.NewsID=Newspapers.NewsID;")
    return cur

def ViewPartSubscribeAndNews(content, userName):
    cur = content.cursor()
    cur.execute("select UserName,NewsName,Kind,UpdateTime,Price,Num from Subscribe,Newspapers where Subscribe.NewsID=Newspapers.NewsID and UserName={};".format(userName))
    return cur


# 获取用户订阅总金额
def GetUserSumPrice(content, userName):
    cur = content.cursor()
    cur.execute("select Price,Num from Subscribe,Newspapers where Subscribe.UserName={} and Subscribe.NewsID=Newspapers.NewsID;".format(userName))
    sum = 0
    for i in cur:
        sum = sum + float(i[0]) * int(i[1])
    return sum