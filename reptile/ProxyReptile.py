# -*- encoding: utf-8 -*-
'''
@File    :   ProxyReptile.py
@Time    :   2023/02/05 20:54:36
@Author  :   UnAbuse 
'''

from packet import *

class Proxy(Meth):
	def __init__(self):
		super(GetIp, self).__init__()
		self.headers = {
			'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33'
		}
		self.url = 'https://www.beesproxy.com/free/page/'
		self.encoding = 'utf-8'

	def run(self, page):
		data = etree.HTML(super(GetIp, self).get_Html(
			''.join((self.url, str(page))),
			'GET',
			'text',
			self.headers,
			self.encoding
			))
		ip_list = data.xpath('//*[@id="article-copyright"]/figure/table/tbody/tr/td[1]')
		port_list = data.xpath('//*[@id="article-copyright"]/figure/table/tbody/tr/td[2]')
		with open('ip.proxy.txt', 'a+', encoding='utf-8') as f:
			res = list(map(lambda x, y: {
					"http": "".join(('http://', x.xpath('string(.)').strip(), ':', y.xpath('string(.)').strip())),
					"https": "".join(('http://', x.xpath('string(.)').strip(), ':', y.xpath('string(.)').strip()))
				},
				ip_list,
				port_list
				))
			list(map(lambda x: f.write(''.join((str(x), '\n'))), res))
