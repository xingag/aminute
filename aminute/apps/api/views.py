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
@time: 2018/7/24 22:26 
@description：TODO
"""

from flask import (
	Blueprint,
	Response,
	jsonify
)

from flask_restful import Api, Resource, fields, marshal_with, reqparse

from exts import db
from utils.restfultools import *
from ..models import WeatherModel, HouseModel, NewsModel, BannerModel
import json

bp = Blueprint('api', __name__, url_prefix='/api')

api = Api(bp)


@bp.route('/')
def index():
	return 'api页面'


# 获取最新天气的接口 [http://127.0.0.1:9000/api/weather]
class WeatherApi(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		super(WeatherApi, self).__init__()

	def get(self):
		# 查询数据库
		weather = WeatherModel.query.order_by(WeatherModel.create_time.desc()).first()
		if not weather:
			return statusResponse(R404_NOTFOUND)
		result = {"weather": weather.weather, "weather_other": weather.weather_other,
				  "current_date": weather.current_date}
		return fullResponse(R200_OK, result)


# 获取最新的房价
class HouseApi(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		super(HouseApi, self).__init__()

	def get(self):
		# 查询数据库
		house = HouseModel.query.order_by(HouseModel.create_time.desc()).first()
		if not house:
			return statusResponse(R404_NOTFOUND)
		result = {"week_new_value": house.house_week_new_value, "old_value": house.house_week_old_value,
				  "yestoday_trans_price": house.house_yestoday_trans_price,
				  "yestoday_trans_num": house.house_yestoday_trans_num}
		return fullResponse(R200_OK, result)


# 获取最新的5篇文章
class NewsListApi(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		super(NewsListApi, self).__init__()

	def get(self):
		news_data = NewsModel.query.order_by(NewsModel.create_time.desc()).limit(10)
		if not news_data:
			return statusResponse(R404_NOTFOUND)

		result = [{"title": news.title, "content": news.content, "img": news.img, 'current_date': news.current_date,
				   "link": news.link} for news in news_data]
		return fullResponse(R200_OK, result)


# 获取文章的头图
class HeadImgApi(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		super(HeadImgApi, self).__init__()

	def get(self):
		img_data = BannerModel.query.order_by(BannerModel.create_time.desc()).limit(1).first()
		if not img_data:
			return statusResponse(R404_NOTFOUND)

		result = {"img": img_data.image_url}
		return fullResponse(R200_OK, result)


api.add_resource(WeatherApi, '/weather', endpoint='weather')
api.add_resource(HouseApi, '/house', endpoint='house')
api.add_resource(NewsListApi, '/news', endpoint='news')
api.add_resource(HeadImgApi, '/head_img', endpoint='head_img')
