#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: models.py 
@time: 2018/7/23 21:32 
@description：TODO
"""

from exts import db
import enum
import shortuuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class GenderEnum(enum.Enum):
	MALE = 1
	FEMALE = 2
	SECRET = 3
	UNKNOW = 4


class FrontUser(db.Model):
	__tablename__ = 'front_user'
	id = db.Column(db.String(100), primary_key=True, default=shortuuid.uuid)
	telephone = db.Column(db.String(11), nullable=False, unique=True)
	username = db.Column(db.String(50), nullable=False)
	_password = db.Column(db.String(100), nullable=False)
	email = db.Column(db.String(50), unique=True)
	realname = db.Column(db.String(50))
	avatar = db.Column(db.String(100))
	signature = db.Column(db.String(100))
	gender = db.Column(db.Enum(GenderEnum), default=GenderEnum.UNKNOW)
	join_time = db.Column(db.DateTime, default=datetime.now)

	def __init__(self, *args, **kwargs):
		if "password" in kwargs:
			self.password = kwargs.get('password');
			kwargs.pop('password')
		super(FrontUser, self).__init__(*args, **kwargs)

	@property
	def password(self):
		return self._password

	@password.setter
	def password(self, new_password):
		self._password = generate_password_hash(new_password)

	# 检查密码的合法性
	def check_password(self, raw_password):
		result = check_password_hash(self.password, raw_password)
		return result
