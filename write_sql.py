import tushare
import datetime
import numpy
import pymysql.cursors

sql_user = "root"
sql_psd = "370829"
db_name = "mylist"

def getUserInfo():
	data = numpy.array( tushare.get_stock_basics() )
	data = data.tolist()

	con  =  pymysql.Connect(
		    host = 'localhost',
		    port = 3306,
		    user = sql_user,
		    passwd = sql_psd,
		    db = db_name,
		    charset = 'utf8'
		)
	cur  =  con.cursor()

	# 更新数据

	sql  =  """CREATE TABLE userinfo (
		name text,
		industry text,
		area text,
		pe double,
		outstanding double,
		totals double,
		totalAssets double
	)"""
	cur.execute(sql)

	for i, d in zip(range(50), data):
		 #插入数据
		sql  =  "INSERT INTO userinfo (name, industry, area, pe, outstanding, totals, totalAssets) VALUES (%s,%s,%s,%s,%s,%s,%s)"
		data  =  ( d[0], d[1], d[2], d[3], d[4], d[5], d[6] )
		cur.execute(sql, data)
		con.commit()
		print('----------%d----------' %i)

	cur.close()
	con.close()


def getDateLine():
	# 取最近100天数据
	end = datetime.datetime.now().strftime("%F")
	start = datetime.datetime.now()+datetime.timedelta(days=-100)
	start = start.strftime("%F")
	temp = numpy.array(tushare.get_k_data("600000", start=start, end=end))
	data = temp.tolist()

	con  =  pymysql.Connect(
		    host = 'localhost',
		    port = 3306,
		    user = sql_user,
		    passwd = sql_psd,
		    db = db_name,
		    charset = 'utf8'
		)
	cur  =  con.cursor()

	# 更新数据
	cur.execute("DROP TABLE IF EXISTS dateline")
	sql  =  """CREATE TABLE dateline (
		id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
		date text,
		open double,
		close double,
		high double,
		low double,
		volume double,
		code text
		)"""
	cur.execute(sql)

	for d in data:
		 #插入数据
		sql  =  "INSERT INTO dateline (date,open,close,high,low,volume,code) VALUES (%s,%s,%s,%s,%s,%s,%s)"
		data  =  ( d[0], d[1], d[2], d[3], d[4], d[5], d[6] )
		cur.execute(sql, data)
		con.commit()

	cur.close()
	con.close()
# code,代码
# name,名称
# industry,所属行业
# area,地区
# pe,市盈率
# outstanding,流通股本(亿)
# totals,总股本(亿)
# totalAssets,总资产(万)
# liquidAssets,流动资产
# fixedAssets,固定资产
# reserved,公积金
# reservedPerShare,每股公积金
# esp,每股收益
# bvps,每股净资
# pb,市净率
# timeToMarket,上市日期
# undp,未分利润
# perundp, 每股未分配
# rev,收入同比(%)
# profit,利润同比(%)
# gpr,毛利率(%)
# npr,净利润率(%)
# holders,股东人数


def getTodayInfo():
	data = numpy.array( tushare.get_today_all() )
	data = data.tolist()

	# 打开数据库
	con  =  pymysql.Connect(
		    host = 'localhost',
		    port = 3306,
		    user = sql_user,
		    passwd = sql_psd,
		    db = db_name,
		    charset = 'utf8'
		)
	cur  =  con.cur()

	# 更新数据
	cur.execute("DROP TABLE IF EXISTS todayinfo")
	sql  =  """CREATE TABLE todayinfo (
		id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
		code text,
		name text,
		changepercent double,
		trade double,
		open double,
		high double,
		low double,
		settlement double,
		volume double,
		turnoverratio double,
		amount double,
		per double,
		pb double,
		mktcap double,
		nmc double
	)"""
	cur.execute(sql)

	for d in data:
		 #插入数据
		sql  =  "INSERT INTO todayinfo (code,name,changepercent,trade,open,high,low,settlement,volume,turnoverratio,amount,per,pb,mktcap,nmc) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		data  =  ( d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7],d[8],d[9],d[10],d[11],d[12],d[13],d[14] )
		cur.execute(sql,data)
		con.commit()

	cur.close()
	con.close()

if __name__ == '__main__':
	getDateLine()
	getTodayInfo()
	getUserInfo()
