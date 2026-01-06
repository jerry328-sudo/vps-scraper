"""
NVIDIA API 客户端
用于调用 NVIDIA 托管的 DeepSeek-R1 等模型
"""
import os
import sys
import time
from typing import Optional, Generator, Dict, Any

from openai import OpenAI

# 确保项目根目录在 Python 路径中
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config import API_KEYS, AI_CONFIG


class NvidiaClient:
    """
    NVIDIA API 客户端封装
    支持流式输出和思考过程展示
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化客户端
        
        Args:
            api_key: API Key，默认从配置读取
        """
        self.api_key = api_key or API_KEYS.get("nvidia", "")
        if not self.api_key:
            raise ValueError("未配置 NVIDIA API Key，请设置环境变量 NVIDIA_API_KEY")
        
        nvidia_config = AI_CONFIG.get("nvidia", {})
        self.base_url = nvidia_config.get("base_url", "https://integrate.api.nvidia.com/v1")
        self.default_model = nvidia_config.get("default_model", "deepseek-ai/deepseek-r1")
        
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )
    
    def chat_stream(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 1,
        max_tokens: int = 65536,
        show_reasoning: bool = True
    ) -> Generator[Dict[str, Any], None, None]:
        """
        流式对话，支持展示思考过程
        
        Args:
            prompt: 用户提问
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大输出 token 数
            show_reasoning: 是否返回思考过程
            
        Yields:
            包含内容和类型的字典
        """
        if model is None:
            model = self.default_model
        
        stream = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            top_p=0.95,
            max_tokens=max_tokens,
            stream=True,
            stream_options={"include_usage": True}
        )
        
        for chunk in stream:
            if chunk.usage is not None:
                yield {"type": "usage", "data": chunk.usage}
            
            if chunk.choices and chunk.choices[0].delta:
                delta = chunk.choices[0].delta
                
                # 思考内容
                reasoning_content = getattr(delta, "reasoning_content", None)
                if reasoning_content and show_reasoning:
                    yield {"type": "reasoning", "content": reasoning_content}
                
                # 正式回复
                if delta.content:
                    yield {"type": "content", "content": delta.content}
    
    def chat(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 1,
        max_tokens: int = 65536,
        verbose: bool = True
    ) -> str:
        """
        非流式对话，带统计信息
        
        Args:
            prompt: 用户提问
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大输出 token 数
            verbose: 是否打印过程信息
            
        Returns:
            模型回复内容
        """
        start_time = time.time()
        first_token_time = None
        
        reasoning_parts = []
        content_parts = []
        usage_info = None
        
        is_reasoning = True
        
        if verbose:
            print("=" * 50)
            print("思考过程：")
            print("=" * 50)
        
        for chunk in self.chat_stream(prompt, model, temperature, max_tokens):
            if chunk["type"] == "usage":
                usage_info = chunk["data"]
            
            elif chunk["type"] == "reasoning":
                if first_token_time is None:
                    first_token_time = time.time()
                reasoning_parts.append(chunk["content"])
                if verbose:
                    print(chunk["content"], end="", flush=True)
            
            elif chunk["type"] == "content":
                if first_token_time is None:
                    first_token_time = time.time()
                if is_reasoning and verbose:
                    print("\n")
                    print("=" * 50)
                    print("正式回复：")
                    print("=" * 50)
                    is_reasoning = False
                content_parts.append(chunk["content"])
                if verbose:
                    print(chunk["content"], end="", flush=True)
        
        end_time = time.time()
        
        if verbose:
            self._print_stats(
                usage_info, 
                start_time, 
                end_time, 
                first_token_time
            )
        
        return "".join(content_parts)
    
    def _print_stats(
        self,
        usage_info,
        start_time: float,
        end_time: float,
        first_token_time: Optional[float]
    ) -> None:
        """打印统计信息"""
        total_time = end_time - start_time
        ttft = first_token_time - start_time if first_token_time else 0
        generation_time = end_time - first_token_time if first_token_time else 0
        
        print()
        print()
        print("=" * 50)
        print("Token 统计：")
        print("=" * 50)
        
        if usage_info:
            prompt_tokens = usage_info.prompt_tokens
            completion_tokens = usage_info.completion_tokens
            total_tokens = usage_info.total_tokens
            reasoning_tokens = getattr(usage_info, 'reasoning_tokens', 0) or 0
            
            print(f"输入 Tokens: {prompt_tokens}")
            print(f"输出 Tokens: {completion_tokens}")
            print(f"思考 Tokens: {reasoning_tokens}")
            print(f"总 Tokens: {total_tokens}")
            print(f"首 Token 延迟 (TTFT): {ttft:.2f} 秒")
            print(f"生成总时间: {total_time:.2f} 秒")
            if generation_time > 0:
                print(f"生成速度: {completion_tokens / generation_time:.2f} tokens/秒")
        else:
            print("API 未返回 usage 信息")
            print(f"首 Token 延迟 (TTFT): {ttft:.2f} 秒")
            print(f"生成总时间: {total_time:.2f} 秒")


if __name__ == "__main__":
    # 测试用例
    client = NvidiaClient()
    response = client.chat("是鸡生蛋还是蛋生鸡？")
    print(f"\n最终回复: {response[:100]}...")
