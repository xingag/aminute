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
@time: 2018/7/24 20:53 
@description：TODO
"""

from ..forms import BaseForm

from wtforms import StringField, ValidationError, IntegerField

from wtforms.validators import Regexp, EqualTo, InputRequired


class SignupForm(BaseForm):
	telephone = StringField(validators=[Regexp(r"1[345789]\d{9}", message="请输入正确格式的手机号码")])
	username = StringField(validators=[Regexp(r".{2,20}", message="请输入正确格式的用户名")])
	password1 = StringField(validators=[Regexp(r"[0-9a-zA-Z_\.]{6,20}", message="请输入正确格式的密码")])
	password2 = StringField(validators=[EqualTo("password1", message="两次输入的密码不一致")])


class SigninForm(BaseForm):
	telephone = StringField(validators=[Regexp(r"1[345789]\d{9}", message="请输入正确格式的手机号码")])
	password = StringField(validators=[Regexp(r"[0-9a-zA-Z_\.]{6,20}", message="请输入正确格式的密码")])
	# 记住我这个input不需要验证
	remember = StringField()
