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
@time: 2018/8/28 15:04 
@description：对Requests的封装
@desc2:网络请求同步用 requests;异步用 aiohttp
@link：https://github.com/zzzzer91/myrequests
"""

from .api import request, get, head, post, patch, put, delete, options
from .sessions import Session
from .log import logger
