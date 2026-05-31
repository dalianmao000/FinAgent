"""计算保单可贷金额工具."""
from qwen_agent.tools.base import BaseTool, register_tool


@register_tool('insurance_calculate_loan')
class CalculateLoanTool(BaseTool):
    """计算保单可贷金额"""
    name = 'insurance_calculate_loan'
    description = '计算保单可以贷款的金额'
    parameters = []

    def call(self, params: str, **kwargs) -> str:
        return "保单贷款计算结果：\n- 寿险现金价值：50万\n- 最高可贷额度(80%)：40万\n- 参考利率：4.5%-6%/年"
