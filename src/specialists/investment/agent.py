"""Investment Specialist Agent - 投资专家."""
from qwen_agent.agents import Assistant

from .tools import (
    QueryPositionsTool,
    CalculatePnLTool,
    ArimaPredictionTool,
    BollDetectionTool,
    ProphetAnalysisTool,
)
from ...tools.config import get_settings


class InvestmentAgent(Assistant):
    """Specialist agent for investment analysis."""
    NAME = "investment"
    DESCRIPTION = "投资分析专家，可以查询持仓和计算盈亏"
    SYSTEM_MESSAGE = """你是一个专业的投资分析专家。你可以查询客户持仓情况、计算盈亏、分析投资收益、进行股价预测、布林带异常检测、周期性分析。"""

    def __init__(self, session_id: str, **kwargs):
        settings = get_settings()
        super().__init__(
            llm={'model': settings.model_name, 'model_type': settings.model_type},
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


def init_agent():
    """Initialize investment agent for standalone use."""
    return InvestmentAgent(session_id='standalone')


def app_gui():
    """Launch WebUI for investment agent testing."""
    try:
        from qwen_agent.gui import WebUI
    except ImportError:
        print("qwen-agent GUI dependencies not installed.")
        print("Run: pip install 'qwen-agent[gui]'")
        return

    bot = init_agent()
    chatbot_config = {
        'prompt.suggestions': [
            '查询我的持仓情况',
            '贵州茅台亏了多少？',
            '预测贵州茅台未来10天股价',
            '检测贵州茅台近一年超买超卖点',
            '分析五粮液近一年周期性规律',
        ]
    }
    print("投资分析专家 WebUI 准备就绪...")
    WebUI(bot, chatbot_config=chatbot_config).run()


def app_tui():
    """Terminal UI for investment agent testing."""
    bot = init_agent()
    messages = []

    print("投资分析专家 TUI (输入 'quit' 退出)")
    print("-" * 40)

    while True:
        try:
            query = input("\n用户问题: ").strip()
            if not query:
                continue
            if query.lower() in ('quit', 'exit', 'q'):
                print("再见!")
                break

            messages.append({'role': 'user', 'content': query})
            print("正在处理...\n")

            response = []
            for chunk in bot.run(messages):
                if chunk:
                    response.extend(chunk)
                    for msg in chunk:
                        if hasattr(msg, 'content') and msg.content:
                            print(f"助手: {msg.content}")

            messages.extend(response)

        except KeyboardInterrupt:
            print("\n\n再见!")
            break
        except Exception as e:
            print(f"处理出错: {str(e)}")


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--tui':
        app_tui()
    else:
        app_gui()
