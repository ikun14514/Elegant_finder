import requests, time, re, json
from lxml import etree, html

def getHtml(url, enc):
	headers = {
	'User-Agent' :'Mozilla/5.0 (Danger hiptop 3.4; U; AvantGo 3.2)'
	}
	html = requests.get(url, headers=headers)
	html.encoding = enc
	return html.text

def get_in_text(buid, name):
	'''
	buid:书本的book_id，可以在get_in_book模块里面查询得到
	name:就是保存得到的文件名，如果在次级目录下，请先建立目录
	'''
	allpoint = get_in_fan(buid)
	files = open(f"data/{name}.txt", 'a', encoding='utf-8')
	for i in allpoint:
		url = f"https://novel.snssdk.com/api/novel/book/reader/full/v1/?group_id={i}&item_id={i}"
		data = getHtml(url, 'utf-8')
		data = json.loads(data)
		data = data["data"]
		data2 = data["content"] # 正文
		data2 = etree.HTML(data2)
		data3 = data2.xpath('//*[@class="tt-title"]/text()')[0] # 标题
		files.write(data3 + "\n")
		data4 = data2.xpath('/html/body/article/p')
		for m in data4:
			data4 = m.xpath('string(.)').strip()
			files.write("    " + data4 + "\n")
	files.close()
	return {"result" :"success"}


def get_in_fan(uid):
	'''
	uid:书本的book_id，可以在get_in_book模块里面查询得到
	这个模块可以查询到所有的章节id，然后传输到get_in_text里面
	'''
	url = f"https://api5-normal-lf.fqnovel.com/reading/bookapi/directory/all_items/v/?need_version=true&book_id={uid}&iid=2665637677906061&aid=1967&app_name=novelapp&version_code=495"
	allpoint = []
	data = getHtml(url, 'utf-8')
	data = json.loads(data)
	data = data["data"]
	data = data["item_data_list"]
	for i in data:
		data = i["item_id"]
		allpoint.append(data)
	return allpoint

def get_in_book(name):
	'''搜索书本的基础信息，获取book_id以供使用'''
	url = f"https://api5-normal-lf.fqnovel.com/reading/bookapi/search/page/v/?offset=0&passback=&query={name}&search_id=&iid=4125792742674311&aid=1967"
	allpoint = []
	try:
		data = getHtml(url, 'utf-8')
		data = json.loads(data)
		data = data["data"]
		for i in data:
			data = i["book_data"]
			data = data[0]
			res = {
			'book_name': data["book_name"],
			'abstract': data["abstract"],
			'author': data["author"],
			'score': data["score"],
			'book_id': data["book_id"]
			}
			allpoint.append(res)
		return allpoint
	except:
		return None

