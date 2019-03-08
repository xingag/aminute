#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: exts.py 
@time: 2018/5/3 22:56 
@description：SQLAlchemy/Mail的配置
"""

from flask_sqlalchemy import SQLAlchemy

# 下面的初始化方式，需要在主py文件中，单独加入app【db.init_app(app)】
db = SQLAlchemy()

