"""Customer Specialist Agent - 客户经营专家."""
from qwen_agent.agents import Assistant

from .tools import (
    ExecuteSQLTool,
    HighValueUserInsightTool,
    DecisionTreeAssetPredictionTool,
    KMeansClusteringTool,
    ProductAssociationRulesTool,
    ARIMAAssetForecastTool,
    LightGBMAssetPredictionTool,
)
from ...tools.config import get_settings


class CustomerAgent(Assistant):
    """Specialist agent for customer management."""
    NAME = "customer"
    DESCRIPTION = "客户经营专家，提供SQL查询、高价值用户画像、决策树分析、KMeans聚类、产品关联、ARIMA预测等高级分析功能"
    SYSTEM_MESSAGE = """你是一个专业的客户经营专家。你可以执行SQL查询客户数据、进行客户分群、预测高价值客户、分析产品关联规则、预测资产趋势等。"""

    def __init__(self, session_id: str, **kwargs):
        settings = get_settings()
        super().__init__(
            llm={'model': settings.model_name, 'model_type': settings.model_type},
            system_message=self.SYSTEM_MESSAGE,
            function_list=[
                ExecuteSQLTool(),
                HighValueUserInsightTool(),
                DecisionTreeAssetPredictionTool(),
                KMeansClusteringTool(),
                ProductAssociationRulesTool(),
                ARIMAAssetForecastTool(),
                LightGBMAssetPredictionTool(),
            ],
            name=self.NAME,
            description=self.DESCRIPTION,
            **kwargs
        )
