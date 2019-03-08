#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: hooks.py
@time: 2018/5/13 14:10
@description：cms后台-钩子函数
"""

from .views import bp
import config
from flask import session, g
from .models import CMSUser, CMSPermission


# 钩子函数
# 作用：如果已经登录，就保存用户信息到g对象中
# 任何请求之前都会调用的函数
@bp.before_request
def before_request():
	if config.CMS_USER_ID in session:
		user_id = session.get(config.CMS_USER_ID)
		user = CMSUser.query.get(user_id)
		if user:
			# 放入到g变量中后，前台html可以直接通过g拿到数据
			g.cms_user = user


# 凡是bp这个蓝图的模板，返回的数据都会添加到上下文中，这样，模板都可以来访问
# 可以向模板上下文中自动注入变量，在模板中调用：返回值必须是一个dict【return dict(user=g.user)】
@bp.context_processor
def cms_context_processor():
	return {'CMSPermission': CMSPermission}

# =========================================================================================
# 注意：默认只有views.py下面的钩子函数会被执行，hooks.py下面的钩子函数不会被执行
# 所以需要在__init__.py里面导入hook.py文件【zlbbs.py中引用的蓝图，会调用在__init__.py中导入的类】
