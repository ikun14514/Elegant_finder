# -*- encoding: utf-8 -*-
'''
@File    :   BilibiliReptile.py
@Time    :   2023/02/05 20:53:03
@Author  :   UnAbuse 
'''

from packet import *

class Bilibili(Meth):
	def __init__(self):
		'''
		1、Cookie的获取通过Cookie.txt来加载
		2、直播与视频的headers不一样, 需要分开使用
		'''
		super(Bilibili, self).__init__()
		with open('Cookie.txt', 'r+', encoding='utf-8') as f:
			Cookie = f.read()
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
		self.lock = Lock()

	def thread(self, pid, data, met):
		'''
		开启多线程, 但是并未写join(), 考虑到主线程执行到这边一般都差不多
		并且加了锁, 写了也没有必要
		'''
		t = Thread(target=self.download, args=(pid, data, met))
		t.start()
		return 1

	def download(self, pid, data, met):
		'''
		下载方法, 加锁保证不会乱序写入
		唯一注意的是ab写入特性
		'''
		self.lock.acquire()
		print(f'{current_thread().name} is run, byte: 512000, time: [{ctime()}]', end='\r')
		with open(f'vedio/{pid}.{met}', "ab") as f:
			f.write(data)
		self.lock.release()
		return 1

	def live_run(self, room_id):
		print(f'开始运行 => time: [{ctime()}]')
		data = super(Bilibili, self).get_Html(
			self.room_id_url,
			'GET',
			'json',
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
						print(f"房间真实ID:{data['data']['room_id']}")
						live_streaming = super(Bilibili, self).get_Html(
							self.live_url,
							'GET',
							'json',
							self.live_headers,
							self.encoding,
							{
								'cid': data['data']['room_id'],
								'quality': 4,
								'platform': 'web'
							}
							)
						match live_streaming['code']:
							case 0:
								url = live_streaming['data']['durl'][0]['url']
								print(f'直播视频流链接：{url}')
								dat = super(Bilibili, self).get_Html(
									url,
									'TGET',
									'timg',
									self.live_headers,
									self.encoding
									)
								print(f'开始录制 => [{ctime()}]')
								list(map(lambda x: self.thread(room_id, x, 'flv'), dat))
								return 'code: 0'
							case _:
								return 'code: ' + live_streaming['code']
			case 1:
				return 'code: 1'

	def vedio_run(self, bid, tid):
		print(f'开始运行 => time: [{ctime()}]')
		data = super(Bilibili, self).get_Html(
			self.cid_url,
			'GET',
			'json',
			self.headers,
			self.encoding,
			{
				bid: tid
			}
			)
		match data['code']:
			case 0:
				cid = data['data']['cid']
				print(f"视频CID:{cid}")
				url_list = super(Bilibili, self).get_Html(
					self.video_url,
					'GET',
					'json',
					self.headers,
					self.encoding,
					{
						bid: tid,
						'cid': cid,
						'qn': 80
					}
					)
				match url_list['code']:
					case 0:
						print(f"视频链接:{url_list['data']['durl'][0]['url']}")
						data = super(Bilibili, self).get_Html(
							url_list['data']['durl'][0]['url'],
							'TGET',
							'timg',
							self.headers,
							self.encoding
							)
						list(map(lambda x: self.thread(tid, x, 'mp4'), data))
						print(f'{tid} => OK!, time: [{ctime()}]')
						return "code: 0"
					case _:
						return f"code: {url_list['code']}"
			case _:
				return f"code: {data['code']}"