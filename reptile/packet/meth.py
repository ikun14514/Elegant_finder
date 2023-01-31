import requests
from random import randint

'''
作者：UnAbuse
githud地址：https://github.com/UnAbuse
转载请注明出处
'''

class Meth:
	def __init__(self, proxy_list=None):
		# 定义代理ip的列表
		self.proxy_list = None
		match self.proxy_list:
			case None:
				self.proxy_list = []
			case _:
				self.proxy_list = proxy_list
		self.session = requests.Session()

	def get_ip(self, filename):
		# 从文件中读取代理ip
		with open(filename, 'r+', encoding='utf-8') as file_data:
			data = file_data.readlines()
			self.proxy_list = list(map(lambda x: x.strip('\n'), data))

	def get_Html(self, url, methods, res, headers, encoding, params=None):
		# 判断是否使用本地代理外的代理
		match len(self.proxy_list):
			case 0:
				proxy = None
			case _:
				proxy = eval(self.proxy_list[randint(0, len(self.proxy_list)-1)])
		# 获取text,json格式
		if params:
			match methods:
				case 'GET':
					data = self.session.get(url=url, headers=headers, params=params, proxies=proxy)
				case 'POST':
					data = self.session.post(url=url, headers=headers, data=params, proxies=proxy)
				case 'TGET':
					data = self.session.get(url=url, headers=headers, params=params, proxies=proxy, stream=True)
		else:
			match methods:
				case 'GET':
					data = self.session.get(url=url, headers=headers, proxies=proxy)
				case 'POST':
					data = self.session.post(url=url, headers=headers, proxies=proxy)
				case 'TGET':
					data = self.session.get(url=url, headers=headers, proxies=proxy, stream=True)
		data.encoding = encoding
		match res:
			case 'text':
				return data.text
			case 'json':
				return data.json()
			case 'img':
				return data.content
			case 'timg':
				return data.iter_content(chunk_size=104857600)
