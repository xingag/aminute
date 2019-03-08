#coding:utf-8
from flask import Flask

from apps.cms import bp as cms_bp
from apps.front import bp as front_bp
from apps.common import bp as common_bp
from apps.api import bp as api_bp

import config

from exts import db
from flask_wtf import CSRFProtect

app = Flask(__name__)  # type:Flask


def create_app():
	app.config.from_object(config)
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.config['SECRET_KEY'] = "xxxxxxxxxxgdsagffdgffgsgfagad"

	app.register_blueprint(cms_bp)
	app.register_blueprint(front_bp)
	app.register_blueprint(common_bp)
	app.register_blueprint(api_bp)

	db.init_app(app)

	CSRFProtect(app)

	return app


# 自定义过滤器：格式化日期
# 注意：过滤器只能在app中定义，不能在蓝图中定义
@app.template_filter('getDate')
def getDate(value):
	temp = [str(value.year), str(value.month), str(value.day)]
	return "-".join(temp)

# 下面这句是便于wsigi服务器调用到app
app = create_app()

if __name__ == '__main__':
	create_app()
	app.run(port=9000,host='0.0.0.0')
