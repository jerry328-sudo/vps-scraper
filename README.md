# VPS 测评文章爬虫

爬取 [狗汪 VPS 测评网](https://www.gwvpsceping.com/) 的 VPS 测评文章，并使用 AI 大模型提取结构化数据。

## 功能特点

- 🕷️ **多模式爬取**：支持列表页批量爬取和单篇文章爬取
- 🤖 **AI 结构化提取**：使用智谱 AI 自动提取 VPS 配置、价格等结构化信息
- 📄 **多格式输出**：支持 JSON（结构化数据）和 Markdown（原始内容）两种格式
- 🔌 **可扩展架构**：基于抽象基类，易于扩展支持更多站点

## 项目结构

```
vps-scraper/
├── main.py              # CLI 入口，解析命令行参数
├── config/              # 全局配置模块
│   ├── __init__.py
│   └── settings.py      # 站点 URL、API Key、请求参数配置
├── src/
│   ├── scrapers/        # 爬虫实现
│   │   ├── base.py      # BaseScraper 抽象基类
│   │   └── gwvps_scraper.py  # 狗汪 VPS 站点爬虫
│   ├── ai_clients/      # AI API 客户端
│   │   ├── zhipu_client.py   # 智谱 AI 客户端
│   │   └── nvidia_client.py  # NVIDIA API 客户端
│   └── utils/           # 工具函数
│       └── file_utils.py     # 文件名清理、保存功能
├── data/
│   ├── articles/        # Markdown 格式输出
│   └── raw/             # JSON 结构化数据输出
├── .env.example         # 环境变量示例
└── pyproject.toml       # 项目配置和依赖
```

## 快速开始

### 1. 安装依赖

```bash
# 使用 uv 包管理器
uv pip install -r pyproject.toml
```

### 2. 配置 API Key

```bash
# 复制环境变量示例文件
cp .env.example .env

# 编辑 .env 填入 API Key
# ZHIPU_API_KEY=your_zhipu_api_key
# NVIDIA_API_KEY=your_nvidia_api_key
```

### 3. 运行爬虫

```bash
# 爬取默认 1 页，输出 JSON
uv run python main.py

# 爬取 3 页
uv run python main.py -p 3

# 爬取单篇文章
uv run python main.py -u https://www.gwvpsceping.com/8785.html

# 输出为 Markdown 格式
uv run python main.py -f markdown

# 查看帮助
uv run python main.py --help
```

## CLI 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-p, --pages` | 爬取页数 | 1 |
| `-s, --site` | 目标站点 | gwvps |
| `-u, --url` | 单篇文章 URL | - |
| `-f, --format` | 输出格式 (json/markdown) | json |

## 扩展新站点

1. 在 `config/settings.py` 中添加站点配置
2. 创建 `src/scrapers/newsite_scraper.py`，继承 `BaseScraper`
3. 实现 `get_article_list()`、`scrape_article()`、`run()` 方法
4. 在 `main.py` 的 `get_scraper()` 中注册新爬虫

## 许可证

MIT License