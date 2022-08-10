import requests, time
from lxml import etree, html
from tqdm import tqdm

def getHtml(url, enc):
	headers = {
	'Accept' :'application/json, text/plain, */*',
	'ser-ch-ua' :'" Not A;Brand";v="99", "Chromium";v="102", "Microsoft Edge";v="102"',
	'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33'
	}
	html = requests.get(url, headers=headers)
	html.encoding = enc
	return html.text

def getIP(i, url):
	html = getHtml(f"https://www.beesproxy.com/free/page/{i}/", 'utf-8')
	data = etree.HTML(html)
	headers = {
	'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33'
	}
	data_ip = data.xpath('//*[@id="article-copyright"]/figure/table/tbody/tr/td[1]')
	data_port = data.xpath('//*[@id="article-copyright"]/figure/table/tbody/tr/td[2]')
	file = open("IP代理池.txt", 'a+', encoding='utf-8')
	for n, m in enumerate(data_ip, 0):
		list_ip = m.xpath('string(.)').strip()
		proxies = {
		"http" :f"http://{list_ip}:{data_port[n].xpath('string(.)').strip()}",
		"https" :f"http://{list_ip}:{data_port[n].xpath('string(.)').strip()}"
		}
		try:
			html = requests.get(url, headers=headers, proxies=proxies, timeout=2)
			if html.status_code == 200:
				file.write(f"{proxies}\n")
				print(f"{list_ip} 可用")
			else:
				pass
		except:
			pass

def run():
	url = input("根据要爬取的网址判断IP可用性：")
	for i in tqdm(range(1, 101)):
		getIP(i, url)
		time.sleep(1)
	file = open("IP代理池.txt", encoding='utf-8')
	print(f"可用代理：{len(file.readlines())}")
	file.close()

run()
