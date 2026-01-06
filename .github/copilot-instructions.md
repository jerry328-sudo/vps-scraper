# VPS 测评文章爬虫 - AI 编码指南

## 项目概述

这是一个针对 [狗汪 VPS 测评网](https://www.gwvpsceping.com/) 的爬虫项目，使用 `requests` + `BeautifulSoup` 爬取 VPS 测评文章并保存为 Markdown 格式。

## 架构说明

```
main.py          → CLI 入口，解析命令行参数
config/          → 全局配置（站点 URL、请求头、爬取参数）
src/scrapers/    → 爬虫实现（继承 BaseScraper 抽象基类）
src/utils/       → 工具函数（文件名清理、Markdown 保存）
data/articles/   → 输出目录，存放爬取的 .md 文件
```

**数据流**: `main.py` → `GWVPSScraper.run()` → 逐页获取文章列表 → 逐篇爬取内容 → `save_article_to_markdown()` 保存

## 强制约定（来自 [docs/GEMINI.md](docs/GEMINI.md)）

- **中文优先**: 所有代码注释、文档、commit message 必须使用中文
- **KISS 原则**: 拒绝过度工程化，保持简洁可读
- **前置调研**: 修改前先理解现有代码，禁止盲目实现

## 开发命令

```bash
# 安装依赖（使用 uv 包管理器）
uv pip install -r requirements.txt

# 运行爬虫（默认 1 页）
uv run python main.py

# 指定页数
uv run python main.py -p 3
```

## 核心模式与约定

### 1. 添加新爬虫（多站点扩展）
继承 `BaseScraper` 并实现三个抽象方法：
```python
# 参考 src/scrapers/gwvps_scraper.py
class NewSiteScraper(BaseScraper):
    def get_article_list(self, page: int) -> List[Dict]:  # 返回 {'title': ..., 'link': ...}
    def scrape_article(self, url: str) -> Optional[Dict]:  # 返回 {'title': ..., 'content': ..., 'url': ...}
    def run(self, max_pages: int) -> None:  # 主循环
```

**扩展新站点步骤**：
1. 在 `config/settings.py` 中添加新站点配置（仿照 `TARGET_SITE` 结构）
2. 在 `src/scrapers/` 下创建 `newsite_scraper.py`，继承 `BaseScraper`
3. 在 `src/scrapers/__init__.py` 中导出新爬虫类
4. 根据需要在 `main.py` 添加 CLI 参数选择站点

### 2. 配置管理
所有配置集中在 [config/settings.py](config/settings.py)，通过 `config/__init__.py` 导出：
- `TARGET_SITE`: 目标站点 base_url、编码
- `REQUEST_CONFIG`: User-Agent、超时、请求间隔
- `SCRAPE_CONFIG`: 默认页数、文件名长度限制

### 3. 文件名处理
使用 `sanitize_filename()` 清理 Windows 非法字符 `\/*?:"<>|`，自动截断到 50 字符

### 4. 请求规范
- 必须设置 User-Agent（否则返回 403）
- 使用 `response.apparent_encoding` 自动检测编码
- 请求间隔 1 秒（`REQUEST_CONFIG["request_delay"]`）

## 站点解析要点（来自 [docs/extraction_guide.md](docs/extraction_guide.md)）

| 元素 | 选择器 |
|------|--------|
| 文章标题 | `h1.article-title` 或 `h1` |
| 文章正文 | `article.article-content` 或 `div.entry-content` |
| 列表页链接 | `h2 > a` |

## 注意事项

- 输出文件保存到 `data/articles/`，格式固定为 `# 标题\n\nSource: URL\n\n正文`
- 项目通过 `sys.path.insert` 处理模块导入，避免相对导入问题
