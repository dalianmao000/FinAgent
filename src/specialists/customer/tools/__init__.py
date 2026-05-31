"""Customer Specialist Tools."""
from qwen_agent.tools.base import BaseTool, register_tool


@register_tool('customer_query_profile')
class QueryProfileTool(BaseTool):
    """查询客户画像"""
    name = 'customer_query_profile'
    description = '查询客户的基本信息和画像'
    parameters = []

    def call(self, params: str, **kwargs) -> str:
        return "客户信息：\n- 姓名：王总\n- 年龄：45岁\n- 资产：500万\n- 风险等级：R4\n- 客户类型：价值客户"


@register_tool('customer_clustering')
class CustomerClusteringTool(BaseTool):
    """客户分群分析"""
    name = 'customer_clustering'
    description = '对客户进行分群分析'
    parameters = []

    def call(self, params: str, **kwargs) -> str:
        return "客户分群结果：\n1. 高净值客户群 (资产>100万)\n2. 中产客户群 (资产50-100万)\n3. 普通客户群 (资产<50万)"


__all__ = ['QueryProfileTool', 'CustomerClusteringTool']
