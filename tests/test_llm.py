"""Tests for LLM module."""
import pytest
from unittest.mock import patch, MagicMock


def test_llm_config():
    """Test LLM configuration."""
    from src.tools.llm import LLMConfig

    config = LLMConfig(
        model="qwen-turbo",
        temperature=0.7,
        max_tokens=2000
    )
    assert config.model == "qwen-turbo"
    assert config.temperature == 0.7
    assert config.max_tokens == 2000


def test_llm_config_defaults():
    """Test LLM configuration defaults."""
    from src.tools.llm import LLMConfig

    config = LLMConfig()
    assert config.model == "qwen-turbo-2025-04-28"
    assert config.temperature == 0.7
    assert config.max_tokens == 2000


def test_llm_initialization():
    """Test LLM initialization."""
    with patch('dashscope.api_key', None):
        from src.tools.llm import DashScopeLLM

        llm = DashScopeLLM(api_key="test-key")
        assert llm.api_key == "test-key"
        assert llm.config.model == "qwen-turbo-2025-04-28"


def test_llm_structured_output_parsing():
    """Test structured output parsing."""
    from src.tools.llm import DashScopeLLM

    llm = DashScopeLLM(api_key="test-key")

    # Mock the chat method to return JSON
    with patch.object(llm, 'chat', return_value='{"stock": "茅台", "price": 1440}'):
        result = llm.structured_output("test prompt", {"stock": str, "price": int})
        assert result["stock"] == "茅台"
        assert result["price"] == 1440


def test_llm_structured_output_fallback():
    """Test structured output fallback on parse error."""
    from src.tools.llm import DashScopeLLM

    llm = DashScopeLLM(api_key="test-key")

    with patch.object(llm, 'chat', return_value='This is not JSON'):
        result = llm.structured_output("test prompt", {})
        assert "raw" in result
        assert result["raw"] == "This is not JSON"