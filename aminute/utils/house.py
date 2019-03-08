#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: house.py 
@time: 2018/8/28 17:02 
@description：爬取房产信息
@extra:pip install lxml
"""

import requests
from bs4 import BeautifulSoup

current_host = 'http://news.szhome.com/tags/278.html'
week_host = 'http://cfj.szhome.com/'

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
}


def getLastDayHouseMsg():
	"""
	获取昨天的房产交易信息
	:return:
	"""
	response = requests.get(url=current_host, headers=headers).text
	soup = BeautifulSoup(response, 'lxml')

	# 获取第一条房产信息作为最新的房产价格
	house_raw = soup.select('.l-content .fix .title')

	if not house_raw or len(house_raw) == 0:
		return None

	# 开始解析房价数据
	house_price = house_raw[0].string

	dateIndex = house_price.find('日')
	# 截取出日期
	date = house_price[0:(dateIndex + 1)]

	numIndex_p = house_price.find('成交')
	numIndex_e = house_price.find('套')
	num = house_price[numIndex_p + 2:numIndex_e]

	price_p = house_price.find('均价')
	price_e = house_price.find('元')
	price = house_price[price_p + 2:price_e]

	# print("今天：{}\t成交：{}\t均价：{}".format(date, num, price))

	return date, price, num


def getWeekHouseMsg():
	"""
	获取一周的房产信息
	:return:
	"""
	response = requests.get(url=week_host, headers=headers).text
	soup = BeautifulSoup(response, 'lxml')
	house_raw = soup.select('div[class=xfjj]')
	# 二手房均价
	second_hand_price = house_raw[0].select('.f36')[0].string
	# 二手房成交数目
	second_hand_num = house_raw[1].select('.f36')[0].string

	# 新手房均价
	new_house_price = house_raw[2].select('.f36')[0].string

	# 新房成交数目
	new_house_num = house_raw[3].select('.f36')[0].string

	# print(second_hand_price, second_hand_num, new_house_price, new_house_num)

	return new_house_price, new_house_num, second_hand_price, second_hand_num
