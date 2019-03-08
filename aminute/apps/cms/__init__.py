#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: __init__.py.py 
@time: 2018/7/23 14:53 
@description：TODO
"""

from .views import bp


# 保证hooks下面的钩子函数会被执行
import apps.cms.hooks
