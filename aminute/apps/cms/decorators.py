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
@description：cms后台所有装饰器
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
		if config.CMS_USER_ID in session:
			return func(*args, **kwargs)
		else:
			return redirect(url_for('cms.login'))

	return inner


# 权限的装饰器【能接受参数的装饰器-相当于2层的装饰器】
# 必须有对应的装饰器，才能访问对应的页面
def permission_required(permission):
	# 里面的函数才是真正的装饰器
	def outter(func):
		@wraps(func)
		def inner(*args, **kwargs):
			user = g.cms_user
			if user.has_permission(permission):
				return func(*args, **kwargs)
			else:
				# 没有这个权限，就直接跳转到首页
				return redirect(url_for('cms.index'))

		return inner

	return outter
