"""
AI 客户端模块入口
导出所有 AI API 客户端
"""

from .zhipu_client import extract_vps_info, VPS_ARTICLE_SCHEMA
from .nvidia_client import NvidiaClient

__all__ = [
    "extract_vps_info",

    "VPS_ARTICLE_SCHEMA",
    "NvidiaClient",
]
