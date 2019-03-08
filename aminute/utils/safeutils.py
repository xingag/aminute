# encoding: utf-8

from urllib.parse import urlparse, urljoin
from flask import request


def is_safe_url(target):
	"""
	判断地址是否合法
	:param target:
	:return:
	"""
	ref_url = urlparse(request.host_url)
	test_url = urlparse(urljoin(request.host_url, target))

	# ref_url: ParseResult(scheme='http', netloc='127.0.0.1:9000', path='/', params='', query='', fragment='')
	# test_url: ParseResult(scheme='http', netloc='127.0.0.1:9000', path='/signin/', params='', query='', fragment='')

	# 域名一致
	return test_url.scheme in ('http', 'https') and \
		   ref_url.netloc == test_url.netloc
