# -*- coding : utf-8 -*-
# @Time      : 2022-01-05 0:06
# @Author    : Zong
# @File      : app.py
# @Software  : PyCharm
# @Function  : 登录和文件管理
# @ChangeLog :

import os
from flask import Flask, request, render_template, session, redirect, flash
from werkzeug.utils import secure_filename
import Admin


# App
app = Flask(__name__)
app.secret_key = 'I have a dream.'  # secret
app.debug = True


# 初始界面 / -> /index -> /login
@app.route('/')
def start():
    return redirect('/subscribe')


# 登陆界面 post -> index
# 用户登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    # session
    user_info = session.get('user_info')

    if request.method == 'GET':
        if not user_info:
            return render_template('loginAn.html')
        else:
            return redirect('/newspapers')

    # 旁观者获取用户
    content = Admin.Connect("root", "@hyh549120")
    cur = content.cursor()
    cur.execute("select UserName, UserPwd from Users;")

    # post
    identity = request.form.get('permission')
    user = request.form.get('name')
    pwd = request.form.get('password')

    # 管理员唯一
    if identity == 'domain':
        if user == 'Admin' and pwd == '123456':
            session['user_info'] = user
            return redirect('/newspapers')

    # 其他人不唯一
    for curRow in cur:
        if user == curRow[0] and pwd == curRow[1]:
            session['user_info'] = user
            return redirect('/subscribe')

    flash('账号或者密码错误！')
    return redirect('/login')


# 注册界面
@app.route('/sign', methods=['GET', 'POST'])
def sign():
    # session
    user_info = session.get('user_info')

    if request.method == 'GET':
        flash("balabala")
        if not user_info:
            return render_template('sign.html')
        else:
            return redirect('/newspapers')

    # 旁观者获取用户
    content = Admin.Connect("root", "@hyh549120")

    # post
    name = request.form.get('name')
    password = request.form.get('password')
    phoneNum = request.form.get('phoneNum')
    email = request.form.get('email')
    address = request.form.get('address')
    name = "'" + name + "'"
    password = "'" + password + "'"
    phoneNum = "'" + phoneNum + "'"
    email = "'" + email + "'"
    address = "'" + address + "'"

    flag = Admin.AddUser(content, name, password, phoneNum, email, address)
    flash(flag)
    if(flag):
        return redirect('/login')
    else:
        return redirect('/sign')


# 主界面
@app.route('/index')
def index():
    # session
    user_info = session.get('user_info')

    if not user_info:
        return redirect('/login')

    # 管理员界面
    if user_info == 'Admin':
        return render_template('index.html')

    return render_template('index.html')


# 退出界面 /logout -> /login
@app.route('/logout')
def logout():
    del session['user_info']
    return redirect('/login')


# 报刊界面
@app.route('/newspapers', methods=['GET', 'POST'])
def newspapers():
    user_info = session.get('user_info')
    context={'user_info': user_info}
    content = Admin.Connect("root", "@hyh549120")

    if request.method == 'GET':
        if not user_info:
            return redirect('/login')

        cur = Admin.ViewNewspapers(content)
        return render_template('newspapers.html', newspapers=cur, **context)

    # 获取标记
    add = request.form.get('add')
    update = request.form.get('update')
    if request.form.get('yes') == None and request.form.get("no") == None:
        deleteOrSubscribeFlag = None
    elif request.form.get('yes') == 'yes':
        deleteOrSubscribeFlag = True
    else:
        deleteOrSubscribeFlag = False

    # 操作判断
    if add == 'add' or update != None:
        name = request.form.get('name')
        price = request.form.get('price')
        updateTime = request.form.get('updateTime')
        kind = request.form.get('kind')
        copies = request.form.get('copies')

        # 修改类型
        name = "'" + name + "'"
        kind = "'" + kind + "'"
        updateTime = "'" + updateTime + "'"
        price = float(price)
        copies = int(copies)

        if(add == 'add'):
            flag = Admin.AddNewspaper(content, name, kind, updateTime, price, copies)
        else:
            flag = Admin.UpdateNewspaper(content, name, kind, updateTime, price, copies, int(update))
        flash(flag)

    if deleteOrSubscribeFlag == True:
        delID = request.form.get('delID')
        subID = request.form.get('subID')
        if delID != None:
            ID = int(delID)
            flag = Admin.DelNewspaper(content, ID)
            flash(flag)

        else:
            ID = int(subID)
            user_info = "'" + user_info + "'"
            flag = Admin.AddSubscribe(content, user_info, ID)
            flash(flag)
    return redirect('/newspapers')


