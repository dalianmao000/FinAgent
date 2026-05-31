"""查询客户画像工具."""
from qwen_agent.tools.base import BaseTool, register_tool


@register_tool('customer_query_profile')
class QueryProfileTool(BaseTool):
    """查询客户画像"""
    name = 'customer_query_profile'
    description = '查询客户的基本信息和画像'
    parameters = []

    def call(self, params: str, **kwargs) -> str:
        return "客户信息：\n- 姓名：王总\n- 年龄：45岁\n- 资产：500万\n- 风险等级：R4\n- 客户类型：价值客户"
