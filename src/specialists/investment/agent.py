"""Investment Specialist Agent - 投资专家."""
from typing import Dict, Any
from qwen_agent.tools.base import BaseTool, register_tool
from qwen_agent.agents import Assistant


@register_tool('investment_query_positions')
class QueryPositionsTool(BaseTool):
    """查询客户持仓情况"""
    name = 'investment_query_positions'
    description = '查询客户的股票持仓情况，包括持仓数量、成本价、当前价等信息'
    parameters = []

    def call(self, params: str, **kwargs) -> str:
        # Mock data - in production would query MySQL
        positions = [
            {"stock": "贵州茅台", "ts_code": "600519.SH", "shares": 500, "cost": 1800, "current": 1440},
            {"stock": "宁德时代", "ts_code": "300750.SZ", "shares": 200, "cost": 450, "current": 380}
        ]
        return f"客户持有以下股票：\n" + "\n".join([
            f"- {p['stock']}({p['ts_code']}): {p['shares']}股，成本价{p['cost']}，当前价{p['current']}"
            for p in positions
        ])


@register_tool('investment_calculate_pnl')
class CalculatePnLTool(BaseTool):
    """计算盈亏情况"""
    name = 'investment_calculate_pnl'
    description = '计算客户持仓的盈亏情况'
    parameters = []

    def call(self, params: str, **kwargs) -> str:
        # Mock calculation
        positions = [
            {"stock": "贵州茅台", "shares": 500, "cost": 1800, "current": 1440},
            {"stock": "宁德时代", "shares": 200, "cost": 450, "current": 380}
        ]
        total_cost = sum(p['shares'] * p['cost'] for p in positions)
        total_value = sum(p['shares'] * p['current'] for p in positions)
        pnl = total_value - total_cost
        pnl_pct = pnl / total_cost * 100 if total_cost > 0 else 0
        return f"总盈亏: {'盈利' if pnl >= 0 else '亏损'}{abs(pnl):.2f}元 ({abs(pnl_pct):.1f}%)"


class InvestmentAgent(Assistant):
    """Specialist agent for investment analysis."""
    NAME = "investment"
    DESCRIPTION = "投资分析专家，可以查询持仓和计算盈亏"
    SYSTEM_MESSAGE = """你是一个专业的投资分析专家。你可以查询客户持仓情况、计算盈亏、分析投资收益。"""

    def __init__(self, session_id: str, **kwargs):
        super().__init__(
            llm={'model': 'qwen-turbo', 'model_type': 'qwen_dashscope'},
            system_message=self.SYSTEM_MESSAGE,
            function_list=[
                QueryPositionsTool(),
                CalculatePnLTool(),
            ],
            name=self.NAME,
            description=self.DESCRIPTION,
            **kwargs
        )