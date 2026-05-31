"""客户分群分析工具."""
from qwen_agent.tools.base import BaseTool, register_tool


@register_tool('customer_clustering')
class CustomerClusteringTool(BaseTool):
    """客户分群分析"""
    name = 'customer_clustering'
    description = '对客户进行分群分析'
    parameters = []

    def call(self, params: str, **kwargs) -> str:
        return "客户分群结果：\n1. 高净值客户群 (资产>100万)\n2. 中产客户群 (资产50-100万)\n3. 普通客户群 (资产<50万)"
