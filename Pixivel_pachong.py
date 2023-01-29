from packet import *

class Pa(Meth):
	def __init__(self):
		super(Pa, self).__init__()
		self.headers = {
			'Accept' :'application/json, text/plain, */*',
			'Referer': 'https://pixivel.moe/',
			'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33'
		}
		self.encoding = 'utf-8'
		self.api_id = 'https://api.pixivel.moe/v2/pixiv/illust/search/'
		self.api_list = 'https://api.pixivel.moe/v2/pixiv/illust/'
		self.api_img = ['https://proxy.pixivel.moe/img-master/img/', '_p0_master1200.jpg']

	def download(self, pid, url):
		data = super(Pa, self).get_Html(
			url,
			'GET',
			'img',
			self.headers,
			self.encoding
			)
		with open(f'image/{pid}.jpg', "wb") as f:
			f.write(data)
			print(f'{pid} => OK!')
		return 1

	def thread(self, pid, url):
		t = Thread(target=self.download, args=(pid, url))
		t.start()
		# t.join()
		return 1

	def run(self, name, page):
		try:
			list_id = super(Pa, self).get_Html(
				''.join((self.api_id, name)),
				'GET',
				'json',
				self.headers,
				self.encoding,
				{
					'page': page,
					'sortpop': 'true',
					'sortdate': 'false'
				})
			id_list = list(map(
				lambda x: x['id'],
				list_id['data']['illusts']
				))
			res = list(map(
				lambda x: super(Pa, self).get_Html(
					''.join((self.api_list, str(x))),
					'GET',
					'json',
					self.headers,
					self.encoding
					)['data']['image'],
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
			list(map(lambda x, y: self.thread(x, y), id_list, url_list))
			return 1
		except:
			return 0
