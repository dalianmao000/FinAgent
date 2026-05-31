"""Investment Specialist Agent - 投资专家."""
from qwen_agent.agents import Assistant

from .tools import (
    QueryPositionsTool,
    CalculatePnLTool,
    ArimaPredictionTool,
    BollDetectionTool,
    ProphetAnalysisTool,
)


class InvestmentAgent(Assistant):
    """Specialist agent for investment analysis."""
    NAME = "investment"
    DESCRIPTION = "投资分析专家，可以查询持仓和计算盈亏"
    SYSTEM_MESSAGE = """你是一个专业的投资分析专家。你可以查询客户持仓情况、计算盈亏、分析投资收益、进行股价预测、布林带异常检测、周期性分析。"""

    def __init__(self, session_id: str, **kwargs):
        super().__init__(
            llm={'model': 'qwen-turbo', 'model_type': 'qwen_dashscope'},
            system_message=self.SYSTEM_MESSAGE,
            function_list=[
                QueryPositionsTool(),
                CalculatePnLTool(),
                ArimaPredictionTool(),
                BollDetectionTool(),
                ProphetAnalysisTool(),
            ],
            name=self.NAME,
            description=self.DESCRIPTION,
            **kwargs
        )