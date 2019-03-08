#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: forms.py 
@time: 2018/7/23 14:54 
@description：公用的表单验证
"""
from wtforms import Form


class BaseForm(Form):

	def get_error(self):
		"""
		:return: 抽象出错误信息
		"""
		message = self.errors.popitem()[1][0]
		return message

	def validate(self):
		return super(BaseForm, self).validate()
