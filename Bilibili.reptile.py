from packet import *

class Bilibili(Meth):
	def __init__(self):
		super(Bilibili, self).__init__()
		Cookie = ""
		self.headers = {
			'Referer': 'https://www.bilibili.com/',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
			'Cookie': Cookie
		}
		self.encoding = 'utf-8'
		self.cid_url = 'https://api.bilibili.com/x/web-interface/view'
		self.video_url = 'https://api.bilibili.com/x/player/playurl'
		self.qrcode_url = 'https://passport.bilibili.com/x/passport-login/web/qrcode/generate'
		self.lock = Lock()

	def thread(self, pid, data):
		t = Thread(target=self.download, args=(pid, data))
		t.start()
		return 1

	def download(self, pid, data):
		self.lock.acquire()
		with open(f'vedio/{pid}.mp4', "ab") as f:
			f.write(data)
			print('thread is done')
		self.lock.release()
		return 1

	def run(self, bid, tid):
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
						data = super(Bilibili, self).get_Html(
							url_list['data']['durl'][0]['url'],
							'TGET',
							'timg',
							self.headers,
							self.encoding
							)
						list(map(lambda x: self.thread(tid, x), data))
						print(f'{tid} => OK!')
					case _:
						return url_list['code']
			case _:
				return data['code']
