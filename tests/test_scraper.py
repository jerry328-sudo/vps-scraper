"""
爬虫测试：精简版
逻辑：测试两种爬取方式能获取内容 → 只用 AI 跑一次提取
目的：减少 API 消耗，如果 AI 提取能工作，说明 API Key 配置正确
"""
import unittest
import sys
from pathlib import Path

# 确保项目根目录在 Python 路径中
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.scrapers import GWVPSScraper


class TestScraper(unittest.TestCase):
    """爬虫测试"""
    
    # 测试用的文章 URL
    TEST_URL = "https://www.gwvpsceping.com/8810.html"
    
    @classmethod
    def setUpClass(cls):
        """测试类初始化，获取 API Key 状态"""
        from config import API_KEYS
        cls.has_zhipu_key = bool(API_KEYS.get("zhipu"))
        cls.has_tavily_key = bool(API_KEYS.get("tavily"))
        
        # 用于存储爬取的内容，供 AI 提取使用
        cls.scraped_content = None
        cls.scraper = None
    
    def test_1_scraper_initialization(self):
        """测试爬虫初始化"""
        # 默认初始化
        scraper1 = GWVPSScraper()
        self.assertFalse(scraper1.use_tavily)
        
        # 使用 Tavily
        scraper2 = GWVPSScraper(use_tavily=True)
        self.assertTrue(scraper2.use_tavily)
        
        # 验证必需的方法存在
        for method in ['scrape_with_ai', 'scrape_article', 'get_article_list']:
            self.assertTrue(hasattr(scraper1, method), f"缺少方法: {method}")
            self.assertTrue(callable(getattr(scraper1, method)))
        
        print("✅ 爬虫初始化测试通过")
    
    def test_2_standard_scrape(self):
        """测试标准爬取方式（requests + BeautifulSoup）"""
        scraper = GWVPSScraper(use_tavily=False)
        
        # 只爬取内容，不调用 AI
        result = scraper.scrape_article(self.TEST_URL)
        
        self.assertIsNotNone(result, "标准爬取应返回内容")
        self.assertIn("content", result, "结果应包含 content 字段")
        self.assertGreater(len(result.get("content", "")), 100, "内容应有足够长度")
        
        # 保存内容供后续 AI 测试使用
        TestScraper.scraped_content = result.get("content")
        TestScraper.scraper = scraper
        
        print(f"✅ 标准爬取测试通过，内容长度: {len(result.get('content', ''))} 字符")
    
    def test_3_tavily_scrape(self):
        """测试 Tavily 爬取方式"""
        if not self.has_tavily_key:
            self.skipTest("未配置 TAVILY_API_KEY，跳过 Tavily 测试")
        
        scraper = GWVPSScraper(use_tavily=True)
        
        # 只爬取内容，不调用 AI
        result = scraper.scrape_article(self.TEST_URL)
        
        self.assertIsNotNone(result, "Tavily 爬取应返回内容")
        self.assertIn("content", result, "结果应包含 content 字段")
        self.assertGreater(len(result.get("content", "")), 100, "内容应有足够长度")
        
        print(f"✅ Tavily 爬取测试通过，内容长度: {len(result.get('content', ''))} 字符")
    
    def test_4_ai_extraction(self):
        """测试 AI 提取（只运行一次，验证完整流程）"""
        if not self.has_zhipu_key:
            self.skipTest("未配置 ZHIPU_API_KEY，跳过 AI 提取测试")
        
        # 使用之前爬取的内容，避免重复请求
        if TestScraper.scraped_content is None:
            # 如果前面的测试没有保存内容，现在爬取
            scraper = GWVPSScraper(use_tavily=False)
            article = scraper.scrape_article(self.TEST_URL)
            content = article.get("content", "") if article else ""
        else:
            content = TestScraper.scraped_content
            scraper = TestScraper.scraper or GWVPSScraper(use_tavily=False)
        
        self.assertGreater(len(content), 0, "需要有内容才能测试 AI 提取")
        
        # 调用 AI 提取
        from src.ai_clients.zhipu_client import extract_vps_info
        result = extract_vps_info(content)
        
        self.assertIsNotNone(result, "AI 提取应返回结果")
        self.assertIsInstance(result, dict, "结果应是字典类型")
        
        # 验证基本结构
        if "products" in result:
            self.assertIsInstance(result["products"], list)
            print(f"✅ AI 提取测试通过，提取到 {len(result['products'])} 个产品")
        else:
            print("✅ AI 提取测试通过（返回结果但无产品数据）")


if __name__ == '__main__':
    unittest.main(verbosity=2)
