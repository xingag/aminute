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
@time: 2018/8/21 16:04 
@description：TODO
"""

from wtforms import StringField, IntegerField, DateField, TextAreaField
from wtforms.validators import Email, InputRequired, Length, EqualTo
from apps.forms import BaseForm
from wtforms import validators
from utils import zlcache
from wtforms import ValidationError
from flask import g


# 登录表单的验证
class LoginForm(BaseForm):
	email = StringField(validators=[Email(message='请输入正确的邮箱格式'), InputRequired(message='请输入邮箱')])
	password = StringField(validators=[Length(6, 20, message='请输入正确格式的密码')])
	# 记住我，可以选，可以不选。所以，不需要设置验证器
	remember = IntegerField()


# 新增轮播图的表单验证
class AddBannerForm(BaseForm):
	image = StringField(validators=[InputRequired(message='请输入轮播图图片')])
	current_date = DateField(validators=[InputRequired(message='请选择日期')])

	def __repr__(self):
		return "<AddBannerForm(image_url:%s,current_date:%s)>" % (
			self.image, self.current_date)


# 新增新闻
class AddNewsForm(BaseForm):
	title = StringField(validators=[InputRequired(message='请输入新闻标题')])
	# 此处需要获取TextAre里面的值
	content = TextAreaField(u'新闻内容', [validators.optional(), validators.length(max=1000)])
	# contentInput = StringField(validators=[InputRequired(message='请输入新闻内容')])

	image = StringField()
	link = StringField()
	current_date = DateField(validators=[InputRequired(message='请选择日期')])


# 修改轮播图的表单验证
class UpdateBannerForm(AddBannerForm):
	banner_id = IntegerField(validators=[InputRequired(message='请输入轮播图的id')])


# 修改新闻
class UpdateNewsForm(AddNewsForm):
	new_id = IntegerField(validators=[InputRequired(message='请输入新闻的id')])
