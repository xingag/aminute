#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: restfultools.py 
@time: 2018/7/26 10:18 
@description：数据封装工具类
"""

from flask import jsonify

#  define status_dics here
R200_OK = {'code': 200, 'message': 'OK'}
R201_CREATED = {'code': 201, 'message': 'CREATED'}
R204_NOCONTENT = {'code': 204, 'message': 'All deleted'}
R400_BADREQUEST = {'code': 400, 'message': 'Bad request'}
R403_FORBIDDEN = {'code': 403, 'message': 'Forbidden'}
R404_NOTFOUND = {'code': 404, 'message': 'Not found'}


# 返回全部的数据
# 当需要获取资源的时候，我们返回一个data对应一个数组，同时返回状态信息
def fullResponse(statu_dic, data):
	return jsonify({'status': statu_dic, 'data': data})


# 仅仅包含状态信息的响应
def statusResponse(statu_dic):
	return jsonify({'status': statu_dic})
