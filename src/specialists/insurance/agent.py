"""Insurance Specialist Agent - 保险顾问专家."""
from qwen_agent.agents import Assistant

from .tools import (
    ESTextRetrievalTool,
    ESVectorRetrievalTool,
    ESHybridRetrievalTool,
    TextEmbeddingTool,
)
from ...tools.config import get_settings


class InsuranceAgent(Assistant):
    """Specialist agent for insurance advisory."""
    NAME = "insurance"
    DESCRIPTION = "保险顾问专家，基于ES检索查询保险条款"
    SYSTEM_MESSAGE = """你是一个专业的保险顾问专家。你可以查询保险条款、保单信息、计算保单贷款金额。

支持5种检索模式：
- 文本检索：基于关键词的ES文本检索（BM25）
- 向量检索：基于语义向量的ES检索（RAG）
- 混合检索：文本+向量混合检索（最佳效果）
- 文本Embedding：生成文本向量表示

当用户询问保险条款时，优先使用ES检索工具获取相关内容。"""

    def __init__(self, session_id: str, **kwargs):
        settings = get_settings()
        super().__init__(
            llm={'model': settings.model_name, 'model_type': settings.model_type},
            system_message=self.SYSTEM_MESSAGE,
            function_list=[
                ESTextRetrievalTool(),
                ESVectorRetrievalTool(),
                ESHybridRetrievalTool(),
                TextEmbeddingTool(),
            ],
            name=self.NAME,
            description=self.DESCRIPTION,
            **kwargs
        )
