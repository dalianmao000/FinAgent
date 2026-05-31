"""查询保险条款工具."""
from qwen_agent.tools.base import BaseTool, register_tool


@register_tool('insurance_query_clause')
class QueryClauseTool(BaseTool):
    """查询保险条款"""
    name = 'insurance_query_clause'
    description = '查询保险条款相关信息'
    parameters = [{
        'name': 'query',
        'type': 'string',
        'description': '查询关键词'
    }]

    def call(self, params: str, **kwargs) -> str:
        import json
        try:
            args = json.loads(params) if isinstance(params, str) else params
        except:
            args = {'query': '保单贷款'}

        return f"关于【{args.get('query', '保险条款')}】的查询结果：\n1. 寿险保单贷款条款：可贷现金价值的80%\n2. 贷款利息：年利率约4.5%-6%"
