"""
爬虫抽象基类
定义所有爬虫必须实现的接口
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import time
import requests

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config import REQUEST_CONFIG


class BaseScraper(ABC):
    """
    爬虫抽象基类
    
    所有站点爬虫都应继承此类并实现以下抽象方法：
    - get_article_list(): 获取文章列表
    - scrape_article(): 爬取单篇文章
    - run(): 主运行逻辑
    """
    
    def __init__(self, site_config: dict):
        """
        初始化爬虫
        
        Args:
            site_config: 站点配置字典，包含 base_url、selectors 等
        """
        self.site_config = site_config
        self.base_url = site_config.get("base_url", "")
        self.encoding = site_config.get("encoding", "utf-8")
        self.selectors = site_config.get("selectors", {})
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": REQUEST_CONFIG["user_agent"]
        })
    
    def _request(self, url: str) -> Optional[str]:
        """
        发送 HTTP GET 请求
        
        Args:
            url: 目标 URL
            
        Returns:
            响应的 HTML 文本，失败返回 None
        """
        try:
            response = self.session.get(url, timeout=REQUEST_CONFIG["timeout"])
            response.encoding = response.apparent_encoding or self.encoding
            return response.text
        except requests.RequestException as e:
            print(f"❌ 请求失败: {url} - {e}")
            return None
    
    def _delay(self) -> None:
        """请求间隔延迟，避免被封禁"""
        time.sleep(REQUEST_CONFIG["request_delay"])
    
    @abstractmethod
    def get_article_list(self, page: int = 1) -> List[Dict[str, str]]:
        """
        获取指定页的文章列表
        
        Args:
            page: 页码，从 1 开始
            
        Returns:
            文章列表，每个元素为 {"title": "标题", "link": "URL"}
        """
        pass
    
    @abstractmethod
    def scrape_article(self, url: str) -> Optional[Dict[str, str]]:
        """
        爬取单篇文章内容
        
        Args:
            url: 文章 URL
            
        Returns:
            文章数据字典 {"title": ..., "content": ..., "url": ...}，失败返回 None
        """
        pass
    
    @abstractmethod
    def run(self, max_pages: int = 1) -> List[Dict]:
        """
        运行爬虫主逻辑
        
        Args:
            max_pages: 最大爬取页数
            
        Returns:
            爬取到的所有文章列表
        """
        pass
