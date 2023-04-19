# -*- encoding: utf-8 -*-
'''
@File    :   FanQieNovelReptile.py
@Time    :   2023/02/05 20:53:29
@Author  :   UnAbuse 
'''

from reptile.packet import *

class FanQie:
    def __init__(self):
        # 定义基本参数
        super().__init__()
        Cookie = ''
        self.search_url = 'https://novel.snssdk.com/api/novel/channel/homepage/search/search/v1/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Danger hiptop 3.4; U; AvantGo 3.2)',
            'Cookie': Cookie
            }
        self.encoding = 'utf-8'
        self.directory_url = 'https://novel.snssdk.com/api/novel/book/directory/list/v1/'
        self.content_url = 'https://novel.snssdk.com/api/novel/book/reader/full/v1/'
        self.meth = Meth()

    def search(self, keywords):
        # 获得书本基本信息
        params = {
            'aid': 13,
            'q': keywords
            }
        book_list_info = self.meth.get_Html(
            self.search_url,
            'GET',
            'JSON',
            self.headers,
            self.encoding,
            params
            )
        return book_list_info['data']['ret_data']

    def direct(self, book_id):
        # 获取书本目录
        params = {
            'book_id': book_id,
            'aid': 1967,
            'iid': 2665637677906061,
            'app_name': 'novelapp',
            'version_code': 495
            }
        direc_list_info = self.meth.get_Html(
            self.directory_url,
            'GET',
            'JSON',
            self.headers,
            self.encoding,
            params
            )
        return direc_list_info['data']['item_list']

    def content(self, item_id):
        # 获取当前章节正文内容
        params = {
            'group_id': item_id,
            'item_id': item_id
            }
        content_info = self.meth.get_Html(
            self.content_url,
            'GET',
            'JSON',
            self.headers,
            self.encoding,
            params
            )
        try:
            return content_info['data']['content']
        except:
            return '未配置cookie或者cookie失效'
