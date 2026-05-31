"""查询保单信息工具."""
from qwen_agent.tools.base import BaseTool, register_tool


@register_tool('insurance_query_policy')
class QueryPolicyTool(BaseTool):
    """查询保单信息"""
    name = 'insurance_query_policy'
    description = '查询客户的保单信息'
    parameters = []

    def call(self, params: str, **kwargs) -> str:
        return "客户保单信息：\n1. 寿险(平安保险)：现金价值50万\n2. 重疾险(平安保险)：现金价值0"
