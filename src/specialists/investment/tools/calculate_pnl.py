"""计算盈亏情况工具."""
from qwen_agent.tools.base import BaseTool, register_tool


@register_tool('investment_calculate_pnl')
class CalculatePnLTool(BaseTool):
    """计算盈亏情况"""
    name = 'investment_calculate_pnl'
    description = '计算客户持仓的盈亏情况'
    parameters = []

    def call(self, params: str, **kwargs) -> str:
        positions = [
            {"stock": "贵州茅台", "shares": 500, "cost": 1800, "current": 1440},
            {"stock": "宁德时代", "shares": 200, "cost": 450, "current": 380}
        ]
        total_cost = sum(p['shares'] * p['cost'] for p in positions)
        total_value = sum(p['shares'] * p['current'] for p in positions)
        pnl = total_value - total_cost
        pnl_pct = pnl / total_cost * 100 if total_cost > 0 else 0
        return f"总盈亏: {'盈利' if pnl >= 0 else '亏损'}{abs(pnl):.2f}元 ({abs(pnl_pct):.1f}%)"
