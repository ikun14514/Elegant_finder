import requests, json, re, time, random, os

class randomIP:
	def __init__(self, list_ip=None):
		self.list_ip = None
		if list_ip is None:
			self.list_ip = []
		else:
			self.list_ip = list_ip

	def randIP(self):
		file = open("IP代理池.txt")
		data = file.readlines()
		for i in data:
			i = i.strip('\n')
			self.list_ip.append(i)

def getHtml(url, enc):
	headers = {
	'Accept' :'application/json, text/plain, */*',
	'ser-ch-ua' :'" Not A;Brand";v="99", "Chromium";v="102", "Microsoft Edge";v="102"',
	'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33'
	}
	pa = randomIP()
	pa.randIP()
	list_ip = pa.list_ip
	l = len(list_ip)
	k = random.randint(0, l)
	try:
		html = requests.get(url, headers=headers, proxies=eval(list_ip[k-1]))
		html.encoding = enc
		return html.text
	except:
		print(list_ip[k-1])
		getHtml(url, enc)

def getId(i):
	'''
	获取所有待下载作品的id，i代表着page
	'''
	allpoint = []
	html = getHtml(f"https://api.pixivel.moe/v2/pixiv/illust/search/涩图?page={i}&sortpop=false&sortdate=false", 'utf-8')
	data = json.loads(html)["data"]["illusts"]
	for i in data:
		data = i["id"]
		allpoint.append(data)
	return allpoint

def getTime(pid):
	'''
	获取下载链接组成部分的时间并且完成图片链接的拼接，pid代表着作品pid
	'''
	html = getHtml(f"https://api.pixivel.moe/v2/pixiv/illust/{pid}", 'utf-8')
	data = json.loads(html)
	data = data["data"]["image"]
	data = re.findall(r'[0-9]+', data)
	data = f"https://proxy.pixivel.moe/img-master/img/{data[0]}/{data[1]}/{data[2]}/{data[3]}/{data[4]}/{data[5]}/{pid}_p0_master1200.jpg"
	return data

def downLoad(url, pid):
	headers = {
	'Accept' :'application/json, text/plain, */*',
	'ser-ch-ua' :'" Not A;Brand";v="99", "Chromium";v="102", "Microsoft Edge";v="102"',
	'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33'
	}
	pa = randomIP()
	pa.randIP()
	list_ip = pa.list_ip
	l = len(list_ip)
	k = random.randint(0, l)
	try:
		html = requests.get(url, headers=headers, proxies=eval(list_ip[k-1]))
		with open(f"image/{pid}.jpg", "wb") as f:
			f.write(html.content)
	except:
		print(list_ip[k-1])
		downLoad(url, pid)

def run(i):
	bid = getId(i)
	for pid in bid:
		if os.path.exists(f"image/{pid}.jpg") != True:
			try:
				url = getTime(pid)
				try:
					downLoad(url, pid)
					open('download.log', 'a+', encoding='utf-8').write(f"[{time.ctime()}] - {pid} download\n")
					print(f"{url} 下载完成")
					# time.sleep(random.randint(5, 15))
				except:
					open('download.log', 'a+', encoding='utf-8').write(f"[{time.ctime()}] - {pid} do not download\n")
					print(f"{url} 下载失败")
			except:
				open('download.log', 'a+', encoding='utf-8').write(f"[{time.ctime()}] - {pid} error\n")
				print(f"{pid} 无效")
		else:
			print(f"{pid} 存在")

def allinall():
	i = 0
	while True:
		i = i + 1
		try:
			run(i)
		except:
			print("代理出错")

allinall()
