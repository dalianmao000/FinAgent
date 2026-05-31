"""ES向量检索工具 - 基于Elasticsearch的向量检索."""
import json

from qwen_agent.tools.base import BaseTool, register_tool


@register_tool('insurance_es_vector_retrieval')
class ESVectorRetrievalTool(BaseTool):
    """基于Elasticsearch的向量检索工具"""
    name = 'insurance_es_vector_retrieval'
    description = '使用Elasticsearch向量检索，查询保险条款相关内容（需要先对文档进行向量化）'
    parameters = [{
        'name': 'query',
        'type': 'string',
        'description': '搜索查询词',
        'required': True
    }, {
        'name': 'size',
        'type': 'integer',
        'description': '返回结果数量，默认5',
        'required': False,
        'default': 5
    }]

    def call(self, params: str, **kwargs) -> str:
        args = json.loads(params) if isinstance(params, str) else params
        query = args['query']
        size = int(args.get('size', 5))

        from ....tools.config import get_settings
        settings = get_settings()

        try:
            from elasticsearch import Elasticsearch
            es = Elasticsearch(
                hosts=[{'host': settings.es_host, 'port': settings.es_port, 'scheme': 'http'}],
                basic_auth=(settings.es_username, settings.es_password),
                verify_certs=False,
                ssl_show_warn=False
            )

            # 获取查询文本的embedding
            import dashscope
            from dashscope import TextEmbedding
            dashscope.api_key = settings.dashscope_api_key

            embedding_response = TextEmbedding.call(
                model=TextEmbedding.Models.text_embedding_v4,
                input=query
            )

            if embedding_response.status_code != 200:
                return f"向量生成失败: {embedding_response.message}"

            query_vector = embedding_response.output['embeddings'][0]['embedding']

            # 向量搜索
            search_body = {
                "query": {
                    "knn": {
                        "field": "vector",
                        "query_vector": query_vector,
                        "k": size,
                        "boost": 0.0
                    }
                },
                "output_fields": ["title", "content", "filename"]
            }

            response = es.search(index=settings.es_index_name, body=search_body)
            hits = response['hits']['hits']

            if not hits:
                return f"未找到关于「{query}」的相关文档（向量检索模式）"

            results = [f"## 向量检索结果：{query}\n"]
            results.append(f"共找到 {len(hits)} 条相关文档\n")

            for i, hit in enumerate(hits, 1):
                score = hit['_score']
                source = hit['_source']

                results.append(f"### {i}. {source.get('title', '未知标题')}")
                results.append(f"**文件**: {source.get('filename', 'N/A')}")
                results.append(f"**相似度**: {score:.4f}")

                content = source.get('content', '')
                if content:
                    results.append(f"**内容预览**: {content[:300]}...")

                results.append("")

            return "\n".join(results)

        except Exception as e:
            return f"ES向量检索出错: {str(e)}"
