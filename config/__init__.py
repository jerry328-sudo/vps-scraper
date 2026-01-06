"""
配置模块入口
导出所有配置常量供其他模块使用
"""

from .settings import (
    API_KEYS,
    TARGET_SITES,
    REQUEST_CONFIG,
    SCRAPE_CONFIG,
    AI_CONFIG,
    OUTPUT_CONFIG,
)

__all__ = [
    "API_KEYS",
    "TARGET_SITES",
    "REQUEST_CONFIG",
    "SCRAPE_CONFIG",
    "AI_CONFIG",
    "OUTPUT_CONFIG",
]
