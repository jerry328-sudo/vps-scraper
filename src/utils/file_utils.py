"""
文件处理工具函数
包含文件名清理、保存等功能
"""
import os
import re
import json
from typing import Optional

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config import SCRAPE_CONFIG


def sanitize_filename(filename: str, max_length: Optional[int] = None) -> str:
    """
    清理文件名，移除 Windows 非法字符
    
    Args:
        filename: 原始文件名
        max_length: 最大长度，默认使用配置值
        
    Returns:
        清理后的安全文件名
    """
    if max_length is None:
        max_length = SCRAPE_CONFIG.get("max_filename_length", 50)
    
    # 移除 Windows 非法字符: \ / * ? : " < > |
    illegal_chars = r'[\\/*?:"<>|]'
    cleaned = re.sub(illegal_chars, "", filename)
    
    # 移除首尾空格和点
    cleaned = cleaned.strip(" .")
    
    # 替换连续空格为单个空格
    cleaned = re.sub(r"\s+", " ", cleaned)
    
    # 截断到最大长度
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length].rstrip()
    
    return cleaned


def ensure_dir(path: str) -> None:
    """确保目录存在，不存在则创建"""
    os.makedirs(path, exist_ok=True)


def save_to_json(data: dict, filename: str, output_dir: str) -> str:
    """
    保存数据为 JSON 文件
    
    Args:
        data: 要保存的数据
        filename: 文件名（不含扩展名）
        output_dir: 输出目录
        
    Returns:
        保存的文件完整路径
    """
    ensure_dir(output_dir)
    
    # 确保文件名安全
    safe_filename = sanitize_filename(filename)
    if not safe_filename:
        safe_filename = "data"
    
    filepath = os.path.join(output_dir, f"{safe_filename}.json")
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 已保存到: {filepath}")
    return filepath


def save_to_markdown(
    title: str,
    content: str,
    url: str,
    filename: str,
    output_dir: str
) -> str:
    """
    保存文章为 Markdown 文件
    
    Args:
        title: 文章标题
        content: 文章内容（HTML 或纯文本）
        url: 原文链接
        filename: 文件名（不含扩展名）
        output_dir: 输出目录
        
    Returns:
        保存的文件完整路径
    """
    from bs4 import BeautifulSoup
    
    ensure_dir(output_dir)
    
    # 确保文件名安全
    safe_filename = sanitize_filename(filename)
    if not safe_filename:
        safe_filename = "article"
    
    filepath = os.path.join(output_dir, f"{safe_filename}.md")
    
    # 如果内容是 HTML，转换为纯文本
    if content.strip().startswith("<"):
        soup = BeautifulSoup(content, "html.parser")
        content = soup.get_text(separator="\n\n", strip=True)
    
    # 组装 Markdown 内容
    md_content = f"# {title}\n\nSource: {url}\n\n{content}"
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(md_content)
    
    print(f"✅ 已保存到: {filepath}")
    return filepath


def save_to_html(
    html: str,
    filename: str,
    output_dir: str = "data/html"
) -> str:
    """
    保存原始 HTML 页面到文件
    
    Args:
        html: 原始 HTML 内容
        filename: 文件名（不含扩展名）
        output_dir: 输出目录
        
    Returns:
        保存的文件完整路径
    """
    ensure_dir(output_dir)
    
    # 确保文件名安全
    safe_filename = sanitize_filename(filename)
    if not safe_filename:
        safe_filename = "page"
    
    filepath = os.path.join(output_dir, f"{safe_filename}.html")
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    
    return filepath


def html_to_text(html_content: str) -> str:
    """
    将 HTML 转换为纯文本，解决 HTML 实体编码问题
    保留表格结构以便 AI 识别
    
    Args:
        html_content: 原始 HTML 内容
        
    Returns:
        提取的纯文本内容
    """
    from bs4 import BeautifulSoup
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 移除脚本和样式
    for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
        tag.decompose()
    
    # 提取文章主体内容
    article = soup.find('article') or soup.find('div', class_='entry-content') or soup
    
    lines = []
    for elem in article.find_all(['h1', 'h2', 'h3', 'p', 'li', 'td', 'th', 'blockquote']):
        text = elem.get_text(strip=True)
        if text:
            # 保留链接信息
            if elem.name in ['td', 'th']:
                link = elem.find('a')
                if link and link.get('href'):
                    lines.append(f"{text} [链接: {link.get('href')}]")
                else:
                    lines.append(text)
            else:
                lines.append(text)
    
    return '\n'.join(lines)
