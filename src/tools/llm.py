"""LLM integration module - unified via config.py."""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from dataclasses import dataclass

import dashscope
from dashscope import Generation

from .config import get_settings


@dataclass
class LLMConfig:
    """LLM configuration."""
    temperature: float = 0.7
    max_tokens: int = 2000
    timeout: int = 30


class DashScopeLLM:
    """DashScope (Qwen) LLM wrapper."""

    def __init__(self, api_key: Optional[str] = None, config: Optional[LLMConfig] = None):
        settings = get_settings()
        self.api_key = api_key or settings.dashscope_api_key
        dashscope.api_key = self.api_key
        self.model_name = settings.model_name
        self.config = config or LLMConfig()

    def chat(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        tools: Optional[List[Dict]] = None,
        **kwargs
    ) -> str:
        """Send chat request to DashScope."""
        if system_prompt:
            full_messages = [{"role": "system", "content": system_prompt}] + messages
        else:
            full_messages = messages

        extra_params = {}
        if tools:
            extra_params["tools"] = tools

        response = Generation.call(
            model=self.model_name,
            messages=full_messages,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            result_format='message',
            **extra_params
        )

        if response.status_code == 200:
            return response.output.choices[0].message.content
        else:
            raise Exception(f"LLM call failed: {response.message}")

    def structured_output(
        self,
        prompt: str,
        output_schema: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Get structured JSON output from LLM."""
        messages = [{"role": "user", "content": prompt}]
        response = self.chat(messages)
        import json
        try:
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                response = response.split("```")[1].split("```")[0]
            return json.loads(response.strip())
        except json.JSONDecodeError:
            return {"raw": response}


# Global instance
_llm_instance: Optional[DashScopeLLM] = None


def get_llm() -> DashScopeLLM:
    """Get global LLM instance."""
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = DashScopeLLM()
    return _llm_instance


def set_llm(llm: DashScopeLLM):
    """Set global LLM instance (for testing)."""
    global _llm_instance
    _llm_instance = llm
