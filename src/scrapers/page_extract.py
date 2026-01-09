"""
页面提取工具
提供两种页面内容提取方式：
1. 标准爬虫方式（使用 requests）
2. Tavily API 提取方式（更智能的内容提取）
"""
from typing import Optional
import os

from tavily import TavilyClient

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config import API_KEYS


def extract_page_with_tavily(url: str) -> Optional[str]:
    """
    使用 Tavily API 提取页面内容
    
    Args:
        url: 要提取的页面 URL
        
    Returns:
        提取的页面文本内容，失败返回 None
    """
    # 获取 Tavily API Key
    api_key = API_KEYS.get("tavily", "")
    if not api_key:
        print("❌ 未配置 Tavily API Key，请设置环境变量 TAVILY_API_KEY")
        return None
    
    try:
        client = TavilyClient(api_key=api_key)
        print(f"📡 使用 Tavily API 提取页面: {url}")
        
        response = client.extract(urls=[url])
        
        # Tavily 返回的结构: {"results": [{"url": "...", "raw_content": "..."}]}
        if response and "results" in response and len(response["results"]) > 0:
            result = response["results"][0]
            content = result.get("raw_content", "")
            
            if content:
                print(f"✅ Tavily 提取成功，内容长度: {len(content)} 字符")
                return content
            else:
                print("⚠️  Tavily 未返回内容")
                return None
        else:
            print("⚠️  Tavily API 返回结果为空")
            return None
            
    except Exception as e:
        print(f"❌ Tavily API 调用失败: {e}")
        return None


if __name__ == "__main__":
    # 测试用例
    test_url = "https://www.gwvpsceping.com/8810.html"
    content = extract_page_with_tavily(test_url)
    if content:
        print("\n" + "="*80)
        print("提取的内容预览（前 500 字符）:")
        print("="*80)
        print(content[:500])
        print("...")