#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: manage.py 
@time: 2018/7/23 21:41 
@description：TODO
"""

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from apps.models import *
from apps.cms import models as cms_models
from apps.front import models as front_models

from aminute import create_app
from exts import db

FrontUser = front_models.FrontUser
CMSUser = cms_models.CMSUser
CMSRole = cms_models.CMSRole
CMSPermission = cms_models.CMSPermission

app = create_app()
manager = Manager(app)
Migrate(app, db)
manager.add_command("db", MigrateCommand)


# Add A FrontUser
@manager.option('-t', '--telephone', dest='telephone')
@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
def create_front_user(telephone, username, password):
	user = FrontUser(telephone=telephone, username=username, password=password)
	db.session.add(user)
	db.session.commit()


# 5.新增的一条create_cms_user的命令【往cms数据表中增加一个用户】
# python manage.py create_cms_user -u zhiliao -p 111111 -e xingag66@gmail.com
# python manage.py create_cms_user -u zhiliao -p 111111 -e xinganguo@gmail.com
# 注意：首先往cms系统中添加一个用户【必要】
@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--email', dest='email')
def create_cms_user(username, password, email):
	user = CMSUser(username=username, password=password, email=email)
	db.session.add(user)
	db.session.commit()
	print('cms 用户添加成功')

# 增加某个用户到某个角色当中【python manage.py add_user_to_role -e xinganguo@gmail.com -n 访问者】
# 测试：python manage.py test_permission
@manager.option('-e', '--email', dest='email')
@manager.option('-n', '--name', dest='name')
def add_user_to_role(email, name):
	user = CMSUser.query.filter_by(email=email).first()
	if user:
		role = CMSRole.query.filter_by(name=name).first()
		if role:
			# 将这个用户添加到角色当中
			role.users.append(user)
			db.session.commit()
			print('用户:%s添加在角色:%s中成功' % (email, name))
		else:
			print('此角色不存在:%s' % user)
	else:
		print('此用户不存在:%s' % email)

# 使用一条命令，往CMSRole表内增加4个角色【python manage.py create_role】
# 使用manager.command装饰器添加一个命名
# 新增一条【创建一个角色】的命令
# 新建角色model之后，就要创建一个命令
@manager.command
def create_role():
	# 开始定义角色
	# 1.访问角色
	visitor = CMSRole(name='访问者', desc='只能访问相关数据，不能修改数据')
	visitor.permission = CMSPermission.VISITOR

	# 2.运营者角色
	# 修改个人信息、管理帖子、管理评论、管理前台用户
	operator = CMSRole(name='运营', desc='管理帖子、管理评论、管理前台用户')
	# 多个权限用【| 运算】来操作
	# 含有的权限：访问者、管理帖子、前台用户、评论
	operator.permission = CMSPermission.VISITOR | CMSPermission.POSTER | CMSPermission.FRONTUSER | CMSPermission.COMMENTER | CMSPermission.CMSUser

	# 3.管理员
	# 拥有绝大部分的权限
	administrator = CMSRole(name='管理员', desc='拥有本系统所有权限')
	administrator.permission = CMSPermission.VISITOR | CMSPermission.POSTER | CMSPermission.FRONTUSER | CMSPermission.COMMENTER | CMSPermission.CMSUser | CMSPermission.BOARDER

	# 4.开发者
	# 拥有最高的权限
	developer = CMSRole(name='开发者', desc='开发人员专用角色')
	developer.permission = CMSPermission.ALL_PERMISSION

	db.session.add_all([visitor, operator, administrator, developer])
	db.session.commit()


if __name__ == '__main__':
	manager.run()
