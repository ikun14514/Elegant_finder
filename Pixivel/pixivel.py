# -*- encoding: utf-8 -*-
'''
@File    :   Pixivel.py
@Time    :   2023/02/05 20:53:55
@Author  :   UnAbuse 
'''

from requests import Session
from threading import Thread
from time import ctime
import gc, re, argparse, os

class Logging:
	def logging(self, func):
		def wapper(*args, **kwargs):
			if not os.path.exists(f'{os.getcwd()}/log'):
				os.makedirs(f'{os.getcwd()}/log')
			with open(f'{os.getcwd()}/log/{func.__name__}.log', 'a+') as f:
				f.write(f'[{ctime()}] {args} {kwargs}\n')
			return func(*args, **kwargs)
		return wapper

class Pixivel:
	logging = Logging().logging

	def __init__(self) -> None:
		gc.isenabled = True
		self.headers = {
			'Accept' :'application/json, text/plain, */*',
			'Referer': 'https://pixivel.moe/',
			'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33'
		}
		self.api_id = 'https://api.pixivel.moe/v2/pixiv/illust/search/'
		self.api_list = 'https://api.pixivel.moe/v2/pixiv/illust/'
		self.api_img = ['https://proxy.pixivel.moe/img-master/img/', '_p0_master1200.jpg']
		self.session = Session()
		if not os.path.exists('./image'):
			os.makedirs('./image')
		

	@logging
	def _download(self, pid: str, url: str) -> int:
		try:
			data = self.session.request(method='GET', url=url, headers=self.headers).content
			with open(f'{os.getcwd()}/image/{pid}.jpg', "x"): pass
			with open(f'{os.getcwd()}/image/{pid}.jpg', "wb") as f:
				f.write(data)
				print(f'[{ctime()}] {pid} has been downloaded...')
			return 1
		except Exception as e:
			print(f"[{ctime()}] {e}")
			return 0

	@logging
	def _thread(self, pid: str, url: str) -> Thread:
		t = Thread(target=self._download, args=(pid, url))
		t.start()
		return t

	@logging
	def _run(self, name: str, page: int) -> int:
		try:
			list_id = self.session.request(method='GET', url=''.join((self.api_id, name)),
				headers=self.headers,
				data={
					'page': str(page),
					'sortpop': 'true',
					'sortdate': 'false'
				}).json()
			id_list = list(map(
				lambda x: x['id'],
				list_id['data']['illusts']
				))
			res = list(map(
				lambda x: self.session.request(
				method='GET', url=''.join((self.api_list, str(x))),
				headers=self.headers).json()['data']['image'],
				id_list
				))
			cut_time = list(map(
				lambda x: re.findall(r'[0-9]+', x),
				res
				))
			url_list = list(map(
				lambda x, y: ''.join((self.api_img[0],x[0], '/', x[1], '/', x[2], '/', x[3], '/', x[4], '/', x[5], '/', str(y), self.api_img[1])),
				cut_time,
				id_list
				))
			thread_pool = list(map(lambda x, y: self._thread(x, y), id_list, url_list))
			thread_pool[-1].join()
			return 1
		except  Exception as e:
			print(f"[{ctime()}] {e}")
			return 0
	
	@logging
	def run(self, name: str, start: int, end: int=None) -> None:
		if end is None:
			print(f"[{ctime()}] start to download page of {start}...")
			self._run(name, start)
		else:
			for item in range(start, end+1):
				print(f"[{ctime()}] start to download page of {item}...")
				self._run(name, item)
				print(f"[{ctime()}] end to download page of {item}...")

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='downloader for pixivel')
	parser.add_argument('-n', '--name', type=str, required=True,help='searching name of graph')
	parser.add_argument('-s', '--start',type=int, default=0, help='starting page: default is 0')
	parser.add_argument('-e', '--end', type=int, default=None, help='ending page: can ignore')
	args = parser.parse_args()

	Pixivel().run(args.name, args.start, args.end)
