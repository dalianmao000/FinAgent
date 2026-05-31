"""WebUI for FinAgent Unified using qwen-agent patterns."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv

from ..specialists.investment.agent import InvestmentAgent
from ..specialists.customer.agent import CustomerAgent
from ..specialists.insurance.agent import InsuranceAgent

load_dotenv()


def init_investment_agent():
    """Initialize investment agent with tools."""
    return InvestmentAgent(session_id='webui-investment')


def init_customer_agent():
    """Initialize customer agent."""
    return CustomerAgent(session_id='webui-customer')


def init_insurance_agent():
    """Initialize insurance agent."""
    return InsuranceAgent(session_id='webui-insurance')


INVESTMENT_EXAMPLES = [
    '查询我的持仓情况',
    '贵州茅台亏了多少？',
    '预测贵州茅台未来10天股价',
    '检测贵州茅台近一年超买超卖点',
    '分析五粮液近一年周期性规律',
]

CUSTOMER_EXAMPLES = [
    '数据库包含哪些表和字段',
    '我行目前有多少客户？总资产管理规模是多少？',
    '客户的平均资产是多少？高净值客户的占比如何？',
    '客户"33c44545627f41e8ad113027340de3e9"成为高价值客户的概率是多少？',
    '哪些客户未来3个月资产容易提升至100万+?',
    '分析产品关联规则，有哪些频繁产品组合？',
    '预测客户00022f44a4c74496aa0d8c5f95142a5b未来3个月资产变化',
    '基于理财产品的交叉销售策略是什么？',
]

INSURANCE_EXAMPLES = [
    '查询保险条款：重疾险保障范围',
    '查询保险条款：意外医疗报销比例',
    '保单贷款能贷多少钱？',
    '查询万能险的收益规则',
    '对比医疗险和重疾险的区别',
]


def app_gui(agent_type='investment'):
    """Launch Gradio WebUI for single specialist agent.

    Args:
        agent_type: 'investment', 'customer', or 'insurance'
    """
    try:
        import gradio as gr
    except ImportError:
        print("Gradio not installed. Run: pip install gradio")
        return

    if agent_type == 'investment':
        bot = init_investment_agent()
        title = "投资分析助手"
        description = "专业投资分析专家，提供持仓查询、盈亏计算、股价预测、布林带检测、周期性分析等功能"
        examples = INVESTMENT_EXAMPLES
    elif agent_type == 'customer':
        bot = init_customer_agent()
        title = "客户经营助手"
        description = "专业客户经营专家，提供客户画像、分群分析、产品关联、资产预测等高级分析功能"
        examples = CUSTOMER_EXAMPLES
    elif agent_type == 'insurance':
        bot = init_insurance_agent()
        title = "保险顾问助手"
        description = "专业保险顾问专家，提供保险条款查询、保单分析、保单贷款计算等功能"
        examples = INSURANCE_EXAMPLES
    else:
        print(f"Unknown agent type: {agent_type}")
        print("Usage: python -m src.gui.webui [investment|customer|insurance]")
        return

    with gr.Blocks(title=title) as demo:
        gr.Markdown(f"# {title}")
        gr.Markdown(description)

        with gr.Row():
            with gr.Column(scale=3):
                chatbot = gr.Chatbot(height=500, label="对话")
                msg_input = gr.Textbox(
                    label="输入您的问题",
                    placeholder=f"例如：{examples[0]}",
                    lines=3
                )
                with gr.Row():
                    submit_btn = gr.Button("发送", variant="primary")
                    clear_btn = gr.Button("清空")

            with gr.Column(scale=1):
                gr.Markdown("### Agent 信息")
                gr.Markdown(f"**类型**: {agent_type}")
                gr.Markdown(f"**模型**: qwen-turbo")

        gr.Markdown("### 示例问题")
        gr.Examples(
            examples=[[e] for e in examples],
            inputs=msg_input
        )

        def chat_fn(message, history):
            """Handle chat interaction."""
            try:
                response = bot.process(message)
                return response
            except Exception as e:
                return f"发生错误: {str(e)}"

        submit_btn.click(chat_fn, inputs=[msg_input, chatbot], outputs=[chatbot])
        msg_input.submit(chat_fn, inputs=[msg_input, chatbot], outputs=[chatbot])
        clear_btn.click(lambda: ([], ""), outputs=[chatbot, msg_input])

    print(f"{title} WebUI 准备就绪...")
    demo.launch(server_name="0.0.0.0", server_port=7860)


def app_gui_unified():
    """Launch unified Gradio WebUI with all specialists."""
    try:
        import gradio as gr
    except ImportError:
        print("Gradio not installed. Run: pip install gradio")
        return

    from ..api.main import create_app

    app = create_app()

    with gr.Blocks(title="金融智能顾问统一平台") as demo:
        gr.Markdown("# 金融智能顾问统一平台")
        gr.Markdown("面向综合金融顾问的AI辅助决策系统，支持投资分析、客户经营、保险顾问三大领域")

        with gr.Row():
            with gr.Column(scale=3):
                chatbot = gr.Chatbot(height=500, label="对话")
                msg_input = gr.Textbox(
                    label="输入您的问题",
                    placeholder="例如：查询我的持仓情况",
                    lines=3
                )
                with gr.Row():
                    submit_btn = gr.Button("发送", variant="primary")
                    clear_btn = gr.Button("清空")

            with gr.Column(scale=1):
                gr.Markdown("### 当前客户信息")
                customer_id = gr.Textbox(label="客户ID", value="C001")
                customer_name = gr.Textbox(label="客户姓名", value="王总")
                customer_assets = gr.Number(label="总资产(元)", value=5000000)
                customer_risk = gr.Dropdown(
                    label="风险等级",
                    choices=["R1", "R2", "R3", "R4", "R5"],
                    value="R4"
                )
                set_customer_btn = gr.Button("设置客户", variant="secondary")

        gr.Markdown("### 示例问题")
        gr.Examples(
            examples=[
                ["查询持仓情况"],
                ["我客户持仓茅台亏损20%，能办保单贷款吗？"],
                ["找出高净值客户有哪些"],
                ["这个客户的保单能贷多少钱"],
                ["预测贵州茅台未来10天的股价"],
            ],
            inputs=msg_input
        )

        gr.Markdown("""
        ### 支持领域
        - **投资分析**: 持仓查询、盈亏计算、股价预测、布林带检测、周期性分析
        - **客户经营**: 客户画像、分群分析、流失预警
        - **保险顾问**: 条款查询、保单查询、保单贷款计算
        """)

        def chat_fn(message, history):
            """Handle chat interaction."""
            try:
                import requests
                response = requests.post(
                    "http://localhost:5000/api/v1/chat",
                    json={"message": message, "session_id": "webui-session"},
                    timeout=60
                )
                result = response.json()
                return result.get("response", "抱歉，发生了错误。")
            except Exception as e:
                return f"发生错误: {str(e)}"

        submit_btn.click(chat_fn, inputs=[msg_input, chatbot], outputs=[chatbot])
        msg_input.submit(chat_fn, inputs=[msg_input, chatbot], outputs=[chatbot])
        clear_btn.click(lambda: ([], ""), outputs=[chatbot, msg_input])

    print("金融智能顾问统一平台 WebUI 准备就绪...")
    demo.launch(server_name="0.0.0.0", server_port=7860)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == '--unified':
            app_gui_unified()
        elif sys.argv[1] in ('investment', 'customer', 'insurance'):
            app_gui(sys.argv[1])
        else:
            print("用法: python -m src.gui.webui [investment|customer|insurance|--unified]")
            print("  默认启动投资分析助手")
            app_gui('investment')
    else:
        app_gui('investment')
