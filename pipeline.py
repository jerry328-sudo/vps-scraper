#!/usr/bin/env python
"""
VPS 测评文章爬虫 - Pipeline 脚本
爬取最近文章并用 AI 总结为 JSON

直接运行: python pipeline.py
"""
import sys
import os
import shutil
from datetime import datetime

# 确保项目根目录在 Python 路径中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.scrapers import GWVPSScraper

# ============================================================
# 参数配置（在此处修改）
# ============================================================

# 爬取最近 N 天的文章
DAYS = 5

# 爬取文章列表的线程数
SCRAPE_THREADS = 4

# AI 处理的线程数
AI_THREADS = 5

# 最大爬取页数（防止无限爬取）
MAX_PAGES = 50

# 页面提取方式
# - False: 标准爬虫（requests + html_to_text）- 免费，可能遇到反爬
# - True:  Tavily API 提取 - 需要 API Key，质量更高，更稳定
USE_TAVILY = True

# 数据目录配置
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
OLD_DATA_DIR = os.path.join(DATA_DIR, "old")

# ============================================================
# 辅助函数
# ============================================================

def archive_old_data():
    """
    将旧数据移入 data/old 文件夹
    按时间戳创建子目录，保留历史数据
    """
    # 需要归档的目录
    dirs_to_archive = ["raw", "html", "articles"]
    
    # 检查是否有数据需要归档
    has_data = False
    for dir_name in dirs_to_archive:
        dir_path = os.path.join(DATA_DIR, dir_name)
        if os.path.exists(dir_path) and os.listdir(dir_path):
            has_data = True
            break
    
    if not has_data:
        print("📂 没有旧数据需要归档")
        return
    
    # 创建带时间戳的归档目录
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_dir = os.path.join(OLD_DATA_DIR, timestamp)
    os.makedirs(archive_dir, exist_ok=True)
    
    print(f"📦 正在归档旧数据到: data/old/{timestamp}/")
    
    moved_count = 0
    for dir_name in dirs_to_archive:
        src_dir = os.path.join(DATA_DIR, dir_name)
        if not os.path.exists(src_dir):
            continue
        
        files = os.listdir(src_dir)
        if not files:
            continue
        
        # 创建目标目录
        dest_dir = os.path.join(archive_dir, dir_name)
        os.makedirs(dest_dir, exist_ok=True)
        
        # 移动文件
        for filename in files:
            src_file = os.path.join(src_dir, filename)
            dest_file = os.path.join(dest_dir, filename)
            if os.path.isfile(src_file):
                shutil.move(src_file, dest_file)
                moved_count += 1
    
    print(f"✅ 已归档 {moved_count} 个文件")
    print()

# ============================================================
# 主程序
# ============================================================

def main():
    """运行 Pipeline"""
    print("=" * 60)
    print("🚀 VPS 测评文章爬虫 - Pipeline")
    print("=" * 60)
    print(f"   日期范围: 最近 {DAYS} 天")
    print(f"   爬取线程: {SCRAPE_THREADS}")
    print(f"   AI 线程:  {AI_THREADS}")
    print(f"   最大页数: {MAX_PAGES}")
    print(f"   提取方式: {'Tavily API' if USE_TAVILY else '标准爬虫'}")
    print("=" * 60)
    print()
    
    # 检查必需的 API Key
    from config import API_KEYS
    
    zhipu_key = API_KEYS.get("zhipu", "")
    tavily_key = API_KEYS.get("tavily", "")
    
    if not zhipu_key:
        print("❌ 错误: 未配置 ZHIPU_API_KEY")
        print("   请在 .env 文件中配置或设置环境变量")
        print("   获取地址: https://open.bigmodel.cn/")
        sys.exit(1)
    
    if USE_TAVILY and not tavily_key:
        print("❌ 错误: USE_TAVILY=True 但未配置 TAVILY_API_KEY")
        print("   请在 .env 文件中配置或设置环境变量")
        print("   获取地址: https://tavily.com/")
        sys.exit(1)
    
    # 归档旧数据
    archive_old_data()
    
    # 创建爬虫实例
    scraper = GWVPSScraper(use_tavily=USE_TAVILY)
    
    # 运行 Pipeline
    results = scraper.pipeline_recent_to_json(
        days=DAYS,
        scrape_threads=SCRAPE_THREADS,
        ai_threads=AI_THREADS,
        max_pages=MAX_PAGES
    )
    
    # 输出结果摘要
    if results:
        print()
        print("📊 处理结果摘要:")
        print("-" * 40)
        for i, result in enumerate(results, 1):
            vendor = result.get("vendor", "未知")
            product = result.get("product_name", "未知")
            date = result.get("publish_date", "")
            print(f"   {i}. [{date}] {vendor} - {product}")
    
    return results


if __name__ == "__main__":
    main()
