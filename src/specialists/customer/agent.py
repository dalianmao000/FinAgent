"""Customer Specialist Agent - 客户经营专家."""
from qwen_agent.agents import Assistant

from .tools import QueryProfileTool, CustomerClusteringTool


class CustomerAgent(Assistant):
    """Specialist agent for customer management."""
    NAME = "customer"
    DESCRIPTION = "客户经营专家，可以查询客户画像和进行分群分析"
    SYSTEM_MESSAGE = """你是一个专业的客户经营专家。你可以查询客户画像、分析客户群体、预测客户流失风险。"""

    def __init__(self, session_id: str, **kwargs):
        super().__init__(
            llm={'model': 'qwen-turbo', 'model_type': 'qwen_dashscope'},
            system_message=self.SYSTEM_MESSAGE,
            function_list=[
                QueryProfileTool(),
                CustomerClusteringTool(),
            ],
            name=self.NAME,
            description=self.DESCRIPTION,
            **kwargs
        )