# 用户界面
@app.route('/users', methods=['GET', 'POST'])
def users():
    user_info = session.get('user_info')
    context={'user_info': user_info}
    content = Admin.Connect("root", "@hyh549120")

    if request.method == 'GET':
        if not user_info:
            return redirect('/login')

        # 管理员界面
        if user_info == 'Admin':
            cur = Admin.ViewUsers(content)
        # 普通用户
        else:
            user_info = "'" + user_info + "'"
            cur = Admin.ViewSingleUser(content, user_info)

        return render_template('users.html', users=cur, **context)

    # 获取标记
    add = request.form.get('add')
    update = request.form.get('update')
    if request.form.get('yes') == None and request.form.get("no") == None:
        deleteOrSubscribeFlag = None
    elif request.form.get('yes') == 'yes':
        deleteOrSubscribeFlag = True
    else:
        deleteOrSubscribeFlag = False

    # 操作判断
    if add == 'add' or update != None:
        name = request.form.get('name')
        password = request.form.get('password')
        phoneNum = request.form.get('phoneNum')

        # 修改类型
        name = "'" + name + "'"
        password = "'" + password + "'"
        phoneNum = "'" + phoneNum + "'"

        if(add == 'add'):
            flag = Admin.AddUser(content, name, password, phoneNum)
        else:
            flag = Admin.UpdateUser(content, name, password, phoneNum)
        flash(flag)

    if deleteOrSubscribeFlag == True:
        name = request.form.get('delID')
        if name != None:
            name = "'" + name + "'"
            flag = Admin.DelUser(content, name)
            flash(flag)
    return redirect('/users')


# 订阅界面
@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    user_info = session.get('user_info')
    context={'user_info': user_info}
    content = Admin.Connect("root", "@hyh549120")

    if request.method == 'GET':
        if not user_info:
            return redirect('/login')

        # 管理员界面
        if user_info == 'Admin':
            cur = Admin.ViewSubscribeAndNews(content)
            sum = 0
        # 普通用户
        else:
            user_info = "'" + user_info + "'"
            cur = Admin.ViewPartSubscribeAndNews(content, user_info)
            sum = Admin.GetUserSumPrice(content, user_info)

        return render_template('subscribe.html', subscribes=cur, sum = sum, **context)

    # 获取标记
    add = request.form.get('add')
    update = request.form.get('update')
    if request.form.get('yes') == None and request.form.get("no") == None:
        deleteOrSubscribeFlag = None
    elif request.form.get('yes') == 'yes':
        deleteOrSubscribeFlag = True
    else:
        deleteOrSubscribeFlag = False

    # 操作判断
    if add == 'add' or update != None:
        name = request.form.get('name')
        newsName = request.form.get('newsName')
        updateTime = request.form.get('updateTime')

        # 修改类型
        name = "'" + name + "'"
        newsName = "'" + newsName + "'"
        updateTime = "'" + updateTime + "'"

        if(add == 'add'):
            flag = Admin.AddSubscribeByName(content, name, newsName, updateTime)
        else:
            flag = Admin.UpdateUser(content, name, newsName, updateTime)
        flash(flag)

    if deleteOrSubscribeFlag == True:
        name = request.form.get('delID')
        newsName = request.form.get('newsName')
        updateTime = request.form.get('updateTime')
        if name != None:
            name = "'" + name + "'"
            newsName = "'" + newsName + "'"
            updateTime = "'" + updateTime + "'"
            flag = Admin.DelSubscribe(content, name, newsName, updateTime)
            flash(flag)
    return redirect('/subscribe')


if __name__ == '__main__':
    app.run()
