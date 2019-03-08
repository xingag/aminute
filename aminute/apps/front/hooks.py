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
@time: 2018/7/23 22:27 
@description：TODO
"""

import config
from flask import session,g,render_template
from .models import FrontUser
from .views import bp


@bp.before_request
def before_request():
	if config.FRONT_USER_ID in session:
		user_id = session.get(config.FRONT_USER_ID)
		user = FrontUser.query.get(user_id)
		if user:
			# 放入到g变量中后，前台html可以直接通过g拿到数据
			g.front_user = user


@bp.errorhandler
def page_not_found():
	return render_template('front/front_404.html'), 404