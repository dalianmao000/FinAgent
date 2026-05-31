"""Text Embedding 工具 - 使用 DashScope text-embedding 生成文本向量."""
import json
from typing import List, Optional

from qwen_agent.tools.base import BaseTool, register_tool


@register_tool('insurance_text_embedding')
class TextEmbeddingTool(BaseTool):
    """使用 DashScope text-embedding 模型生成文本向量"""
    name = 'insurance_text_embedding'
    description = '将文本转换为向量表示，用于语义相似度计算、检索增强生成(RAG)等场景'
    parameters = [{
        'name': 'texts',
        'type': 'array',
        'description': '要转换的文本列表',
        'required': True
    }, {
        'name': 'model',
        'type': 'string',
        'description': 'embedding模型名称，默认 text-embedding-v2',
        'required': False,
        'default': 'text-embedding-v2'
    }]

    def call(self, params: str, **kwargs) -> str:
        args = json.loads(params) if isinstance(params, str) else params
        texts = args['texts']
        model = args.get('model', 'text-embedding-v2')

        if isinstance(texts, str):
            texts = [texts]

        from ....tools.config import get_settings
        settings = get_settings()

        try:
            import dashscope
            from dashscope import TextEmbedding

            dashscope.api_key = settings.dashscope_api_key

            if not settings.dashscope_api_key:
                return "错误: 未配置 DASHSCOPE_API_KEY"

            results = []
            for text in texts:
                response = TextEmbedding.call(
                    model=model,
                    text=text
                )

                if response.status_code == 200:
                    embedding = response.output['embeddings'][0]['embedding']
                    results.append({
                        'text': text[:50] + '...' if len(text) > 50 else text,
                        'embedding_dim': len(embedding),
                        'embedding': embedding[:5] + ['...'] if len(embedding) > 5 else embedding
                    })
                else:
                    results.append({
                        'text': text[:50] + '...' if len(text) > 50 else text,
                        'error': response.message
                    })

            return json.dumps(results, ensure_ascii=False, indent=2)

        except Exception as e:
            return f"Text Embedding 出错: {str(e)}"
