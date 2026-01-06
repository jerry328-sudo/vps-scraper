"""
智谱 AI 大模型 API 客户端
用于调用智谱 AI 进行结构化数据提取
"""
import json
import os
import sys
from typing import Optional

from zai import ZhipuAiClient
from bs4 import BeautifulSoup

# 确保项目根目录在 Python 路径中
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config import API_KEYS, AI_CONFIG


# 单个 VPS 产品的 Schema 定义
VPS_PRODUCT_SCHEMA = {
    "type": "object",
    "properties": {
        "vendor": {"type": "string", "description": "VPS 商家名称"},
        "product_name": {"type": "string", "description": "产品名称"},
        "location": {"type": "string", "description": "机房位置"},
        "plans": {
            "type": "array",
            "description": "套餐列表",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "套餐名称"},
                    "cpu": {
                        "type": "object",
                        "properties": {
                            "cores": {"type": "number", "description": "核心数"},
                            "model": {"type": "string", "description": "型号"}
                        }
                    },
                    "memory": {
                        "type": "object",
                        "properties": {
                            "value": {"type": "number", "description": "数值"},
                            "unit": {"type": "string", "description": "单位（MB/GB）"}
                        }
                    },
                    "storage": {
                        "type": "object",
                        "properties": {
                            "value": {"type": "number", "description": "数值"},
                            "unit": {"type": "string", "description": "单位（GB/TB）"},
                            "type": {"type": "string", "description": "类型（SSD/HDD/NVMe）"}
                        }
                    },
                    "bandwidth": {
                        "type": "object",
                        "properties": {
                            "value": {"type": "number", "description": "数值"},
                            "unit": {"type": "string", "description": "单位（Mbps/Gbps）"}
                        }
                    },
                    "traffic": {
                        "type": "object",
                        "properties": {
                            "value": {"type": "number", "description": "数值，无限流量则为 -1"},
                            "unit": {"type": "string", "description": "单位（GB/TB/无限）"}
                        }
                    },
                    "price": {
                        "type": "object",
                        "properties": {
                            "value": {"type": "number", "description": "数值"},
                            "currency": {"type": "string", "description": "货币（CNY/USD）"},
                            "period": {"type": "string", "description": "周期（月/年）"}
                        }
                    }
                }
            }
        },
        "purchase_url": {"type": "string", "description": "购买链接"},
        "coupon_code": {"type": "string", "description": "优惠码"},
        "payment_methods": {
            "type": "array", 
            "items": {"type": "string"}, 
            "description": "支持的支付方式"
        },
        "features": {
            "type": "array", 
            "items": {"type": "string"}, 
            "description": "产品特点/优势"
        },
        "suitable_for": {
            "type": "array", 
            "items": {"type": "string"}, 
            "description": "适用场景"
        },
        "summary": {"type": "string", "description": "产品总结"}
    },
    "required": ["vendor", "product_name", "plans"]
}

# VPS 测评文章结构化数据的 JSON Schema（支持多个供应商）
VPS_ARTICLE_SCHEMA = {
    "type": "object",
    "properties": {
        "products": {
            "type": "array",
            "description": "文章中包含的所有 VPS 产品列表（一篇测评可能包含多个供应商/产品）",
            "items": VPS_PRODUCT_SCHEMA
        },
        "article_title": {"type": "string", "description": "文章标题"},
        "article_summary": {"type": "string", "description": "文章总结"}
    },
    "required": ["products"]
}


def html_to_text(html_content: str) -> str:
    """
    将 HTML 转换为纯文本，解决 HTML 实体编码问题
    保留表格结构以便 AI 识别
    """
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


def extract_vps_info(html_content: str, model: Optional[str] = None) -> Optional[dict]:
    """
    使用智谱 AI 从 HTML 内容中提取 VPS 结构化信息
    
    Args:
        html_content: 网页的 HTML 内容
        model: 使用的模型名称，默认使用配置中的值
        
    Returns:
        提取的结构化数据字典，失败返回 None
    """
    # 获取 API Key
    api_key = API_KEYS.get("zhipu", "")
    if not api_key:
        print("❌ 未配置智谱 AI API Key，请设置环境变量 ZHIPU_API_KEY")
        return None
    
    # 获取模型配置
    zhipu_config = AI_CONFIG.get("zhipu", {})
    if model is None:
        model = zhipu_config.get("default_model", "glm-4.7")
    
    # 先将 HTML 转换为纯文本
    text_content = html_to_text(html_content)
    print(f"📝 提取文本长度: {len(text_content)} 字符")
    
    client = ZhipuAiClient(api_key=api_key)
    
    system_prompt = f"""你是一名专业的 VPS 测评数据分析师。请从用户提供的文章内容中提取 VPS 产品信息。

**重要说明**：
- 一篇测评文章可能包含【多个】VPS 供应商或产品，请**完整提取所有 VPS 产品信息**，不要遗漏任何一个
- 每个不同的供应商或不同的产品线应作为 products 数组中的独立元素
- 请确保提取的信息完整准确，包括所有套餐配置和价格

请严格按照以下 JSON Schema 格式返回结果：
{json.dumps(VPS_ARTICLE_SCHEMA, indent=2, ensure_ascii=False)}

注意事项：
1. 只返回 JSON 对象，不要包含任何其他文字
2. 如果某个字段在文章中找不到，设为 null 或空数组
3. 购买链接请提取实际的 URL
4. 套餐信息要完整提取（CPU、内存、硬盘、带宽、流量、价格等）
5. 如果文章涉及多个供应商，每个供应商单独作为一个 product 对象"""

    user_prompt = f"""请从以下 VPS 测评文章中提取结构化信息：

{text_content[:50000]}"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            max_tokens=zhipu_config.get("max_tokens", 4096),
            temperature=zhipu_config.get("temperature", 0.1),
            top_p=0.95,
            thinking={"type": "disabled"}
        )
        
        content = response.choices[0].message.content
        result = json.loads(content)
        return result
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失败: {e}")
        return None
    except Exception as e:
        print(f"❌ API 调用失败: {e}")
        return None


if __name__ == "__main__":
    # 测试用例
    test_html = "<html><body><h1>测试 VPS</h1></body></html>"
    result = extract_vps_info(test_html)
    print(json.dumps(result, indent=2, ensure_ascii=False))
