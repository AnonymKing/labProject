import tornado.ioloop
import tornado.web
import sessionClass
import pymysql
import hashlib
from tornado.options import define, options

hashlibHandler = hashlib.md5()#定义一个全局hashlib对象，便于使用

def insert_mysql(username, userpsw, usermail):
    # 打开数据库连接
    db = pymysql.connect(host="localhost", user="root", passwd="370829", db="mylist", port=3306, charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 插入语句
    sql = "INSERT INTO tornadoData(username, userpsw, usermail) VALUES (%s, %s, %s)"
    data = (username, userpsw, usermail)
    try:
        cursor.execute(sql, data)
        db.commit()
    except:
        db.rollback()
    cursor.close()
    db.close()


def open_mysql(name):
    db = pymysql.connect(host="localhost", user="root", passwd="370829", db="mylist", port=3306, charset='utf8')
    cursor = db.cursor()
    cursor.execute("select * from tornadoData where username=%s", name)
    results = cursor.fetchall()
    cursor.close()
    db.close()
    return results


class indexHandler(tornado.web.RequestHandler):  #定义一个类，继承tornado.web下的RequestHandler类
    def get(self):
        session = sessionClass.Session(self, 1)    #创建session对象，cookie保留1天
        if session['zhuangtai'] == True:         #判断session里的zhuangtai等于True
            self.render("index.html")
        else:
            self.redirect("/login")#重定向

class loginHandler(tornado.web.RequestHandler):
    def get(self):
        session = sessionClass.Session(self, 1)
        if session['zhuangtai'] == True:
            self.redirect("/index")
        else:
            self.render("login.html", remind = '')

    def post(self):        
        username = self.get_argument('username')               #接收用户提交的用户名
        userpsw = self.get_argument('userpsw')               #接收用户提交的密码
        hashlibHandler.update(userpsw.encode('utf-8'))
        userpsw = hashlibHandler.hexdigest()

        userInfo = open_mysql(username)
        name = userInfo[0][0]
        password = userInfo[0][1]

        if name == '':
            self.render("login.html", remind = '请先注册！')
            self.redirect("/register")  #用户不存在时跳转注册界面
        elif username == name and userpsw == password:        #判断用户名和密码
            session = sessionClass.Session(self, 1)
            session['username'] = username                     #将用户名保存到session
            session['userpsw'] = userpsw                     #将密码保存到session
            session['zhuangtai'] = True              #在session写入登录状态
            self.redirect("/index")
        else:
            self.render("login.html", remind = '用户名或密码错误')

class registerHandler(tornado.web.RequestHandler):
    def get(self):
        session = sessionClass.Session(self, 1)
        if session['zhuangtai'] == True:
            self.redirect("/index")
        else:
            self.render("register.html", tishi="tishi()")

    def post(self):        
        name = self.get_argument('username')
        password = self.get_argument('password')
        mail = self.get_argument('mail')

        if len(open_mysql(name)) > 0:
        	self.render("register.html", tishi="tishi1()")
        else:
            hashlibHandler.update(password.encode('utf-8'))
            password = hashlibHandler.hexdigest()
            insert_mysql(name, password, mail)
            self.render("register.html", tishi="tishi2()")

#文件配置
settings = {                                        
    "template_path":"htmls",#存放HTML
    "static_path":"statics",#存放js、css、img
}

#路由映射
application = tornado.web.Application([
    (r"/index", indexHandler),
    (r"/login", loginHandler),
    (r"/register", registerHandler),
],**settings)

define("port", default=8000, help="run on the given port", type=int)

if __name__ == "__main__":
    application.listen(options.port)
    print("Starting development server at http://127.0.0.1:"+str(options.port)+"/login")
    print("Quit the server with CONTROL-C.")
    tornado.ioloop.IOLoop.instance().start()