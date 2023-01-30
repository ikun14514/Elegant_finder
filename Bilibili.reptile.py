from packet import *

class Bilibili(Meth):
	def __init__(self):
		super(Bilibili, self).__init__()
		self.headers = {
			'Referer': 'https://www.bilibili.com/',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
		}
		self.encoding = 'utf-8'
		self.cid_url = 'https://api.bilibili.com/x/web-interface/view'
		self.video_url = 'https://api.bilibili.com/x/player/playurl'
	
	def download(self, pid, url):
		data = super(Bilibili, self).get_Html(
			url,
			'GET',
			'img',
			self.headers,
			self.encoding
			)
		with open(f'vedio/{pid}.mp4', "wb") as f:
			f.write(data)
			print(f'{pid} => OK!')
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
						'cid': cid
					}
					)
				match url_list['code']:
					case 0:
						self.download(tid, url_list['data']['durl'][0]['url'])
					case _:
						return url_list['code']
			case _:
				return data['code']
