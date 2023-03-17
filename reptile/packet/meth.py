# -*- encoding: utf-8 -*-
'''
@File    :   meth.py
@Time    :   2023/02/05 20:51:30
@Author  :   UnAbuse 
'''

from requests import Session
from random import randint

class Meth:
	def __init__(self, proxy_list: list=None, size: int=None) -> None:
		# 定义代理ip的列表
		self.proxy_list = None
		if proxy_list is None:
			self.proxy_list = []
		else:
			self.proxy_list = proxy_list
		# 定义iter_content每次获取的大小
		if size is None:
			self.size = 1048576
		else:
			self.size = size
		self.session = Session()
		self.methods = {
			'GET': self.session.get,
			'POST': self.session.post,
		}

	def get_ip(self, filename:str):
		'''
		filename: 装着代理数据的文件, 需要带后缀
		'''
		# 从文件中读取代理ip
		with open(filename, 'r+', encoding='utf-8') as file_data:
			data = file_data.readlines()
			self.proxy_list = list(map(lambda x: x.strip('\n'), data))

	def get_Html(self, url: str, methods: str, res: str, headers: dict=None, encoding: str=None, params: dict=None, stream: bool=False):
		'''
		url: 访问的链接;
		methods: 访问方法, GET、POST;
		res: 结果返回形式, TEXT、JSON、CONTENT、TCONTENT;
		headers: 请求头;
		params: 附带数据;
		'''
		# 判断是否加载代理
		if self.proxy_list == []:
			proxy = None
		else:
			proxy = eval(self.proxy_list[randint(0, len(self.proxy_list)-1)])
		# 获取text,json格式
		if params:
			params = params
		else:
			params = None
		info = {
			'GET': {
			'url': url,
			'headers': headers,
			'params': params,
			'proxies': proxy,
			'stream': stream
			},
			'POST': {
			'url': url,
			'headers': headers,
			'data': params,
			'proxies': proxy
			}
		}
		data = self.methods[methods](**info[methods])
		data.encoding = encoding
		self.cookies = data.cookies
		if res == 'TEXT':
			return data.text
		elif res == 'JSON':
			return data.json()
		elif res == 'CONTENT':
			return data.content
		elif res == 'TCONTENT':
			return data.iter_content(chunk_size=self.size)
