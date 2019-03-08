import os
import time

from requests import Session as _Session
from requests.models import Request
from requests.exceptions import Timeout, HTTPError, ConnectionError, ChunkedEncodingError

from .log import logger

TRY_COUNT = 4  # 请求失败后, 尝试次数


class Session(_Session):

	def request(self, method, url,
				params=None,
				data=None,
				headers=None,
				cookies=None,
				files=None,
				auth=None,
				timeout=5,
				allow_redirects=True,
				proxies=None,
				hooks=None,
				stream=None,
				verify=None,
				cert=None,
				json=None):

		req = Request(
			method=method.upper(),
			url=url,
			headers=headers,
			files=files,
			data=data or {},
			json=json,
			params=params or {},
			auth=auth,
			cookies=cookies,
			hooks=hooks,
		)
		prep = self.prepare_request(req)

		proxies = proxies or {}

		settings = self.merge_environment_settings(
			prep.url, proxies, stream, verify, cert
		)

		send_kwargs = {
			'timeout': timeout,
			'allow_redirects': allow_redirects,
		}
		send_kwargs.update(settings)

		message = '%s: %s' % (method, prep.url)
		logger.info(message)
		for i in range(TRY_COUNT + 1):
			try:
				r = self.send(prep, **send_kwargs)
				r.raise_for_status()
				return r
			except Timeout:
				why = 'Timeout'
			except ConnectionError:
				why = 'ConnectionError'
			except HTTPError:
				why = '%s' % r.status_code
			except ChunkedEncodingError:  # 读到的字节数与实际字节数不符
				why = 'ChunkedEncodingError'
			if i != TRY_COUNT:
				logger.warning('%s, %s, retry %d >>> %s' % (os.getpid(), why, i + 1, message))
				time.sleep(3)
		logger.error('[%s] %s' % (why, message))
