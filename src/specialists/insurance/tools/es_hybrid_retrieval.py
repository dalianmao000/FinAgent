"""ES混合检索工具 - 结合文本检索和向量检索."""
import json

from qwen_agent.tools.base import BaseTool, register_tool


@register_tool('insurance_es_hybrid_retrieval')
class ESHybridRetrievalTool(BaseTool):
    """混合检索工具，结合文本检索和向量检索"""
    name = 'insurance_es_hybrid_retrieval'
    description = '使用混合检索（文本+向量）查询保险条款，获得最佳检索效果'
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

            # 文本检索
            text_search_body = {
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["title^2", "content"],
                        "type": "best_fields",
                        "fuzziness": "AUTO"
                    }
                },
                "size": size,
                "_source": ["title", "content", "filename"]
            }

            text_response = es.search(index=settings.es_index_name, body=text_search_body)
            text_hits = text_response['hits']['hits']

            # 向量检索
            import dashscope
            from dashscope import TextEmbedding
            dashscope.api_key = settings.dashscope_api_key

            embedding_response = TextEmbedding.call(
                model=TextEmbedding.Models.text_embedding_v4,
                input=query
            )

            if embedding_response.status_code == 200:
                query_vector = embedding_response.output['embeddings'][0]['embedding']

                vector_search_body = {
                    "query": {
                        "knn": {
                            "field": "vector",
                            "query_vector": query_vector,
                            "k": size,
                            "boost": 0.0
                        }
                    },
                    "size": size,
                    "_source": ["title", "content", "filename"]
                }

                vector_response = es.search(index=settings.es_index_name, body=vector_search_body)
                vector_hits = vector_response['hits']['hits']
            else:
                vector_hits = []

            # 合并结果，去重
            seen_ids = set()
            merged_results = []

            # 先添加文本检索结果
            for hit in text_hits:
                doc_id = hit['_id']
                if doc_id not in seen_ids:
                    seen_ids.add(doc_id)
                    merged_results.append({
                        'id': doc_id,
                        'source': hit['_source'],
                        'score': hit['_score'],
                        'mode': 'text'
                    })

            # 添加向量检索结果
            for hit in vector_hits:
                doc_id = hit['_id']
                if doc_id not in seen_ids:
                    seen_ids.add(doc_id)
                    merged_results.append({
                        'id': doc_id,
                        'source': hit['_source'],
                        'score': hit['_score'],
                        'mode': 'vector'
                    })

            if not merged_results:
                return f"未找到关于「{query}」的相关文档"

            results = [f"## 混合检索结果：{query}\n"]
            results.append(f"共找到 {len(merged_results)} 条相关文档（文本+向量）\n")

            for i, item in enumerate(merged_results[:size], 1):
                source = item['source']
                results.append(f"### {i}. {source.get('title', '未知标题')}")
                results.append(f"**文件**: {source.get('filename', 'N/A')}")
                results.append(f"**检索模式**: {item['mode']}")

                content = source.get('content', '')
                if content:
                    results.append(f"**内容预览**: {content[:200]}...")

                results.append("")

            return "\n".join(results)

        except Exception as e:
            return f"ES混合检索出错: {str(e)}"
