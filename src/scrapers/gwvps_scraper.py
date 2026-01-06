"""
狗汪 VPS 测评网爬虫
爬取 https://www.gwvpsceping.com/ 的 VPS 测评文章
"""
from typing import List, Dict, Optional, Tuple
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.scrapers.base import BaseScraper
from src.ai_clients.zhipu_client import extract_vps_info
from src.utils import sanitize_filename, save_to_json, save_to_markdown, save_to_html
from config import TARGET_SITES, OUTPUT_CONFIG


class GWVPSScraper(BaseScraper):
    """
    狗汪 VPS 测评网爬虫实现
    
    支持两种输出格式：
    - JSON: 使用 AI 提取结构化数据
    - Markdown: 保存原始文章内容
    """
    
    def __init__(self):
        super().__init__(TARGET_SITES["gwvps"])
    
    def get_article_list(self, page: int = 1) -> List[Dict[str, str]]:
        """获取指定页的文章列表"""
        if page == 1:
            url = self.base_url
        else:
            url = f"{self.base_url}/page/{page}"
        
        print(f"📄 正在获取第 {page} 页文章列表: {url}")
        html = self._request(url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, "html.parser")
        articles = []
        
        # 使用配置的选择器查找文章链接
        selector = self.selectors.get("article_list", "h2 > a")
        for link in soup.select(selector):
            title = link.get_text(strip=True)
            href = link.get("href", "")
            if title and href:
                # 处理相对链接
                if not href.startswith("http"):
                    href = f"{self.base_url}/{href.lstrip('/')}"
                articles.append({"title": title, "link": href})
        
        print(f"   找到 {len(articles)} 篇文章")
        return articles
    
    def scrape_article(self, url: str) -> Optional[Dict[str, str]]:
        """爬取单篇文章内容"""
        print(f"📡 正在爬取: {url}")
        html = self._request(url)
        if not html:
            return None
        
        soup = BeautifulSoup(html, "html.parser")
        
        # 提取标题
        title_selector = self.selectors.get("article_title", "h1")
        title_elem = soup.select_one(title_selector)
        title = title_elem.get_text(strip=True) if title_elem else "无标题"
        
        # 提取正文
        content_selector = self.selectors.get("article_content", "article")
        content_elem = soup.select_one(content_selector)
        content = str(content_elem) if content_elem else ""
        
        return {
            "title": title,
            "content": content,
            "html": html,
            "url": url,
        }
    
    def scrape_with_ai(self, url: str) -> Optional[Dict]:
        """
        爬取文章并使用 AI 提取结构化数据
        
        Args:
            url: 文章 URL
            
        Returns:
            AI 提取的结构化数据字典
        """
        print(f"📡 正在爬取: {url}")
        html = self._request(url)
        if not html:
            return None
        
        print(f"✅ HTML 获取成功，长度: {len(html)} 字符")
        
        # 调用 AI 提取结构化数据
        print("🤖 正在调用大模型提取结构化数据...")
        vps_info = extract_vps_info(html)
        
        if vps_info:
            vps_info["source_url"] = url
            return vps_info
        
        return None
    
    def run(
        self, 
        max_pages: int = 1, 
        output_format: str = "json",
        single_url: Optional[str] = None
    ) -> List[Dict]:
        """
        运行爬虫
        
        Args:
            max_pages: 最大爬取页数
            output_format: 输出格式，"json" 或 "markdown"
            single_url: 单篇文章 URL（指定时忽略 max_pages）
            
        Returns:
            爬取结果列表
        """
        results = []
        
        # 单篇文章模式
        if single_url:
            if output_format == "json":
                result = self.scrape_with_ai(single_url)
            else:
                result = self.scrape_article(single_url)
            
            if result:
                self._save_result(result, output_format)
                results.append(result)
            return results
        
        # 列表爬取模式
        for page in range(1, max_pages + 1):
            articles = self.get_article_list(page)
            
            for article in articles:
                self._delay()
                
                if output_format == "json":
                    result = self.scrape_with_ai(article["link"])
                else:
                    result = self.scrape_article(article["link"])
                
                if result:
                    self._save_result(result, output_format)
                    results.append(result)
        
        print(f"\n✅ 爬取完成，共 {len(results)} 篇文章")
        return results
    
    def _save_result(self, result: Dict, output_format: str) -> None:
        """保存爬取结果到文件"""
        if output_format == "json":
            # JSON 格式：从 URL 提取文件名
            url = result.get("source_url", "")
            filename = url.split("/")[-1].replace(".html", "")
            filename = sanitize_filename(filename) or "article"
            output_dir = OUTPUT_CONFIG["raw_dir"]
            save_to_json(result, filename, output_dir)
            vendor = result.get("vendor", "未知")
            product = result.get("product_name", "未知")
            print(f"   商家: {vendor} | 产品: {product}")
        else:
            # Markdown 格式
            title = result.get("title", "无标题")
            filename = sanitize_filename(title)
            output_dir = OUTPUT_CONFIG["articles_dir"]
            save_to_markdown(
                title=title,
                content=result.get("content", ""),
                url=result.get("url", ""),
                filename=filename,
                output_dir=output_dir
            )

    def _get_articles_with_date_from_page(self, page: int) -> List[Dict[str, str]]:
        """
        获取指定页的文章列表（包含日期）
        
        Args:
            page: 页码
            
        Returns:
            包含 title, link, date 的文章列表
        """
        if page == 1:
            url = self.base_url
        else:
            url = f"{self.base_url}/page/{page}"
        
        html = self._request(url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, "html.parser")
        articles = []
        
        # 查找所有文章元素
        for article_elem in soup.select("article"):
            # 提取标题和链接
            link_elem = article_elem.select_one("h2 > a")
            if not link_elem:
                continue
            
            title = link_elem.get_text(strip=True)
            href = link_elem.get("href", "")
            if not title or not href:
                continue
            
            # 处理相对链接
            if not href.startswith("http"):
                href = f"{self.base_url}/{href.lstrip('/')}"
            
            # 提取日期
            time_elem = article_elem.select_one("time")
            date_str = time_elem.get_text(strip=True) if time_elem else ""
            
            articles.append({
                "title": title,
                "link": href,
                "date": date_str
            })
        
        return articles

    def _fetch_page_worker(self, page: int, cutoff_date: datetime, results: List, lock: threading.Lock, stop_event: threading.Event) -> bool:
        """
        线程工作函数：获取单页文章并过滤日期
        
        Args:
            page: 页码
            cutoff_date: 截止日期（只保留此日期之后的文章）
            results: 共享结果列表
            lock: 线程锁
            stop_event: 停止事件
            
        Returns:
            是否应该继续抓取（True=继续，False=停止）
        """
        if stop_event.is_set():
            return False
        
        articles = self._get_articles_with_date_from_page(page)
        
        page_has_recent = False
        filtered_articles = []
        
        for article in articles:
            date_str = article.get("date", "")
            if date_str:
                try:
                    article_date = datetime.strptime(date_str, "%Y-%m-%d")
                    if article_date >= cutoff_date:
                        filtered_articles.append(article)
                        page_has_recent = True
                except ValueError:
                    # 日期格式解析失败，跳过
                    pass
        
        with lock:
            results.extend(filtered_articles)
        
        # 如果整页都没有符合日期条件的文章，说明后续页也不会有了
        if not page_has_recent and articles:
            stop_event.set()
            return False
        
        return True

    def get_recent_articles(
        self, 
        days: int = 5, 
        max_pages: int = 50,
        num_threads: int = 4
    ) -> List[Dict[str, str]]:
        """
        多线程获取最近 N 天内发布的文章
        
        Args:
            days: 最近天数（默认 5 天）
            max_pages: 最大爬取页数（默认 50 页，避免无限爬取）
            num_threads: 线程数（默认 4）
            
        Returns:
            包含 title, link, date 的文章列表，按日期降序排列
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        cutoff_str = cutoff_date.strftime("%Y-%m-%d")
        
        print(f"🔍 开始获取最近 {days} 天的文章（{cutoff_str} 之后）")
        print(f"   使用 {num_threads} 个线程，最大爬取 {max_pages} 页")
        
        results: List[Dict] = []
        lock = threading.Lock()
        stop_event = threading.Event()
        
        # 使用线程池并发获取
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            # 分批提交任务，每批 num_threads 个页面
            page = 1
            while page <= max_pages and not stop_event.is_set():
                # 提交一批任务
                futures = {}
                for i in range(num_threads):
                    current_page = page + i
                    if current_page > max_pages:
                        break
                    future = executor.submit(
                        self._fetch_page_worker,
                        current_page,
                        cutoff_date,
                        results,
                        lock,
                        stop_event
                    )
                    futures[future] = current_page
                
                # 等待这批任务完成
                for future in as_completed(futures):
                    page_num = futures[future]
                    try:
                        future.result()
                        print(f"   ✓ 第 {page_num} 页完成，当前共 {len(results)} 篇文章")
                    except Exception as e:
                        print(f"   ✗ 第 {page_num} 页出错: {e}")
                
                page += num_threads
                
                # 如果收到停止信号，退出循环
                if stop_event.is_set():
                    print("   📌 检测到旧文章，停止继续爬取")
                    break
        
        # 按日期降序排序
        results.sort(key=lambda x: x.get("date", ""), reverse=True)
        
        # 去重（基于链接）
        seen_links = set()
        unique_results = []
        for article in results:
            if article["link"] not in seen_links:
                seen_links.add(article["link"])
                unique_results.append(article)
        
        print(f"\n✅ 完成！找到 {len(unique_results)} 篇最近 {days} 天的文章\n")
        
        return unique_results

    def print_recent_articles(
        self,
        days: int = 5,
        max_pages: int = 50,
        num_threads: int = 4
    ) -> List[Dict[str, str]]:
        """
        获取并打印最近 N 天的文章列表
        
        Args:
            days: 最近天数（默认 5 天）
            max_pages: 最大爬取页数（默认 50 页）
            num_threads: 线程数（默认 4）
            
        Returns:
            文章列表
        """
        articles = self.get_recent_articles(days, max_pages, num_threads)
        
        if not articles:
            print("😕 没有找到符合条件的文章")
            return []
        
        print("=" * 80)
        print(f"📰 最近 {days} 天的文章列表（共 {len(articles)} 篇）")
        print("=" * 80)
        
        for i, article in enumerate(articles, 1):
            print(f"\n{i}. [{article['date']}] {article['title']}")
            print(f"   🔗 {article['link']}")
        
        print("\n" + "=" * 80)
        
        return articles

    def _ai_process_worker(
        self, 
        article: Dict[str, str], 
        results: List[Dict], 
        lock: threading.Lock,
        index: int,
        total: int
    ) -> Optional[Dict]:
        """
        AI 处理工作线程：爬取单篇文章并用 AI 提取结构化数据
        
        Args:
            article: 文章信息（包含 title, link, date）
            results: 共享结果列表
            lock: 线程锁
            index: 当前索引
            total: 总数
        """
        url = article["link"]
        title = article["title"]
        
        print(f"   [{index}/{total}] 🤖 正在处理: {title[:40]}...")
        
        try:
            html = self._request(url)
            if not html:
                print(f"   [{index}/{total}] ❌ 获取失败: {title[:30]}...")
                return None
            
            # 保存原始 HTML 页面
            filename = url.split("/")[-1].replace(".html", "")
            filename = sanitize_filename(filename) or "article"
            save_to_html(html, filename, OUTPUT_CONFIG["html_dir"])
            
            # 调用 AI 提取结构化数据
            vps_info = extract_vps_info(html)
            
            if vps_info:
                vps_info["source_url"] = url
                vps_info["publish_date"] = article.get("date", "")
                
                # 保存 JSON
                save_to_json(vps_info, filename, OUTPUT_CONFIG["raw_dir"])
                
                with lock:
                    results.append(vps_info)
                
                vendor = vps_info.get("vendor", "未知")
                print(f"   [{index}/{total}] ✅ 完成: {vendor} - {title[:30]}...")
                return vps_info
            else:
                print(f"   [{index}/{total}] ⚠️ AI 提取失败: {title[:30]}...")
                return None
                
        except Exception as e:
            print(f"   [{index}/{total}] ❌ 出错: {e}")
            return None

    def pipeline_recent_to_json(
        self,
        days: int = 5,
        scrape_threads: int = 4,
        ai_threads: int = 2,
        max_pages: int = 50
    ) -> List[Dict]:
        """
        Pipeline: 爬取最近文章并用 AI 总结为 JSON
        
        流程:
        1. 多线程爬取最近 N 天的文章列表（scrape_threads 个线程）
        2. 多线程调用 AI 处理每篇文章（ai_threads 个线程）
        3. 保存结构化数据到 JSON 文件
        
        Args:
            days: 最近天数（默认 5 天）
            scrape_threads: 爬取线程数（默认 4）
            ai_threads: AI 处理线程数（默认 2）
            max_pages: 最大爬取页数（默认 50）
            
        Returns:
            AI 提取的结构化数据列表
        """
        print("=" * 80)
        print("🚀 Pipeline: 爬取最近文章 → AI 提取 → 保存 JSON")
        print("=" * 80)
        print(f"   日期范围: 最近 {days} 天")
        print(f"   爬取线程: {scrape_threads}")
        print(f"   AI 线程: {ai_threads}")
        print("=" * 80)
        print()
        
        # 第一步：多线程获取最近文章列表
        print("📋 第一步：获取最近文章列表")
        print("-" * 40)
        articles = self.get_recent_articles(
            days=days, 
            max_pages=max_pages, 
            num_threads=scrape_threads
        )
        
        if not articles:
            print("😕 没有找到符合条件的文章")
            return []
        
        print(f"\n📰 共找到 {len(articles)} 篇文章待处理")
        print()
        
        # 第二步：多线程 AI 处理
        print("🤖 第二步：AI 提取结构化数据")
        print("-" * 40)
        
        results: List[Dict] = []
        lock = threading.Lock()
        total = len(articles)
        
        with ThreadPoolExecutor(max_workers=ai_threads) as executor:
            futures = {}
            for i, article in enumerate(articles, 1):
                future = executor.submit(
                    self._ai_process_worker,
                    article,
                    results,
                    lock,
                    i,
                    total
                )
                futures[future] = article
            
            # 等待所有任务完成
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    article = futures[future]
                    print(f"   ❌ 处理出错 [{article['title'][:30]}]: {e}")
        
        # 统计结果
        print()
        print("=" * 80)
        print(f"✅ Pipeline 完成！")
        print(f"   文章总数: {total}")
        print(f"   成功处理: {len(results)}")
        print(f"   失败数量: {total - len(results)}")
        print(f"   输出目录: {OUTPUT_CONFIG['raw_dir']}")
        print("=" * 80)
        
        return results

