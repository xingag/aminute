#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: views.py 
@time: 2018/7/23 15:21 
@description：前台
"""

from flask import (
	Blueprint,
	render_template,
	url_for,
	views,
	request,
	session,
	g,
	redirect,
	abort
)

from ..models import BannerModel, NewsModel, WeatherModel, HouseModel
from .forms import SignupForm, SigninForm
from .models import FrontUser
from utils import restful, safeutils
import utils.http as requests
from exts import db
from .decorators import login_required
import config
from flask_paginate import Pagination, get_page_parameter
from utils.dateutils import curDateWithFormat, get_week_day, curDate
from datetime import datetime
from utils.house import getLastDayHouseMsg, getWeekHouseMsg

bp = Blueprint('front', __name__, )


def getCurrentWeather():
	"""
	获取当前的天气信息
	:return:
	"""
	# get请求获取天气的数据
	weather_raw = requests.get(url='https://www.sojson.com/open/api/weather/json.shtml?city=深圳').json()
	if not weather_raw or not weather_raw.get('data') or not weather_raw.get('data').get('forecast'):
		return None

	weather_json = weather_raw.get('data').get(
		'forecast')[0]
	# 实时天气
	weather = weather_json.get('type')

	# 最低温度和最高温度
	temp_low = weather_json.get('low').lstrip('低温').strip('.0℃').strip()
	temp_high = weather_json.get('high').lstrip('高温').strip('.0℃').strip()
	# 风
	wind = weather_json.get('fx')

	weather_other = temp_low + " ~ " + temp_high + " ℃," + wind

	weather_db = WeatherModel.query.filter_by(current_date=curDate()).first()

	if weather_db:
		# 更新数据库数据
		print('更新一条天气数据')
		weather_db.weather = weather
		weather_db.weather_other = weather_other
		db.session.commit()
		return weather_db
	else:
		# 插入数据库
		print('新增一条天气数据')
		weather_new = WeatherModel(weather=weather, weather_other=weather_other, current_date=curDate())
		db.session.add(weather_new)
		db.session.commit()
		return weather_new


def getHouseMsg():
	"""
	获取今日房价信息
	:return:
	"""
	current_house_msg = getLastDayHouseMsg()
	week_house_msg = getWeekHouseMsg()
	current_house_date = current_house_msg[0]
	current_house_price = current_house_msg[1]
	current_house_num = current_house_msg[2]

	new_house_price = week_house_msg[0]
	new_house_num = week_house_msg[1]
	second_hand_price = week_house_msg[2]
	second_hand_num = week_house_msg[3]

	# 查询数据库中是否已经存在这条记录
	house_db = HouseModel.query.filter_by(current_date=current_house_date).first()
	if house_db:
		# 更新
		print('更新一条房产信息,日期是%s' % current_house_date)
		house_db.house_week_new_value = new_house_price
		house_db.house_week_old_value = second_hand_price
		house_db.house_yestoday_trans_price = current_house_price
		house_db.house_yestoday_trans_num = current_house_num
		db.session.commit()
		return house_db
	else:
		# 插入
		print('插入一条房产信息,日期是%s' % current_house_date)
		house = HouseModel(house_yestoday_trans_price=current_house_price, house_yestoday_trans_num=current_house_num,
						   house_week_new_value=new_house_price, house_week_old_value=second_hand_price,
						   current_date=current_house_date)
		db.session.add(house)
		db.session.commit()
		return house


@bp.route('/')
def index():
	# 默认是查看所有帖子，sort为2的时候代表只查看今天的新闻
	sort = request.args.get('sort', type=int, default=1)

	# 每一页新闻的开始、结尾索引数
	page = request.args.get(get_page_parameter(), type=int, default=1)
	start_index = (page - 1) * config.PER_PAGE
	end_index = start_index + config.PER_PAGE

	# 所有新闻
	if sort == 1:
		news_obj = NewsModel.query.order_by(NewsModel.create_time.desc())
	else:
		news_obj = NewsModel.query.filter_by(current_date=curDate()).order_by(NewsModel.create_time.desc())

	news_total = news_obj.count()
	news = news_obj.slice(start_index, end_index)

	# 获取当前的天气信息
	# weather = getCurrentWeather()
	weather = WeatherModel(weather="多云转晴", weather_other="北风3级", current_date="2018年8月31日")

	# 获取房价信息
	# house = getHouseMsg()
	house = HouseModel(house_yestoday_trans_price="49000", house_yestoday_trans_num=23,
					   house_week_new_value="55000", house_week_old_value="58000",
					   current_date="2018年8月30日")

	# 轮播图
	banners = BannerModel.query.order_by(BannerModel.create_time.desc()).limit(3)

	# 分页器
	pagination = Pagination(bs_version=3, page=page, total=news_total, outer_window=0, inner_window=2)

	context = {
		'current_sort': sort,
		'current_date': curDateWithFormat(),
		'curWeek': get_week_day(datetime.now()),
		'banners': banners,
		'news': news,
		'weather': weather,
		'house': house,
		'pagination': pagination
	}
	return render_template('front/index.html', **context)


# 注册
class SignupView(views.MethodView):
	def get(self):
		# 获取上一个页面
		return_to = request.referrer
		if return_to and return_to != request.url and safeutils.is_safe_url(return_to):
			return render_template('front/front_signup.html', return_to=return_to)
		else:
			return render_template('front/front_signup.html')

	def post(self):
		form = SignupForm(request.form)
		if form.validate():
			telephone = form.telephone.data
			username = form.username.data
			password = form.password1.data

			front_user = FrontUser(telephone=telephone, username=username, password=password)
			db.session.add(front_user)
			db.session.commit()
			return restful.success()
		else:
			return restful.params_error(form.get_error())


# 登录
class SigninView(views.MethodView):
	def get(self):
		return render_template('front/front_signin.html')

	def post(self):
		form = SigninForm(request.form)
		if form.validate():
			telephone = form.telephone.data
			password = form.password.data
			remember = form.remember.data

			# 查询数据库中是否存在这个用户
			front_user = FrontUser.query.filter_by(telephone=telephone).first()
			if front_user and front_user.check_password(password):
				session[config.FRONT_USER_ID] = front_user.id
				if remember:
					session.permanent = True
				return restful.success()
			else:
				return restful.params_error('手机号或者密码错误')
		else:
			return restful.params_error(message=form.get_error())


@bp.route('/news_detail/<news_id>')
@login_required
def news_detail(news_id):
	news = NewsModel.query.get(news_id)
	if not news:
		abort(404)
	return render_template('front/front_news_detail.html', news=news)


bp.add_url_rule('/signup/', view_func=SignupView.as_view('signup'))
bp.add_url_rule('/signin/', view_func=SigninView.as_view('signin'))
