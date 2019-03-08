#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: restful.py 
@time: 2018/5/16 21:38 
@description：返回一个restful的数据的工具类
"""

from flask import jsonify


class HttpCode(object):
	# 常用的4中状态码
	ok = 200
	un_auth_error = 401
	params_error = 400
	server_error = 500


# restful 格式化数据
def restful_result(code, message, data):
	# 注意：针对data数据，如果没有传入任何值，就显示一个空字典{}，便于管理
	return jsonify({"code": code, "message": message, "data": data or {}})


# 请求成功
def success(message="", data=None):
	return restful_result(code=HttpCode.ok, message=message, data=data)


# 未授权的错误
def un_auth_error(message=""):
	return restful_result(code=HttpCode.un_auth_error, message=message, data=None)


# 参数错误
def params_error(message=""):
	return restful_result(code=HttpCode.params_error, message=message, data=None)


# 服务器错误
def server_error(message=""):
	return restful_result(code=HttpCode.server_error, message=message or '服务器内部错误', data=None)
