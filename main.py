#!/usr/bin/env python
"""
VPS 测评文章爬虫 - CLI 入口
支持多站点爬取，输出 JSON 或 Markdown 格式
"""
import argparse
import sys
import os

# 确保项目根目录在 Python 路径中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.scrapers import GWVPSScraper
from config import SCRAPE_CONFIG


def create_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        description="VPS 测评文章爬虫 - 爬取 VPS 测评网站并提取结构化数据",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 爬取默认 1 页，输出 JSON
  python main.py
  
  # 爬取 3 页
  python main.py -p 3
  
  # 爬取单篇文章
  python main.py -u https://www.gwvpsceping.com/8785.html
  
  # 输出为 Markdown
  python main.py -f markdown
  
  # 查看最近 5 天的文章
  python main.py --recent 5
  
  # Pipeline: 爬取最近文章并用 AI 总结为 JSON
  python main.py --pipeline 3
  
  # 使用 uv 运行
  uv run python main.py -p 2
"""
    )
    
    parser.add_argument(
        "-p", "--pages",
        type=int,
        default=SCRAPE_CONFIG.get("default_pages", 1),
        help=f"爬取页数（默认: {SCRAPE_CONFIG.get('default_pages', 1)}）"
    )
    
    parser.add_argument(
        "-s", "--site",
        type=str,
        default="gwvps",
        choices=["gwvps"],
        help="目标站点（默认: gwvps）"
    )
    
    parser.add_argument(
        "-u", "--url",
        type=str,
        default=None,
        help="单篇文章 URL（指定时忽略 --pages）"
    )
    
    parser.add_argument(
        "-f", "--format",
        type=str,
        default="json",
        choices=["json", "markdown"],
        help="输出格式（默认: json）"
    )
    
    parser.add_argument(
        "-r", "--recent",
        type=int,
        default=None,
        metavar="DAYS",
        help="查看最近 N 天的文章列表（使用多线程）"
    )
    
    parser.add_argument(
        "-t", "--threads",
        type=int,
        default=4,
        help="爬取线程数（用于 --recent 和 --pipeline 模式，默认: 4）"
    )
    
    parser.add_argument(
        "--pipeline",
        type=int,
        default=None,
        metavar="DAYS",
        help="Pipeline 模式：爬取最近 N 天文章并用 AI 总结为 JSON"
    )
    
    parser.add_argument(
        "--ai-threads",
        type=int,
        default=2,
        help="AI 处理线程数（仅用于 --pipeline 模式，默认: 2）"
    )
    
    return parser


def get_scraper(site: str):
    """根据站点名称获取对应的爬虫实例"""
    scrapers = {
        "gwvps": GWVPSScraper,
    }
    
    scraper_class = scrapers.get(site)
    if not scraper_class:
        print(f"❌ 不支持的站点: {site}")
        print(f"   支持的站点: {', '.join(scrapers.keys())}")
        sys.exit(1)
    
    return scraper_class()


def main():
    """主入口函数"""
    parser = create_parser()
    args = parser.parse_args()
    
    print("=" * 50)
    print("🕷️  VPS 测评文章爬虫")
    print("=" * 50)
    print(f"站点: {args.site}")
    
    # 获取爬虫实例
    scraper = get_scraper(args.site)
    
    # Pipeline 模式：爬取 + AI 总结
    if args.pipeline is not None:
        print(f"模式: Pipeline（爬取 + AI 总结）")
        print(f"天数: {args.pipeline}")
        print(f"爬取线程: {args.threads}")
        print(f"AI 线程: {args.ai_threads}")
        print("=" * 50)
        print()
        
        results = scraper.pipeline_recent_to_json(
            days=args.pipeline,
            scrape_threads=args.threads,
            ai_threads=args.ai_threads
        )
        return
    
    # 最近文章模式
    if args.recent is not None:
        print(f"模式: 最近文章查询")
        print(f"天数: {args.recent}")
        print(f"线程数: {args.threads}")
        print("=" * 50)
        print()
        
        articles = scraper.print_recent_articles(
            days=args.recent,
            num_threads=args.threads
        )
        return
    
    # 常规爬取模式
    print(f"输出格式: {args.format}")
    
    if args.url:
        print(f"模式: 单篇文章")
        print(f"URL: {args.url}")
    else:
        print(f"模式: 列表爬取")
        print(f"页数: {args.pages}")
    
    print("=" * 50)
    print()
    
    # 运行爬虫
    results = scraper.run(
        max_pages=args.pages,
        output_format=args.format,
        single_url=args.url
    )
    
    print()
    print("=" * 50)
    print(f"✅ 爬取完成，共处理 {len(results)} 篇文章")
    print("=" * 50)


if __name__ == "__main__":
    main()
