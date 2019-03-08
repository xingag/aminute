#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: zlcache.py 
@time: 2018/5/17 22:40 
@description：缓存数据工具类
"""

import memcache

# 确定memcache服务已经启动
# 本地
cache = memcache.Client(['127.0.0.1:11211'], debug=True)


def set(key, value, timeout=60):
	"""
	往memcached里面设置数据
	:param key: 键
	:param value: 值
	:param timeout: 超时时间，默认是60秒
	:return:
	"""
	# 此处添加其他代码【自己的代码】
	return cache.set(key, value, timeout)


def get(key):
	return cache.get(key)


def delete(key):
	return cache.delete(key)
