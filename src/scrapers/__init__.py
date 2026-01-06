"""
爬虫模块入口
导出所有爬虫类
"""

from .base import BaseScraper
from .gwvps_scraper import GWVPSScraper

__all__ = [
    "BaseScraper",
    "GWVPSScraper",
]
