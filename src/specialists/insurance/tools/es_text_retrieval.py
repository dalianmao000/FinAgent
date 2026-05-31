"""ES文本检索工具 - 基于Elasticsearch的文本检索."""
import json

from qwen_agent.tools.base import BaseTool, register_tool


@register_tool('insurance_es_text_retrieval')
class ESTextRetrievalTool(BaseTool):
    """基于Elasticsearch的文本检索工具"""
    name = 'insurance_es_text_retrieval'
    description = '使用Elasticsearch进行文本检索，查询保险条款相关内容'
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

            search_body = {
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["title^2", "content"],
                        "type": "best_fields",
                        "fuzziness": "AUTO"
                    }
                },
                "highlight": {
                    "fields": {
                        "content": {
                            "fragment_size": 200,
                            "number_of_fragments": 3
                        }
                    },
                    "pre_tags": ["<mark>"],
                    "post_tags": ["</mark>"]
                },
                "size": size
            }

            response = es.search(index=settings.es_index_name, body=search_body)
            hits = response['hits']['hits']
            total = response['hits']['total']['value']

            if not hits:
                return f"未找到关于「{query}」的相关文档"

            results = [f"## 搜索结果：{query}\n"]
            results.append(f"共找到 {total} 条相关文档\n")

            for i, hit in enumerate(hits, 1):
                score = hit['_score']
                source = hit['_source']
                highlights = hit.get('highlight', {})

                results.append(f"### {i}. {source.get('title', '未知标题')}")
                results.append(f"**文件**: {source.get('filename', 'N/A')}")
                results.append(f"**相关度**: {score:.2f}")

                if 'content' in highlights:
                    results.append("**相关内容**:")
                    for fragment in highlights['content']:
                        results.append(f"- {fragment}")

                results.append("")

            return "\n".join(results)

        except Exception as e:
            return f"ES文本检索出错: {str(e)}"
