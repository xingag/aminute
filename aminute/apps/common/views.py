#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: views.py 
@time: 2018/7/23 21:20 
@description：TODO
"""
import qiniu
from flask import (
	Blueprint,
	jsonify
)

bp = Blueprint('common', __name__, url_prefix='/c')


# 获取七牛云的uptoken【通过AK和SK】，并以json的格式返回
@bp.route('/uptoken/')
def uptoken():
	AccessKey = "MXpNm02HDDsgqIYhModZnkNIIpj0oRP4lWOS8yiQ"
	SecretKey = "zGznUzAzXirP3fzQB5TCR3hD58gIMPV-ULmEdCA6"
	q = qiniu.Auth(AccessKey, SecretKey)

	# 参数：仓库名
	bucket = "flask"
	token = q.upload_token(bucket)

	print(token)

	# 返回给前端JSON格式的数据【注意：键值必须是uptoken，否则使用七牛云的JS SDK就获取不成功了】
	return jsonify({'uptoken': token})
