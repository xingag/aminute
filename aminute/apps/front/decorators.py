#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: decorators.py 
@time: 2018/5/11 0:06 
@description：前台所有装饰器
"""

from flask import session, redirect, url_for, g

from functools import wraps

import config


# 登录的装饰器
# 应用场景：必须登录，才能执行对应的修饰函数
def login_required(func):
	"""
	:param func: 待执行的函数
	:return:
	"""

	# 使用泛型参数：代表任意参数
	@wraps(func)
	def inner(*args, **kwargs):
		if config.FRONT_USER_ID in session:
			return func(*args, **kwargs)
		else:
			return redirect(url_for('front.signin'))

	return inner
