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


def app_gui():
    """Launch Gradio WebUI with tabs for all specialist agents."""
    try:
        import gradio as gr
    except ImportError:
        print("Gradio not installed. Run: pip install gradio")
        return

    # Initialize agents
    investment_bot = init_investment_agent()
    customer_bot = init_customer_agent()
    insurance_bot = init_insurance_agent()

    with gr.Blocks(title="金融智能顾问统一平台") as demo:
        gr.Markdown("# 金融智能顾问统一平台")
        gr.Markdown("面向综合金融顾问的AI辅助决策系统，支持投资分析、客户经营、保险顾问三大领域")

        with gr.Tabs():
            # Tab 1: 投资分析
            with gr.Tab("投资分析助手"):
                gr.Markdown("## 投资分析助手")
                gr.Markdown("专业投资分析专家，提供持仓查询、盈亏计算、股价预测、布林带检测、周期性分析等功能")

                with gr.Row():
                    with gr.Column(scale=3):
                        investment_chatbot = gr.Chatbot(height=500, label="对话")
                        investment_input = gr.Textbox(
                            label="输入您的问题",
                            placeholder=f"例如：{INVESTMENT_EXAMPLES[0]}",
                            lines=3
                        )
                        with gr.Row():
                            investment_submit = gr.Button("发送", variant="primary")
                            investment_clear = gr.Button("清空")

                    with gr.Column(scale=1):
                        gr.Markdown("### Agent 信息")
                        gr.Markdown("**类型**: 投资分析")
                        gr.Markdown("**模型**: qwen-turbo")

                gr.Markdown("### 示例问题")
                gr.Examples(
                    examples=[[e] for e in INVESTMENT_EXAMPLES],
                    inputs=investment_input
                )

                def investment_chat(message, history):
                    try:
                        return investment_bot.process(message)
                    except Exception as e:
                        return f"发生错误: {str(e)}"

                investment_submit.click(investment_chat, inputs=[investment_input, investment_chatbot], outputs=[investment_chatbot])
                investment_input.submit(investment_chat, inputs=[investment_input, investment_chatbot], outputs=[investment_chatbot])
                investment_clear.click(lambda: ([], ""), outputs=[investment_chatbot, investment_input])

            # Tab 2: 客户经营
            with gr.Tab("客户经营助手"):
                gr.Markdown("## 客户经营助手")
                gr.Markdown("专业客户经营专家，提供客户画像、分群分析、产品关联、资产预测等高级分析功能")

                with gr.Row():
                    with gr.Column(scale=3):
                        customer_chatbot = gr.Chatbot(height=500, label="对话")
                        customer_input = gr.Textbox(
                            label="输入您的问题",
                            placeholder=f"例如：{CUSTOMER_EXAMPLES[0]}",
                            lines=3
                        )
                        with gr.Row():
                            customer_submit = gr.Button("发送", variant="primary")
                            customer_clear = gr.Button("清空")

                    with gr.Column(scale=1):
                        gr.Markdown("### Agent 信息")
                        gr.Markdown("**类型**: 客户经营")
                        gr.Markdown("**模型**: qwen-turbo")

                gr.Markdown("### 示例问题")
                gr.Examples(
                    examples=[[e] for e in CUSTOMER_EXAMPLES],
                    inputs=customer_input
                )

                def customer_chat(message, history):
                    try:
                        return customer_bot.process(message)
                    except Exception as e:
                        return f"发生错误: {str(e)}"

                customer_submit.click(customer_chat, inputs=[customer_input, customer_chatbot], outputs=[customer_chatbot])
                customer_input.submit(customer_chat, inputs=[customer_input, customer_chatbot], outputs=[customer_chatbot])
                customer_clear.click(lambda: ([], ""), outputs=[customer_chatbot, customer_input])

            # Tab 3: 保险顾问
            with gr.Tab("保险顾问助手"):
                gr.Markdown("## 保险顾问助手")
                gr.Markdown("专业保险顾问专家，提供保险条款查询、保单分析、保单贷款计算等功能")

                with gr.Row():
                    with gr.Column(scale=3):
                        insurance_chatbot = gr.Chatbot(height=500, label="对话")
                        insurance_input = gr.Textbox(
                            label="输入您的问题",
                            placeholder=f"例如：{INSURANCE_EXAMPLES[0]}",
                            lines=3
                        )
                        with gr.Row():
                            insurance_submit = gr.Button("发送", variant="primary")
                            insurance_clear = gr.Button("清空")

                    with gr.Column(scale=1):
                        gr.Markdown("### Agent 信息")
                        gr.Markdown("**类型**: 保险顾问")
                        gr.Markdown("**模型**: qwen-turbo")

                gr.Markdown("### 示例问题")
                gr.Examples(
                    examples=[[e] for e in INSURANCE_EXAMPLES],
                    inputs=insurance_input
                )

                def insurance_chat(message, history):
                    try:
                        return insurance_bot.process(message)
                    except Exception as e:
                        return f"发生错误: {str(e)}"

                insurance_submit.click(insurance_chat, inputs=[insurance_input, insurance_chatbot], outputs=[insurance_chatbot])
                insurance_input.submit(insurance_chat, inputs=[insurance_input, insurance_chatbot], outputs=[insurance_chatbot])
                insurance_clear.click(lambda: ([], ""), outputs=[insurance_chatbot, insurance_input])

            # Tab 4: 统一平台
            with gr.Tab("统一平台"):
                gr.Markdown("## 金融智能顾问统一平台")
                gr.Markdown("通过协调者自动调度合适的专家Agent处理问题")

                with gr.Row():
                    with gr.Column(scale=3):
                        unified_chatbot = gr.Chatbot(height=500, label="对话")
                        unified_input = gr.Textbox(
                            label="输入您的问题",
                            placeholder="例如：查询我的持仓情况",
                            lines=3
                        )
                        with gr.Row():
                            unified_submit = gr.Button("发送", variant="primary")
                            unified_clear = gr.Button("清空")

                    with gr.Column(scale=1):
                        gr.Markdown("### 当前客户信息")
                        unified_customer_id = gr.Textbox(label="客户ID", value="C001")
                        unified_customer_name = gr.Textbox(label="客户姓名", value="王总")
                        unified_customer_assets = gr.Number(label="总资产(元)", value=5000000)
                        unified_customer_risk = gr.Dropdown(
                            label="风险等级",
                            choices=["R1", "R2", "R3", "R4", "R5"],
                            value="R4"
                        )

                gr.Markdown("### 示例问题")
                gr.Examples(
                    examples=[
                        ["查询持仓情况"],
                        ["我客户持仓茅台亏损20%，能办保单贷款吗？"],
                        ["找出高净值客户有哪些"],
                        ["这个客户的保单能贷多少钱"],
                        ["预测贵州茅台未来10天的股价"],
                    ],
                    inputs=unified_input
                )

                gr.Markdown("""
                ### 支持领域
                - **投资分析**: 持仓查询、盈亏计算、股价预测、布林带检测、周期性分析
                - **客户经营**: 客户画像、分群分析、流失预警
                - **保险顾问**: 条款查询、保单查询、保单贷款计算
                """)

                def unified_chat(message, history):
                    try:
                        import requests
                        response = requests.post(
                            "http://localhost:5000/api/v1/chat",
                            json={"message": message, "session_id": "webui-unified-session"},
                            timeout=60
                        )
                        result = response.json()
                        return result.get("response", "抱歉，发生了错误。")
                    except Exception as e:
                        return f"发生错误: {str(e)}"

                unified_submit.click(unified_chat, inputs=[unified_input, unified_chatbot], outputs=[unified_chatbot])
                unified_input.submit(unified_chat, inputs=[unified_input, unified_chatbot], outputs=[unified_chatbot])
                unified_clear.click(lambda: ([], ""), outputs=[unified_chatbot, unified_input])

    print("金融智能顾问统一平台 WebUI 准备就绪...")
    try:
        demo.launch(server_name="0.0.0.0", server_port=7861, show_error=True)
    except Exception as e:
        print(f"启动服务 (后台运行): {e}")
        import time
        time.sleep(3600)  # Keep alive


if __name__ == '__main__':
    app_gui()
