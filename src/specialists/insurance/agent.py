"""Insurance Specialist Agent - 保险顾问专家."""
from typing import Dict, Any

from ..base import SpecialistAgent, SpecialistConfig, Tool
from ...coordinator.intent_classifier import Domain


class InsuranceAgent(SpecialistAgent):
    """Specialist agent for insurance advisory."""

    def _initialize_tools(self):
        """Initialize insurance tools."""
        self.register_tool(Tool(
            name="rag_query",
            description="RAG保险条款查询"
        ))
        self.register_tool(Tool(
            name="query_policy",
            description="保单查询"
        ))
        self.register_tool(Tool(
            name="calculate_loan",
            description="保单贷款计算"
        ))

    def _execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute insurance tool."""
        task = parameters.get("task")

        if tool_name == "rag_query":
            return self._rag_query(task)
        elif tool_name == "query_policy":
            return self._query_policy()
        elif tool_name == "calculate_loan":
            return self._calculate_loan()

        return {"status": "unknown_tool", "tool": tool_name}

    def _rag_query(self, task=None) -> Dict[str, Any]:
        """Query insurance clauses using RAG."""
        query = getattr(task, 'description', '保单贷款') if task else '保单贷款'

        # Mock RAG results
        # In production, this would query Elasticsearch
        results = [
            {
                "title": "寿险保单贷款条款",
                "content": "投保人可申请保单现金价值80%的贷款",
                "score": 0.95,
                "source": "平安寿险条款.pdf"
            },
            {
                "title": "贷款利息规定",
                "content": "年利率约4.5%-6%，按日计息，提前还款无违约金",
                "score": 0.88,
                "source": "平安寿险条款.pdf"
            }
        ]

        return {
            "status": "success",
            "query": query,
            "results": results,
            "summary": f"找到{len(results)}条相关保险条款"
        }

    def _query_policy(self) -> Dict[str, Any]:
        """Query customer's insurance policies."""
        # Mock policy data
        # In production, this would query MySQL
        policies = [
            {
                "type": "寿险",
                "insurer": "平安保险",
                "policy_no": "PA***1234",
                "cash_value": 500000,
                "premium": 100000,
                "status": "有效"
            },
            {
                "type": "重疾险",
                "insurer": "平安保险",
                "policy_no": "PA***5678",
                "cash_value": 0,
                "premium": 30000,
                "status": "有效"
            }
        ]

        return {
            "status": "success",
            "policies": policies,
            "summary": f"客户持有{len(policies)}份保单"
        }

    def _calculate_loan(self) -> Dict[str, Any]:
        """Calculate policy loan amount."""
        policies_result = self._query_policy()
        if policies_result["status"] != "success":
            return policies_result

        policies = policies_result.get("policies", [])
        total_loanable = sum(p["cash_value"] * 0.8 for p in policies if p["cash_value"] > 0)

        return {
            "status": "success",
            "policies": policies,
            "total_loanable": total_loanable,
            "summary": f"最高可贷{total_loanable/10000:.0f}万（按现金价值80%计算）"
        }