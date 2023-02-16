# -*- encoding: utf-8 -*-
'''
@File    :   BilibiliReptile.py
@Time    :   2023/02/05 20:53:03
@Author  :   UnAbuse 
'''

from packet import *

class Bilibili:
	def __init__(self, vedio_path: str, size: int=None) -> None:
		'''
		1、Cookie的获取通过Cookie.txt来加载
		2、直播与视频的headers不一样, 需要分开使用
		'''
		if not exists('Cookie.txt'): 
			with open('Cookie.txt', 'w', encoding='utf-8') as f: pass
		with open('Cookie.txt', 'r+', encoding='utf-8') as f:
			Cookie = f.read()
		self.vedio_path = vedio_path
		if not exists(vedio_path):
			mkdir(vedio_path)
		self.headers = {
			'origin': 'https://www.bilibili.com/',
			'referer': 'https://www.bilibili.com/',
			'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
			'cookie': Cookie,
			'accept': 'application/json, text/plain, */*'
		}
		self.live_headers = {
			'origin': 'https://live.bilibili.com',
			'referer': 'https://live.bilibili.com/',
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
			'cookie': Cookie,
			'accept': 'application/json, text/plain, */*'
		}
		self.encoding = 'utf-8'
		self.cid_url = 'https://api.bilibili.com/x/web-interface/view'
		self.video_url = 'https://api.bilibili.com/x/player/playurl'
		self.qrcode_url = 'https://passport.bilibili.com/x/passport-login/web/qrcode/generate'
		self.room_id_url = 'https://api.live.bilibili.com/room/v1/Room/get_info'
		self.live_url = 'https://api.live.bilibili.com/room/v1/Room/playUrl'
		self.information_url = 'https://api.bilibili.com/x/space/myinfo'
		self.lock = Lock()
		self.meth = Meth(proxy_list=None, size=size)

	def information(self):
		print(f'[{ctime()}] 开始验证Cookie')
		info = self.meth.get_Html(
			url=self.information_url,
			methods='GET', res='JSON',
			headers=self.headers,
			encoding=self.encoding
			)
		match info['code']:
			case -101:
				print(f'[{ctime()}] 未登录或者Cookie失效')
			case 0:
				print(f"[{ctime()}] {info['data']['name']} ({info['data']['mid']})")
				match info['data']['vip']['status']:
					case 0:
						print(f'[{ctime()}] 未开通大会员')
					case 1:
						print(f'[{ctime()}] 已开通大会员')

	def thread(self, pid, data, met):
		'''
		开启多线程, 但是并未写join(), 考虑到主线程执行到这边一般都差不多
		并且加了锁, 写了也没有必要
		'''
		t = Thread(target=self.download, args=(pid, data, met))
		t.start()
		return t

	def download(self, pid, data, met):
		'''
		下载方法, 加锁保证不会乱序写入
		唯一注意的是ab写入特性
		'''
		self.lock.acquire()
		try:
			with open(f'{self.vedio_path}/{pid}.{met}', "ab") as f:
				f.write(data)
		finally:
			self.lock.release()
			return 1

	def live_run(self, room_id:int, methods: str):
		'''
		room_id: 房间号, 有可能不是真实的;
		methods: 直播录制方式, 目前只支持flv
		'''
		print(f'[{ctime()}] 开始运行')
		data = self.meth.get_Html(
			self.room_id_url,
			'GET',
			'JSON',
			self.live_headers,
			self.encoding,
			{
				'room_id': room_id
			}
			)
		match data['code']:
			case 0:
				match data['data']['live_status']:
					case 0:
						return 'live_status: 0'
					case _:
						print(f"[{ctime()}] 房间真实ID:{data['data']['room_id']}")
						live_streaming = self.meth.get_Html(
							self.live_url,
							'GET',
							'JSON',
							self.live_headers,
							self.encoding,
							{
								'cid': data['data']['room_id'],
								'quality': 4,
								'platform': methods
							}
							)
						match live_streaming['code']:
							case 0:
								url = live_streaming['data']['durl'][0]['url']
								print(f'[{ctime()}] 直播视频流链接：{url}')
								match methods:
									case 'web':
										dat = self.meth.get_Html(
											url,
											'TGET',
											'TCONTENT',
											self.live_headers,
											self.encoding
											)
										print(f'[{ctime()}] 开始录制')
										list(map(lambda x: self.thread(room_id, x, 'flv'), dat))
								return 'code: 0'
							case _:
								return 'code: ' + live_streaming['code']
			case 1:
				return 'code: 1'

	def vedio_run(self, bid: str, tid: str, quality: int) -> str:
		'''
		视频下载
		'''
		print(f'[{ctime()}] 开始运行')
		data = self.meth.get_Html(
			self.cid_url,
			'GET',
			'JSON',
			self.headers,
			self.encoding,
			{
				bid: tid
			}
			)
		match data['code']:
			case 0:
				cid = data['data']['cid']
				print(f"[{ctime()}] 视频CID:{cid}")
				fnval = 1
				fourk = 0
				if quality == 120:
					fnval = 128
					fourk = 1
				url_list = self.meth.get_Html(
					self.video_url,
					'GET',
					'JSON',
					self.headers,
					self.encoding,
					{
						bid: tid,
						'cid': cid,
						'qn': quality,
						'fnval': fnval,
						'fourk': fourk
					}
					)
				match url_list['code']:
					case 0:
						print(f'[{ctime()}] 画质:{quality}')
						print(f"[{ctime()}] 视频链接:{url_list['data']['durl'][0]['url']}")
						print(f"[{ctime()}] 文件大小:{url_list['data']['durl'][0]['size']/(2**20)}M")
						chunk_list = self.cut_size(url_list['data']['durl'][0]['size'])
						t = list(map(lambda x: self.thread_on(url_list['data']['durl'][0]['url'], x[0], x[1], tid), chunk_list))
						t[-1].join()
						list(map(lambda x: self.reader(x[1], tid, f'{quality}.mp4'), chunk_list))
						list(map(lambda x: remove(f'{self.vedio_path}/{tid}/{x[1]}.link'), chunk_list))
						rmdir(f'{self.vedio_path}/{tid}')
						print(f"[{ctime()}] 文件已保存")
						return "code: 0"
					case _:
						return f"code: {url_list['code']}"
			case _:
				return f"code: {data['code']}"
	
	def cut_size(self, filesize):
		step = filesize//8
		a = list(range(0, filesize, step))
		r = []
		for i in range(len(a) - 1):
			start_byte, stop_byte = a[i], a[i+1] - 1
			r.append([start_byte, stop_byte])
		r[-1][-1] = filesize - 1
		return r

	def reader(self, name, tid, met):
		with open(f'{self.vedio_path}/{tid}/{name}.link', 'rb') as f:
			a = f.read()
		with open(f'{self.vedio_path}/{tid}.{met}', 'ab') as file:
			file.write(a)

	def thread_on(self, url, start_byte, stop_byte, tid):
		t = Thread(target=self.thread_download, args=(url, start_byte, stop_byte, tid, ))
		t.start()
		return t

	def thread_download(self, url, start_byte, stop_byte, tid):
		headers = self.headers
		headers['Range'] = f'bytes={start_byte}-{stop_byte}'
		data = self.meth.get_Html(
			url,
			'GET',
			'CONTENT',
			headers,
			self.encoding
			)
		if not exists(f'{self.vedio_path}/{tid}'): mkdir(f'./{self.vedio_path}/{tid}')
		with open(f'{self.vedio_path}/{tid}/{stop_byte}.link', 'wb') as f:
			f.write(data)
		self.lock.acquire()
		try:
			print(f"[{ctime()}] {self.vedio_path}/{tid}/{stop_byte}.link")
		finally:
			self.lock.release()
