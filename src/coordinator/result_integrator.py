"""Result integration from multiple agents."""
from typing import Dict, List, Any

from .intent_classifier import Domain
from .task_decomposer import Task


class ResultIntegrator:
    """Integrates results from multiple specialist agents."""

    def __init__(self):
        pass

    def integrate(
        self,
        original_query: str,
        tasks: List[Task],
        results: Dict[str, Dict[str, Any]]
    ) -> str:
        """Integrate results from all agents into a coherent response."""
        if not results:
            return "抱歉，没有找到相关信息。"

        if len(results) == 1:
            return self._integrate_single(results, tasks)

        return self._integrate_cross_domain(original_query, tasks, results)

    def _integrate_single(
        self,
        results: Dict[str, Dict[str, Any]],
        tasks: List[Task]
    ) -> str:
        """Integrate single domain results."""
        agent_name = list(results.keys())[0]
        data = results[agent_name]

        if "summary" in data:
            return data["summary"]

        if "positions" in data and data["positions"]:
            pos = data["positions"][0]
            stock = pos.get("stock", "股票")
            shares = pos.get("shares", 0)
            pnl = pos.get("pnl", 0)
            if pnl != 0:
                pnl_str = f"{'盈利' if pnl >= 0 else '亏损'}{abs(pnl)*100:.1f}%"
                return f"您持有{stock}共{shares}股，当前{pnl_str}"
            return f"您持有{stock}共{shares}股"

        return f"查询完成，结果: {data}"

    def _integrate_cross_domain(
        self,
        original_query: str,
        tasks: List[Task],
        results: Dict[str, Dict[str, Any]]
    ) -> str:
        """Integrate cross-domain results with synthesis."""
        sections = []

        # Customer info
        if "customer" in results:
            customer_data = results["customer"]
            profile = customer_data.get("profile", {})
            name = profile.get("name", "客户")
            assets = profile.get("total_assets", 0)
            risk = profile.get("risk_level", "")
            if assets:
                sections.append(f"【客户信息】{name}，总资产{assets/10000:.0f}万，风险等级{risk}")
            else:
                sections.append(f"【客户信息】{name}")

        # Investment info
        if "investment" in results:
            inv_data = results["investment"]
            if "positions" in inv_data and inv_data["positions"]:
                pos = inv_data["positions"][0]
                stock = pos.get("stock", "股票")
                pnl = pos.get("pnl", 0)
                pnl_str = f"盈利{abs(pnl)*100:.0f}%" if pnl >= 0 else f"亏损{abs(pnl)*100:.0f}%"
                sections.append(f"【投资情况】持有{stock}，当前{pnl_str}")
            elif "total_pnl" in inv_data:
                total_pnl = inv_data["total_pnl"]
                total_pnl_str = f"盈利{abs(total_pnl):.0f}元" if total_pnl >= 0 else f"亏损{abs(total_pnl):.0f}元"
                sections.append(f"【投资情况】{total_pnl_str}")
            elif "summary" in inv_data:
                sections.append(f"【投资情况】{inv_data['summary']}")

        # Insurance info
        if "insurance" in results:
            ins_data = results["insurance"]
            if "summary" in ins_data:
                sections.append(f"【保险情况】{ins_data['summary']}")
            elif "total_loanable" in ins_data:
                loanable = ins_data["total_loanable"]
                sections.append(f"【保险情况】最高可贷{loanable/10000:.0f}万")
            elif "policies" in ins_data:
                policies = ins_data["policies"]
                if policies:
                    sections.append(f"【保险情况】持有{len(policies)}份保单")

        # Synthesize based on query intent
        if "贷款" in original_query:
            if "insurance" in results and "total_loanable" in results["insurance"]:
                loanable = results["insurance"]["total_loanable"]
                analysis = self._synthesize_loan_advice(results)
                sections.append(f"【综合建议】{analysis}")
            elif "insurance" in results and "summary" in results["insurance"]:
                sections.append(f"【综合建议】{results['insurance']['summary']}")

        return "\n\n".join(sections) if sections else "已完成查询，请查看详细信息。"

    def _synthesize_loan_advice(self, results: Dict[str, Any]) -> str:
        """Synthesize advice for loan-related queries."""
        advice_parts = []

        # Get investment loss info
        inv_data = results.get("investment", {})
        pnl = 0
        if "positions" in inv_data and inv_data["positions"]:
            pnl = inv_data["positions"][0].get("pnl", 0)
        elif "total_pnl" in inv_data:
            pnl = inv_data.get("total_pnl", 0)

        # Get loan info
        ins_data = results.get("insurance", {})
        loanable = ins_data.get("total_loanable", 0)

        # Generate advice
        if pnl < -0.1:
            advice_parts.append(f"您的投资持仓亏损{abs(pnl)*100:.0f}%，")
            advice_parts.append(f"但保单可贷{loanable/10000:.0f}万，")
            advice_parts.append("可考虑应急周转。")
        elif pnl < 0:
            advice_parts.append(f"您的投资持仓小幅亏损{abs(pnl)*100:.0f}%，")
            advice_parts.append(f"保单可贷{loanable/10000:.0f}万作为备用。")
        else:
            advice_parts.append(f"您的投资情况良好，保单可贷{loanable/10000:.0f}万。")

        return "".join(advice_parts) if advice_parts else "详细信息请咨询客户经理。"