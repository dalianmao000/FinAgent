"""Gradio WebUI for FinAgent Unified."""
import gradio as gr
import uuid
import requests
from typing import Tuple

API_BASE = "http://localhost:5000/api/v1"


def chat_fn(message: str, history: list, session_id: str) -> Tuple[str, str]:
    """Handle chat interaction."""
    if not session_id:
        session_id = str(uuid.uuid4())

    try:
        response = requests.post(
            f"{API_BASE}/chat",
            json={"message": message, "session_id": session_id},
            timeout=30
        )
        result = response.json()
        response_text = result.get("response", "抱歉，发生了错误。")
        return response_text, session_id
    except requests.exceptions.ConnectionError:
        return "连接失败：无法连接到后端服务，请确保API服务已启动。", session_id
    except Exception as e:
        return f"发生错误: {str(e)}", session_id


def set_customer_fn(customer_id: str, name: str, assets: float, risk_level: str, session_id: str) -> Tuple[str, str]:
    """Set current customer."""
    if not session_id:
        return "请先发送一条消息建立会话", ""

    try:
        response = requests.post(
            f"{API_BASE}/session/{session_id}/customer",
            json={
                "customer_id": customer_id,
                "name": name,
                "total_assets": assets,
                "risk_level": risk_level
            },
            timeout=10
        )
        if response.status_code == 200:
            return f"客户信息已设置: {name}", session_id
        return f"设置失败: {response.text}", session_id
    except requests.exceptions.ConnectionError:
        return "连接失败：无法连接到后端服务", session_id
    except Exception as e:
        return f"发生错误: {str(e)}", session_id


def create_ui():
    """Create Gradio UI."""
    with gr.Blocks(title="金融智能顾问") as demo:
        gr.Markdown("# 金融智能顾问统一平台")
        gr.Markdown("面向综合金融顾问的AI辅助决策系统，支持投资分析、客户经营、保险顾问三大领域")

        session_id = gr.State(value="")

        with gr.Row():
            with gr.Column(scale=3):
                chatbot = gr.Chatbot(height=500, label="对话")
                msg_input = gr.Textbox(
                    label="输入您的问题",
                    placeholder="例如：我客户持仓茅台亏了20%，能办保单贷款吗？",
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
                ["分析客户流失风险"]
            ],
            inputs=msg_input
        )

        gr.Markdown("""
        ### 使用说明
        1. 先设置当前客户信息（可选）
        2. 在对话框输入您的问题
        3. 系统会自动识别问题领域并调度相应专家Agent
        4. 跨领域问题会自动协作完成

        ### 支持领域
        - **投资分析**: 持仓查询、盈亏计算、股价预测
        - **客户经营**: 客户画像、分群分析、流失预警
        - **保险顾问**: 条款查询、保单贷款计算
        """)

        # Event handlers
        submit_btn.click(
            chat_fn,
            inputs=[msg_input, chatbot, session_id],
            outputs=[chatbot, session_id]
        )
        msg_input.submit(
            chat_fn,
            inputs=[msg_input, chatbot, session_id],
            outputs=[chatbot, session_id]
        )
        clear_btn.click(
            lambda: ([], ""),
            outputs=[chatbot, msg_input]
        )
        set_customer_btn.click(
            set_customer_fn,
            inputs=[customer_id, customer_name, customer_assets, customer_risk, session_id],
            outputs=[msg_input, session_id]
        )

    return demo


if __name__ == "__main__":
    demo = create_ui()
    demo.launch(server_name="0.0.0.0", server_port=7860)