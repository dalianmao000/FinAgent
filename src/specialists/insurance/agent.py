"""Insurance Specialist Agent - 保险顾问专家."""
from qwen_agent.tools.base import BaseTool, register_tool
from qwen_agent.agents import Assistant


@register_tool('insurance_query_clause')
class QueryClauseTool(BaseTool):
    """查询保险条款"""
    name = 'insurance_query_clause'
    description = '查询保险条款相关信息'
    parameters = [{
        'name': 'query',
        'type': 'string',
        'description': '查询关键词'
    }]

    def call(self, params: str, **kwargs) -> str:
        import json
        try:
            args = json.loads(params) if isinstance(params, str) else params
        except:
            args = {'query': '保单贷款'}

        return f"关于【{args.get('query', '保险条款')}】的查询结果：\n1. 寿险保单贷款条款：可贷现金价值的80%\n2. 贷款利息：年利率约4.5%-6%"


@register_tool('insurance_query_policy')
class QueryPolicyTool(BaseTool):
    """查询保单信息"""
    name = 'insurance_query_policy'
    description = '查询客户的保单信息'
    parameters = []

    def call(self, params: str, **kwargs) -> str:
        return "客户保单信息：\n1. 寿险(平安保险)：现金价值50万\n2. 重疾险(平安保险)：现金价值0"


@register_tool('insurance_calculate_loan')
class CalculateLoanTool(BaseTool):
    """计算保单可贷金额"""
    name = 'insurance_calculate_loan'
    description = '计算保单可以贷款的金额'
    parameters = []

    def call(self, params: str, **kwargs) -> str:
        return "保单贷款计算结果：\n- 寿险现金价值：50万\n- 最高可贷额度(80%)：40万\n- 参考利率：4.5%-6%/年"


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