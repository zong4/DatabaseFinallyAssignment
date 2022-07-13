import pymysql
import Admin
import Config

content = Admin.Connect('root', '@hyh549120')
if content == None:
    print("没有content")

Admin.Start(content)
name = "'" + "zong" + "'"
# cur = content.cursor()
# cur.execute("insert into Users values({}, {}, {})".format(name, '123456', '18367378370'))
# content.commit()
# sum = Admin.GetUserSumPrice(content, name)
# print(sum)
#
#
# for i in cur:
#     print(i)

