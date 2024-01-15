# -*- encoding: utf-8 -*-
# verified time: 2024/1/15

from config import *
from requests import Session

class FanQie:
    def __init__(self) -> None:
        # 初始化函数，定义基本参数
        super().__init__()  # 调用父类的初始化函数
        self.session = Session()  # 创建一个Session对象，并赋值给self.session

    def search(self, keywords: str) -> list:
        """
        搜索书籍信息

        参数:
        keywords (str): 关键字

        返回:
        list: 书籍信息列表
        """
        # 获得书本基本信息
        params = {
            'aid': 13,
            'q': keywords
        }
        book_list_info = self.session.get(search_url, params=params, headers=headers).json()
        return book_list_info['data']['ret_data']

    def direct(self, book_id: str) -> list:
        # 获取书本目录
        params = {
            'book_id': book_id,  # 书本ID
            'device_platform': 'android',  # 设备平台
            'version_code': 600,  # 版本码
            'novel_version': None,  # 小说版本
            'app_name': 'news_article',  # 应用名称
            'version_name': '6.0.0',  # 应用版本名
            'app_version': '6.0.0aid=520',  # 应用版本号
            'channel': '1',  # 渠道
            'device_type': 'landseer',  # 设备类型
            'os_api': '25',  # 操作系统API
            'os_version': '10',  # 操作系统版本
        }
        direc_list_info = self.session.get(directory_url, params=params, headers=headers).json()
        return direc_list_info['data']['item_list']

    def content(self, item_id: str) -> str:
        """
        获取当前章节正文内容

        Args:
            item_id (str): 章节ID

        Returns:
            str: 章节正文内容

        Raises:
            str: '未配置cookie或者cookie失效'
        """
        # 定义参数
        params = {
            'aid': 2329,
            'item_id': item_id
        }
        # 发送GET请求并解析响应内容为JSON格式
        content_info = self.session.get(content_url, params=params, headers=headers).json()
        try:
            # 返回章节正文内容
            return content_info['data']['content']
        except:
            # 返回错误信息，表示未配置cookie或者cookie失效
            return '未配置cookie或者cookie失效'
