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
@time: 2018/5/3 22:31
@description：cms后台中的模型
"""

from exts import db
from datetime import datetime

# flask中加密的算法
# 【生成密码、检测密码】
from werkzeug.security import generate_password_hash, check_password_hash


# 权限类
class CMSPermission(object):
	# 255二进制的方式来表示：1111 1111
	# 0.所有权限
	ALL_PERMISSION = 0b11111111
	# 1.访问权限
	VISITOR = 0b00000001
	# 2.管理帖子的权限
	POSTER = 0b00000010
	# 3.管理评论的权限
	COMMENTER = 0b00000100
	# 4.管理板块的权限
	BOARDER = 0b00001000
	# 5.管理前台用户的权限
	FRONTUSER = 0b00010000
	# 6.管理后台用户的权限
	CMSUser = 0b00100000
	# 7.管理【后台管理员】的权限
	ADMINER = 0b01000000


# 【多对多：用户和角色之间的中间表】
cms_role_user = db.Table(
	'cms_role_user',
	db.Column('cms_user_id', db.Integer, db.ForeignKey('cms_user.id'), primary_key=True),
	db.Column('cms_role_id', db.Integer, db.ForeignKey('cms_role.id'), primary_key=True)
)


class CMSUser(db.Model):
	__tablename__ = "cms_user"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(50), nullable=False)
	# _开头的属性代表是私有的，不希望直接就能被访问到
	_password = db.Column(db.String(100), nullable=False)
	# email 在数据库中保证唯一性
	email = db.Column(db.String(50), nullable=False, unique=True)
	join_time = db.Column(db.DateTime, default=datetime.now)

	# ---------------------------------------------------------------------------

	# 重写构造函数
	def __init__(self, username, password, email):
		self.username = username
		# 由于没有_password属性
		# 相当于执行的set函数
		self.password = password
		self.email = email

	# python 中的属性方法【property】
	# @property广泛应用在类的定义中，可以让调用者写出简短的代码，同时保证对参数进行必要的检查，这样，程序运行时就减少了出错的可能性。
	# Python内置的 @property装饰器就是负责把一个方法变成属性调用的：
	# 实现了：
	# 对外，cms_user.password可以拿到；
	# 对内，cms_user._password可以拿到
	# 相当于【get函数】
	@property
	def password(self):
		return self._password

	# @property本身又创建了另一个装饰器 @score.setter，负责把一个setter方法变成属性赋值，于是，我们就拥有一个可控的属性操作
	# 相当于【set函数】
	# 可以通过cms_user.password = 'xxx' 设置密码
	@password.setter
	def password(self, raw_password):
		# 加密后进行保存
		self._password = generate_password_hash(raw_password)

	# 检查密码的函数
	def check_password(self, raw_password):
		# 检查原始密码使用hash算法加密后，与数据库中保存的密码进行比较，看是否一致
		result = check_password_hash(self.password, raw_password)
		return result

	# 获取用户拥有的所有权限【通过所拥有的角色，来遍历权限，然后进行二进制 |操作】
	# 属性：不会添加到数据库当中
	@property
	def permissions(self):
		# 没有任何权限
		if not self.roles:
			return 0
		# 所有的权限
		all_permission = 0
		for role in self.roles:
			permission = role.permission
			all_permission |= permission
		return all_permission

	# 是否拥有某个权限
	# 注意：判断某个用户是否有某个权限，用这个权限与自己拥有的所有权限做【&操作】。结果等于这个权限就是拥有，否则就是不拥有这个权限。
	def has_permission(self, permission):
		return (permission & self.permissions) == permission

	# 判断是否是开发者【最高权限者】
	# 属性：不会添加到数据库当中
	@property
	def is_developer(self):
		return self.has_permission(CMSPermission.ALL_PERMISSION)


# 角色模型【一个用户有多种角色，一种角色可能对应多个用户】【一种角色只能有一个权限】
class CMSRole(db.Model):
	__tablename__ = 'cms_role'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(50), nullable=False)
	desc = db.Column(db.String(200), nullable=True)
	create_time = db.Column(db.DateTime, default=datetime.now)
	# 角色所拥有的权限，默认是浏览者的权限
	permission = db.Column(db.Integer, default=CMSPermission.VISITOR)

	# 和中间表cms_role_user建立联系
	# Role表和User表之间的关系：User可以通过roles获取到角色信息；角色可以通过users获取到用户信息
	users = db.relationship('CMSUser', secondary=cms_role_user, backref='roles')

# ====================================================================================
# 密码的安全性
# 1.对外的字段名叫password，对内的字段名叫做_password
# 2.CMSUser类重写了构造函数__init__()函数，并使用property关键字定义了属性变量：password，并设置了get和set方法
# 3.定义了检查密码是否正确的check_password()函数
