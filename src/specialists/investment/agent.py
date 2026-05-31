"""Investment Specialist Agent - 投资专家."""
from typing import Dict, Any
from unittest.mock import MagicMock

from ..base import SpecialistAgent, SpecialistConfig, Tool
from ...coordinator.intent_classifier import Domain


class InvestmentAgent(SpecialistAgent):
    """Specialist agent for investment analysis."""

    def _initialize_tools(self):
        """Initialize investment tools."""
        self.register_tool(Tool(
            name="query_positions",
            description="查询客户持仓情况"
        ))
        self.register_tool(Tool(
            name="calculate_pnl",
            description="计算盈亏情况"
        ))
        self.register_tool(Tool(
            name="arima_forecast",
            description="ARIMA预测股价"
        ))
        self.register_tool(Tool(
            name="bollinger_detection",
            description="布林带技术指标检测"
        ))

    def _execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute investment tool."""
        task = parameters.get("task")

        if tool_name == "query_positions":
            return self._query_positions()
        elif tool_name == "calculate_pnl":
            return self._calculate_pnl()
        elif tool_name == "arima_forecast":
            return self._arima_forecast()
        elif tool_name == "bollinger_detection":
            return self._bollinger_detection()

        return {"status": "unknown_tool", "tool": tool_name}

    def _query_positions(self) -> Dict[str, Any]:
        """Query customer positions from database."""
        try:
            # Try to get customer from context
            try:
                customer = self.shared_context.get_customer()
            except Exception:
                # Redis not available or no customer set
                customer = None

            # Mock positions for demonstration
            # In production, this would query actual position data from MySQL
            positions = [
                {
                    "stock": "贵州茅台",
                    "ts_code": "600519.SH",
                    "shares": 500,
                    "cost": 1800,
                    "current": 1440,
                    "market_value": 720000
                },
                {
                    "stock": "宁德时代",
                    "ts_code": "300750.SZ",
                    "shares": 200,
                    "cost": 450,
                    "current": 380,
                    "market_value": 76000
                }
            ]

            return {
                "status": "success",
                "positions": positions,
                "summary": f"客户{(customer.name if customer else '未知')}持有{len(positions)}只股票"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _calculate_pnl(self) -> Dict[str, Any]:
        """Calculate profit and loss."""
        positions_result = self._query_positions()
        if positions_result["status"] != "success":
            return positions_result

        positions = positions_result.get("positions", [])
        total_cost = 0
        total_value = 0

        for pos in positions:
            cost = pos["shares"] * pos["cost"]
            value = pos["shares"] * pos["current"]
            pnl = value - cost
            pos["pnl"] = pnl
            pos["pnl_pct"] = pnl / cost if cost > 0 else 0
            total_cost += cost
            total_value += value

        total_pnl = total_value - total_cost
        total_pnl_pct = total_pnl / total_cost if total_cost > 0 else 0

        return {
            "status": "success",
            "positions": positions,
            "total_cost": total_cost,
            "total_value": total_value,
            "total_pnl": total_pnl,
            "total_pnl_pct": total_pnl_pct,
            "summary": f"总盈亏: {'盈利' if total_pnl >= 0 else '亏损'}{abs(total_pnl):.2f}元 ({abs(total_pnl_pct)*100:.1f}%)"
        }

    def _arima_forecast(self) -> Dict[str, Any]:
        """ARIMA price forecasting - placeholder."""
        return {
            "status": "placeholder",
            "message": "ARIMA预测功能开发中"
        }

    def _bollinger_detection(self) -> Dict[str, Any]:
        """Bollinger band detection - placeholder."""
        return {
            "status": "placeholder",
            "message": "布林带检测功能开发中"
        }