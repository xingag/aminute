#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: config.py 
@time: 2018/7/23 14:56 
@description：配置
"""

DEBUG = False

# =====================================================================================
# Mysql配置文件
USERNAME = 'root'
PASSWORD = 'Hu881025@'
HOSTNAME = "127.0.0.1"
PORT = '3306'
DATABASE = 'aminute'

DIALECT = 'mysql'
DRIVER = 'pymysql'

# 1.组成一个连接数据的一个固定格式的字符串
# dialect+driver://username:password@host:port/database
DB_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

# 注意：【SQLALCHEMY_DATABASE_URI 名字不能写错，不然会创建表失败】
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = False


# 下面可以设置为True，会把图片上传到七牛服务器
UEDITOR_UPLOAD_TO_QINIU = True
UEDITOR_QINIU_ACCESS_KEY = "MXpNm02HDDsgqIYhModZnkNIIpj0oRP4lWOS8yiQ"
UEDITOR_QINIU_SECRET_KEY = "zGznUzAzXirP3fzQB5TCR3hD58gIMPV-ULmEdCA6"
UEDITOR_QINIU_BUCKET_NAME = "flask"
UEDITOR_QINIU_DOMAIN = "http://pbcomlwfv.bkt.clouddn.com"  # 域名

# =======================================================================================
CMS_USER_ID = 'DAGAYHNGEBLGEWGL'
FRONT_USER_ID = 'xsdfsdgdsagsadga'

#======================================================

PER_PAGE = 10  # 每一页的数据
