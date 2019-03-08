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
@time: 2018/7/23 15:17 
@description：cms后台
"""

from flask import (
	render_template,
	views,
	Blueprint,
	request,
	session,
	redirect,
	url_for
)
from .forms import LoginForm, UpdateBannerForm, AddBannerForm, AddNewsForm, UpdateNewsForm
import config
from .models import CMSUser, CMSPermission
from .decorators import login_required, permission_required
from ..models import BannerModel, NewsModel
from utils.dateutils import *
from exts import db
from utils import restful

bp = Blueprint('cms', __name__, url_prefix='/cms')


# 获取当前时间


@bp.route('/')
@login_required
def index():
	return render_template('cms/cms_index.html')


# 登录【页面】
class LoginView(views.MethodView):

	# get方法
	# message指定一个默认值的目的：message参数可以传，也可以不传，达到get请求与post请求出错的兼容性
	def get(self, message=None):
		return render_template('cms/cms_login.html', message=message)

	def post(self):
		login_form = LoginForm(request.form)
		if login_form.validate():
			email = login_form.email.data
			password = login_form.password.data
			# 如果不选中，cookie在浏览器关闭的时候，自动清除掉
			# 如果选中，cookie保存的时间更久
			remember = login_form.remember.data
			# 1.查询数据库中是否存在
			# 2.验证密码和数据库的密码是否一致
			user = CMSUser.query.filter_by(email=email).first()
			if user and user.check_password(password):
				# 保存登录信息到session中
				session[config.CMS_USER_ID] = user.id
				# 是否选中【记住我】这个checkbox
				if remember:
					# 设置【31天】后过期
					session.permanent = True
				# 重定向到cms首页页面【蓝图name.方法名】
				return redirect(url_for('cms.index'))
			# 邮箱或者密码错误
			else:
				# return u'邮箱或者密码错误'
				return self.get(message=u'邮箱或者密码错误')
		else:
			message = login_form.get_error()
			return self.get(message=message)


# 轮播图管理
@bp.route('/banners/')
@login_required
def banners():
	banners_data = BannerModel.query.order_by(BannerModel.create_time.desc()).all()
	return render_template('cms/cms_banners.html', banners=banners_data, current_date=curDate())


# 新闻- 主页面
@bp.route('/news/')
@login_required
def news():
	news_data = NewsModel.query.order_by(NewsModel.create_time.desc()).all()
	return render_template('cms/cms_news.html', news=news_data, current_date=curDate())


# 增加一个Banner【只容许post请求】【新增】
@bp.route('/add_banner/', methods=['POST'])
@login_required
def add_banner():
	form = AddBannerForm(request.form)
	print(form)
	if form.validate():
		image = form.image.data
		current_date = form.current_date.data
		# 保存到数据库当中
		banner = BannerModel(image_url=image, current_date=current_date)
		db.session.add(banner)
		db.session.commit()
		return restful.success()
	else:
		return restful.params_error(form.get_error())


# 新闻【Add】
@bp.route('/add_news/', methods=['POST'])
@login_required
def add_news():
	form = AddNewsForm(request.form)
	print(form)
	if form.validate():
		title = form.title.data
		content = form.content.data
		current_date = form.current_date.data
		image_url = form.image.data
		link_url = form.link.data
		# 保存到数据库
		new = NewsModel(title=title, content=content, img=image_url, link=link_url, current_date=current_date)
		db.session.add(new)
		db.session.commit()
		return restful.success()
	else:
		return restful.params_error(form.get_error())


# 删除一个banner【删除】
@bp.route('/delete_banner/', methods=['POST'])
@login_required
def delete_banner():
	banner_id = request.form.get('banner_id')
	if not banner_id:
		return restful.params_error(message='请传入轮播图id')

	# 如果存在，就去查询数据库
	banner = BannerModel.query.get(banner_id)
	if not banner:
		return restful.params_error(message='没有这个轮播图')

	# 从数据库中删除掉
	db.session.delete(banner)
	db.session.commit()

	# 显示删除成功的对话框
	return restful.success()


@bp.route('/delete_news/', methods=['POST'])
@login_required
def delete_news():
	# 注意：只有一个参数，不需要判断
	news_id = request.form.get('news_id')
	if not news_id:
		return restful.params_error(message='请传入新闻id')

	news = NewsModel.query.get(news_id)
	if not news:
		return restful.params_error(message='没有这条新闻')

	db.session.delete(news)
	db.session.commit()

	return restful.success()


# 修改一个Banner【更新】
@bp.route('/update_banner/', methods=['POST'])
@login_required
def update_banner():
	form = UpdateBannerForm(request.form)
	if form.validate():

		# 表单提交上来的数据
		banner_id = form.banner_id.data
		image = form.image.data
		current_date = form.current_date.data

		# 通过id去查询数据库
		banner = BannerModel.query.get(banner_id)

		# 如果数据库存在这条记录，就更新数据
		if banner:
			banner.image_url = image
			banner.current_date = current_date
			db.session.commit()
			return restful.success()
		else:
			return restful.params_error(message='没有这个轮播图')
	else:
		return restful.params_error(message=form.get_error())


# 新闻【Update】
@bp.route('/update_news/', methods=['POST'])
@login_required
def update_news():
	form = UpdateNewsForm(request.form)
	if form.validate():
		title = form.title.data
		content = form.content.data
		current_date = form.current_date.data
		image_url = form.image.data
		link_url = form.link.data
		news_id = form.new_id.data

		# 查询数据库
		news = NewsModel.query.get(news_id)
		if news:
			news.title = title
			news.content = content
			news.img = image_url
			news.link = link_url
			news.current_date = current_date
			db.session.commit()
			return restful.success()
		else:
			return restful.params_error(message='没有这条新闻')
	else:
		return restful.params_error(message=form.get_error())


bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
