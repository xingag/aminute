#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: models.py 
@time: 2018/7/23 14:55 
@description：公用的模型
"""

from exts import db
from datetime import datetime
from datetime import date


# 轮播图Model
class BannerModel(db.Model):
	__tablename__ = 'banner'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	image_url = db.Column(db.String(500), nullable=False)

	# 当前时间
	current_date = db.Column(db.Date, default=date.today())

	# 创建时间
	create_time = db.Column(db.DateTime, default=datetime.now)

	# 额外的参数
	extra_arg = db.Column(db.String(500))


# 新闻模型
class NewsModel(db.Model):
	__tablename__ = 'news'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	# 标题
	title = db.Column(db.String(500), nullable=False)
	# 内容
	content = db.Column(db.Text, nullable=False)
	# 图片
	img = db.Column(db.String(500), nullable=False)
	# 跳转链接
	link = db.Column(db.String(500), nullable=False)
	# 新闻时间
	current_date = db.Column(db.Date, default=date.today())
	# 创建时间
	create_time = db.Column(db.DateTime, default=datetime.now)


# 天气模型
class WeatherModel(db.Model):
	__tablename__ = 'weather'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)

	# 天气信息1
	weather = db.Column(db.String(500), nullable=False)

	# 天气信息2
	weather_other = db.Column(db.String(500), nullable=False)

	# 天气时间【当前日期下的天气状况】
	current_date = db.Column(db.Date, default=date.today())

	# 创建时间【当天的天气只能有一个】
	create_time = db.Column(db.DateTime, default=datetime.now)


# 房产信息
class HouseModel(db.Model):
	__tablename__ = 'house'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)

	# 一周新房成交价格
	house_week_new_value = db.Column(db.String(500), nullable=False)
	# 一周二手房成交价格
	house_week_old_value = db.Column(db.String(500), nullable=False)

	# 昨日交易价格
	house_yestoday_trans_price = db.Column(db.String(500), nullable=False)
	# 昨日交易量
	house_yestoday_trans_num = db.Column(db.String(500), nullable=False)

	# 有效时间
	current_date = db.Column(db.String(500), nullable=False)

	# 创建时间【当天的房产信息只能有一个】
	create_time = db.Column(db.DateTime, default=datetime.now)
