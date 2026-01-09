# 测试文档

## 测试概览

本项目使用精简的测试策略，只有一个测试文件：

- **`tests/test_scraper.py`** - 爬虫完整流程测试

**设计理念**：测试两种爬取方式都能获取内容后，只用 AI 跑一次提取，减少 API 消耗。

## 测试用例说明

| 测试 | 说明 | API 消耗 |
|------|------|----------|
| `test_1_scraper_initialization` | 验证爬虫初始化和必需方法 | 无 |
| `test_2_standard_scrape` | 标准爬取方式（requests） | 无 |
| `test_3_tavily_scrape` | Tavily 爬取方式（可选） | Tavily 1次 |
| `test_4_ai_extraction` | AI 提取（复用已爬内容） | 智谱 1次 |

**测试 URL：** `https://www.gwvpsceping.com/8810.html`

## 运行方式

```bash
# 运行所有测试
uv run python -m unittest tests.test_scraper -v

# 只运行不消耗 API 的基础测试
uv run python -m unittest tests.test_scraper.TestScraper.test_1_scraper_initialization -v
uv run python -m unittest tests.test_scraper.TestScraper.test_2_standard_scrape -v
```

## 前置条件

### 必需配置
- **ZHIPU_API_KEY** - 智谱 AI API Key（用于 AI 提取测试）

### 可选配置
- **TAVILY_API_KEY** - Tavily API Key（用于 Tavily 爬取测试，未配置则跳过）

### 配置方式

1. **通过 .env 文件：**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，填入真实的 API Key
   ```

2. **通过系统环境变量：**
   ```powershell
   # Windows PowerShell
   $env:ZHIPU_API_KEY="your_key_here"
   $env:TAVILY_API_KEY="your_key_here"
   ```
   ```bash
   # Linux/Mac
   export ZHIPU_API_KEY="your_key_here"
   export TAVILY_API_KEY="your_key_here"
   ```

## 测试覆盖的功能

- ✅ 爬虫初始化（use_tavily 参数）
- ✅ 必需方法存在性检查
- ✅ 标准爬取（requests + BeautifulSoup）
- ✅ Tavily API 爬取
- ✅ AI 结构化数据提取
- ✅ API Key 读取（如果 AI 提取成功，说明 Key 配置正确）

## 测试架构

```
tests/
├── __init__.py         # 测试包初始化
├── README.md           # 本文档
└── test_scraper.py     # 爬虫测试
```

## 持续集成

GitHub Actions 工作流配置：

```yaml
# .github/workflows/test.yml
- name: Run scraper tests
  env:
    ZHIPU_API_KEY: ${{ secrets.ZHIPU_API_KEY }}
    TAVILY_API_KEY: ${{ secrets.TAVILY_API_KEY }}
  run: uv run python -m unittest tests.test_scraper -v
```

## 注意事项

1. **网络连接**：测试需要访问外部网站，确保网络连接正常
2. **API 消耗**：完整测试只调用 1 次智谱 API + 1 次 Tavily API
3. **测试时间**：完整测试约 10-20 秒
4. **跳过机制**：未配置 API Key 的测试会自动跳过（skipTest）
