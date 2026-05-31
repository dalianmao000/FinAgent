"""Insurance Specialist Agent - 保险顾问专家."""
from qwen_agent.agents import Assistant

from .tools import QueryClauseTool, QueryPolicyTool, CalculateLoanTool


class InsuranceAgent(Assistant):
    """Specialist agent for insurance advisory."""
    NAME = "insurance"
    DESCRIPTION = "保险顾问专家，可以查询保险条款和保单信息"
    SYSTEM_MESSAGE = """你是一个专业的保险顾问专家。你可以查询保险条款、保单信息、计算保单贷款金额。"""

    def __init__(self, session_id: str, **kwargs):
        super().__init__(
            llm={'model': 'qwen-turbo', 'model_type': 'qwen_dashscope'},
            system_message=self.SYSTEM_MESSAGE,
            function_list=[
                QueryClauseTool(),
                QueryPolicyTool(),
                CalculateLoanTool(),
            ],
            name=self.NAME,
            description=self.DESCRIPTION,
            **kwargs
        )