"""查询客户持仓情况工具."""
from qwen_agent.tools.base import BaseTool, register_tool


@register_tool('investment_query_positions')
class QueryPositionsTool(BaseTool):
    """查询客户持仓情况"""
    name = 'investment_query_positions'
    description = '查询客户的股票持仓情况，包括持仓数量、成本价、当前价等信息'
    parameters = []

    def call(self, params: str, **kwargs) -> str:
        positions = [
            {"stock": "贵州茅台", "ts_code": "600519.SH", "shares": 500, "cost": 1800, "current": 1440},
            {"stock": "宁德时代", "ts_code": "300750.SZ", "shares": 200, "cost": 450, "current": 380}
        ]
        return f"客户持有以下股票：\n" + "\n".join([
            f"- {p['stock']}({p['ts_code']}): {p['shares']}股，成本价{p['cost']}，当前价{p['current']}"
            for p in positions
        ])
