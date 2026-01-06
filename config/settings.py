"""
全局配置模块
集中管理站点 URL、API 密钥、请求参数等配置
"""
import os
from pathlib import Path
from typing import Dict, Any

from dotenv import load_dotenv

# 加载项目根目录下的 .env 文件
_project_root = Path(__file__).parent.parent
load_dotenv(_project_root / ".env")

# ============================================================
# API 配置（优先从环境变量读取，保证安全性）
# ============================================================

API_KEYS = {
    # 智谱 AI API Key
    "zhipu": os.getenv("ZHIPU_API_KEY", ""),
    # NVIDIA API Key
    "nvidia": os.getenv("NVIDIA_API_KEY", ""),
}

# ============================================================
# 目标站点配置
# ============================================================

TARGET_SITES: Dict[str, Dict[str, Any]] = {
    "gwvps": {
        "name": "狗汪 VPS 测评网",
        "base_url": "https://www.gwvpsceping.com",
        "encoding": "utf-8",
        "selectors": {
            "article_title": "h1.article-title, h1",
            "article_content": "article.article-content, div.entry-content",
            "article_list": "h2 > a",
        },
    },
}

# ============================================================
# HTTP 请求配置
# ============================================================

REQUEST_CONFIG: Dict[str, Any] = {
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "timeout": 30,
    "request_delay": 1.0,  # 请求间隔（秒）
}

# ============================================================
# 爬取配置
# ============================================================

SCRAPE_CONFIG: Dict[str, Any] = {
    "default_pages": 1,  # 默认爬取页数
    "max_filename_length": 50,  # 文件名最大长度
}

# ============================================================
# AI 模型配置
# ============================================================

AI_CONFIG: Dict[str, Dict[str, Any]] = {
    "zhipu": {
        "default_model": "glm-4.7",
        "max_tokens": 65536,
        "temperature": 0.7,
    },
    "nvidia": {
        "base_url": "https://integrate.api.nvidia.com/v1",
        "default_model": "deepseek-ai/deepseek-r1",
        "max_tokens": 65536,
        "temperature": 1,
    },
}

# ============================================================
# 输出目录配置
# ============================================================

OUTPUT_CONFIG: Dict[str, str] = {
    "base_dir": "data",
    "articles_dir": "data/articles",  # Markdown 文章输出
    "raw_dir": "data/raw",  # 原始 JSON 数据输出
    "html_dir": "data/html",  # 原始 HTML 页面输出
}
