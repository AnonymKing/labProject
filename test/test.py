import hashlib
import pymysql
hashlibHandler = hashlib.md5()
def open_mysql(name):
    db = pymysql.connect(host="localhost", user="root", passwd="370829", db="mylist", port=3306, charset='utf8')
    cursor = db.cursor()
    cursor.execute("select * from tornadoData where username=%s", name)
    results = cursor.fetchall()
    cursor.close()
    db.close()
    return results

userInfo = open_mysql("hgtsdd")
name = userInfo[0][0]
password = userInfo[0][1]
print(name,'---',password)
hashlibHandler.update("hgtsdd".encode('utf-8'))
userpsw = hashlibHandler.hexdigest()
print(userpsw)
print(type(name), type(password), type(userpsw), sep="--")