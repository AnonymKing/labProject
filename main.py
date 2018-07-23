import os
import redis
import numpy
import pymysql
import tornado.ioloop
import tornado.web
import sessionClass
import hashlib
from tornado.options import define, options

sql_user = "root"
sql_psd = "123456"
db_name = "mylist"
hashlibHandler = hashlib.md5()#定义一个全局hashlib对象，便于使用

# 注册，存储用户信息
def insert_mysql(username, userpsw, usermail):
	con = pymysql.connect(
		  host="localhost",
		  user=sql_user,
		  passwd=sql_psd,
		  db=db_name,
		  port=3306,
		  charset='utf8'
	)
	cur = con.cursor()
	sql = "INSERT INTO tornadoData(username, userpsw, usermail) VALUES (%s, %s, %s)"
	data = (username, userpsw, usermail)
	try:
		cur.execute(sql, data)
		con.commit()
	except:
		con.rollback()
	cur.close()
	con.close()

# 用户名匹配用户信息
def search_mysql(name):
	con = pymysql.connect(
		  host="localhost",
		  user=sql_user,
		  passwd=sql_psd,
		  db=db_name,
		  port=3306,
		  charset='utf8'
	)
	cur = con.cursor()
	cur.execute("select * from tornadoData where username=%s", name)
	results = cur.fetchall()
	cur.close()
	con.close()
	return results

# 数据缓存 redis
def redisTodayInfo():
	con  =  pymysql.connect(
			host = 'localhost',
			port = 3306,
			user = sql_user,
			passwd = sql_psd,
			db = db_name,
			charset = 'utf8',
			cursorclass = pymysql.cursors.DictCursor
	)
	cur  =  con.cursor()
	sql  =  "select * from todayinfo"
	cur.execute(sql)
	info  =  cur.fetchall()
	cur.close()
	con.close()
	r  =  redis.Redis(host = '127.0.0.1', port = 6379)#缓存到内存
	r.set('todayInfo', info)

def redisUserInfo():
	con  =  pymysql.connect(
			host = 'localhost',
			port = 3306,
			user = sql_user,
			passwd = sql_psd,
			db = db_name,
			charset = 'utf8',
			cursorclass = pymysql.cursors.DictCursor
	)
	cur  =  con.cursor()
	sql  =  "select * from userinfo"
	cur.execute(sql)
	info  =  cur.fetchall()
	cur.close()
	con.close()
	r  =  redis.Redis(host = '127.0.0.1', port = 6379)#缓存到内存
	r.set('userInfo', info)

class ifLoginHandler(tornado.web.RequestHandler):  #判断登录状态
	def post(self):#判断登录状态
		session = sessionClass.Session(self, 1)
		if session['static'] == True:
			result = {"state": "true", "user": session['username']}
			self.write(result)
		else:
			result = {"state": "false"}
			self.write(result)

class logoutHandler(tornado.web.RequestHandler):  #注销
	def post(self):#判断登录状态
		session = sessionClass.Session(self, 1)
		if session['static'] == True:
			session['username'] = ''
			session['userpsw'] = ''
			session['static'] = False
			result = {"state": "true"}
			self.write(result)
		else:
			result = {"state": "false"}
			self.write(result)

class loginHandler(tornado.web.RequestHandler):
	def post(self):
		username = self.get_argument('username') #接收用户提交的用户名
		userpsw = self.get_argument('password') #接收用户提交的密码
		hashlibHandler.update(userpsw.encode('utf-8'))
		userpsw = hashlibHandler.hexdigest()

		userInfo = search_mysql(username)
		name = userInfo[0][0]
		password = userInfo[0][1]

		if username == name and userpsw == password: #判断用户名和密码
			session = sessionClass.Session(self, 1)
			session['username'] = username #将用户名保存到session
			session['userpsw'] = userpsw #将密码保存到session
			session['static'] = True #在session写入登录状态
			result = {"state": "true"}
			self.write(result) #返回结果
		else:
			result = {"state": "false"}
			self.write(result) #返回结果

class registerHandler(tornado.web.RequestHandler):
	def post(self):
		username = self.get_argument('username') #接收用户提交的用户名
		userpsw = self.get_argument('password') #接收用户提交的密码
		usermail = self.get_argument('mail')
		if( search_mysql(username) ):
			result = {"state": "false"}
		else:
			hashlibHandler.update(userpsw.encode('utf-8'))
			userpsw = hashlibHandler.hexdigest()
			result = {"state": "true"}
			insert_mysql(username, userpsw, usermail)

class indexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("index.html")

class todayInfoHandler(tornado.web.RequestHandler):
	def post(self):
		self.write({"data": self._get_data()})
	def _get_data(self):
		r  =  redis.Redis(host = '127.0.0.1', port = 6379)
		data  =  r.get('todayInfo')
		data  =  eval(data.decode())
		return data

class userInfoHandler(tornado.web.RequestHandler):
	def post(self):
		self.write({"data": self._get_data()})
	def _get_data(self):
		r  =  redis.Redis(host = '127.0.0.1', port = 6379)
		data  =  r.get('userInfo')
		data  =  eval(data.decode())
		return data

#文件配置
settings  =  {										
	"static_path": os.path.join(os.path.dirname(__file__), "static")
}

#路由映射
application  =  tornado.web.Application([
	(r"/", indexHandler),
	(r"/ajax/todayInfo", todayInfoHandler),
	(r"/ajax/userInfo", userInfoHandler),
	(r"/ajax/login", loginHandler),
	(r"/ajax/logout", logoutHandler),
	(r"/ajax/register", registerHandler),
	(r"/ajax/ifLogin", ifLoginHandler),
],**settings)


define("port", default = 8888, help = "run on the given port", type = int)
if __name__  ==  "__main__":
	redisUserInfo()
	redisTodayInfo() #数据缓存，等待取用
	application.listen(options.port)
	print("Starting development server at http://127.0.0.1:"+str(options.port))
	print("Quit the server with CONTROL-C.")
	tornado.ioloop.IOLoop.instance().start()
