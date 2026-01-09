# 页面提取方式使用指南

## 概览

`GWVPSScraper` 现在支持两种页面内容提取方式：

1. **标准爬虫方式**（默认）- 使用 `requests` + `html_to_text`
2. **Tavily API 方式** - 使用 Tavily 的智能提取 API

## 配置

### 环境变量

在 `.env` 文件中添加 Tavily API Key（可选）：

```env
# 标准配置
ZHIPU_API_KEY=your_zhipu_api_key

# 如果要使用 Tavily 提取方式，添加此配置
TAVILY_API_KEY=your_tavily_api_key
```

## 使用方法

### 方式 1: 标准爬虫（默认）

```python
from src.scrapers.gwvps_scraper import GWVPSScraper

# 使用标准爬虫方式
scraper = GWVPSScraper(use_tavily=False)  # 或直接 GWVPSScraper()

# 爬取单篇文章
result = scraper.scrape_with_ai("https://www.gwvpsceping.com/8810.html")
```

**特点：**
- ✅ 不需要额外的 API Key
- ✅ 完全控制爬取过程
- ✅ 保存原始 HTML 文件
- ⚠️ 可能遇到反爬虫限制

### 方式 2: Tavily API 提取

```python
from src.scrapers.gwvps_scraper import GWVPSScraper

# 使用 Tavily API 提取方式
scraper = GWVPSScraper(use_tavily=True)

# 爬取单篇文章
result = scraper.scrape_with_ai("https://www.gwvpsceping.com/8810.html")
```

**特点：**
- ✅ 智能内容提取，质量更高
- ✅ 更好的反爬虫处理
- ✅ 自动 fallback 到标准方式（如果失败）
- ⚠️ 需要 Tavily API Key（付费服务）

## 完整示例

### 示例 1: 爬取最近文章（标准方式）

```python
from src.scrapers.gwvps_scraper import GWVPSScraper

# 初始化：标准爬虫
scraper = GWVPSScraper(use_tavily=False)

# 爬取最近 5 天的文章并用 AI 提取
results = scraper.pipeline_recent_to_json(
    days=5,
    scrape_threads=4,  # 爬取文章列表用 4 个线程
    ai_threads=2,      # AI 处理用 2 个线程
    max_pages=50
)

print(f"成功提取 {len(results)} 篇文章")
```

### 示例 2: 爬取最近文章（Tavily 方式）

```python
from src.scrapers.gwvps_scraper import GWVPSScraper

# 初始化：Tavily API 提取
scraper = GWVPSScraper(use_tavily=True)

# 爬取最近 3 天的文章
results = scraper.pipeline_recent_to_json(
    days=3,
    scrape_threads=4,
    ai_threads=2,
    max_pages=30
)

print(f"成功提取 {len(results)} 篇文章")
```

### 示例 3: 单篇文章对比测试

```python
from src.scrapers.gwvps_scraper import GWVPSScraper

url = "https://www.gwvpsceping.com/8810.html"

# 标准方式
print("=" * 80)
print("使用标准爬虫方式")
print("=" * 80)
scraper_standard = GWVPSScraper(use_tavily=False)
result_standard = scraper_standard.scrape_with_ai(url)

# Tavily 方式
print("\n" + "=" * 80)
print("使用 Tavily API 方式")
print("=" * 80)
scraper_tavily = GWVPSScraper(use_tavily=True)
result_tavily = scraper_tavily.scrape_with_ai(url)

# 对比结果
print("\n" + "=" * 80)
print("结果对比")
print("=" * 80)
print(f"标准方式提取: {result_standard is not None}")
print(f"Tavily 方式提取: {result_tavily is not None}")
```

## 自动 Fallback 机制

当使用 `use_tavily=True` 时，如果 Tavily API 提取失败，会自动回退到标准爬虫方式：

```
📡 正在爬取: https://www.gwvpsceping.com/8810.html
📡 使用 Tavily API 提取页面: https://...
⚠️  Tavily API 返回结果为空
⚠️  Tavily 提取失败，尝试使用标准爬虫方式...
✅ HTML 获取成功，长度: 45678 字符
📝 正在将 HTML 转换为纯文本...
   提取文本长度: 12345 字符
🤖 正在调用大模型提取结构化数据...
```

## 性能对比

| 指标 | 标准爬虫 | Tavily API |
|------|---------|-----------|
| 提取质量 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 速度 | 快 | 中等 |
| 成本 | 免费 | 付费 |
| 反爬虫能力 | 低 | 高 |
| 可靠性 | 依赖网站结构 | 高 |

## 建议

- **开发测试阶段**：使用标准爬虫（`use_tavily=False`）
- **生产环境/大规模爬取**：使用 Tavily API（`use_tavily=True`）
- **个人项目**：标准爬虫即可满足需求
