"""WebUI for FinAgent Unified - FinTech Luxury Design."""
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

# Custom CSS for FinTech Luxury Design
CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&family=Space+Grotesk:wght@400;500;600&display=swap');

:root {
    --bg-primary: #0a0e17;
    --bg-secondary: #111827;
    --bg-card: #1a2235;
    --bg-card-hover: #243044;
    --accent-gold: #d4a853;
    --accent-gold-dim: #b8923f;
    --accent-emerald: #10b981;
    --accent-sapphire: #3b82f6;
    --accent-ruby: #ef4444;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --border-subtle: rgba(255,255,255,0.08);
    --glow-gold: 0 0 30px rgba(212,168,83,0.3);
    --glow-emerald: 0 0 20px rgba(16,185,129,0.2);
    --glow-sapphire: 0 0 20px rgba(59,130,246,0.2);
}

* {
    font-family: 'Space Grotesk', 'Noto Serif SC', -apple-system, sans-serif;
}

body {
    background: var(--bg-primary);
    background-image:
        radial-gradient(ellipse at 20% 0%, rgba(212,168,83,0.08) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 100%, rgba(59,130,246,0.05) 0%, transparent 50%);
    background-attachment: fixed;
}

/* Header Styling */
.header-section {
    text-align: center;
    padding: 2rem 1rem 1rem;
    background: linear-gradient(180deg, rgba(26,34,53,0.8) 0%, transparent 100%);
    border-bottom: 1px solid var(--border-subtle);
    margin-bottom: 1rem;
}

.main-title {
    font-family: 'Noto Serif SC', serif !important;
    font-size: 2.5rem !important;
    font-weight: 700 !important;
    background: linear-gradient(135deg, var(--accent-gold) 0%, #f5d799 50%, var(--accent-gold) 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    letter-spacing: 0.05em;
    margin-bottom: 0.5rem !important;
    animation: shimmer 3s ease-in-out infinite;
}

@keyframes shimmer {
    0%, 100% { filter: brightness(1); }
    50% { filter: brightness(1.2); }
}

.subtitle {
    color: var(--text-secondary);
    font-size: 1rem;
    letter-spacing: 0.1em;
}

/* Tab Styling */
.tab-item {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 12px 12px 0 0 !important;
    padding: 0.75rem 1.5rem !important;
    margin: 0 4px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.tab-item:hover {
    background: var(--bg-card-hover) !important;
    transform: translateY(-2px);
}

.tab-item.selected {
    background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-secondary) 100%) !important;
    border-bottom: 2px solid var(--accent-gold) !important;
}

.tab-icon {
    font-size: 1.2rem;
    margin-right: 8px;
}

/* Chat Container */
.chat-container {
    background: linear-gradient(145deg, var(--bg-card) 0%, rgba(17,24,39,0.9) 100%);
    border: 1px solid var(--border-subtle);
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.05);
}

/* Chatbot */
.gradio-container .chatbot {
    background: transparent !important;
    border-radius: 12px;
    border: 1px solid var(--border-subtle);
    min-height: 450px;
}

/* User Message */
.message.user {
    background: linear-gradient(135deg, var(--accent-gold-dim) 0%, var(--accent-gold) 100%) !important;
    color: #0a0e17 !important;
    border-radius: 18px 18px 4px 18px !important;
    padding: 12px 18px !important;
    font-weight: 500;
    box-shadow: var(--glow-gold);
}

/* Bot Message */
.message.bot {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 18px 18px 18px 4px !important;
    padding: 14px 18px !important;
    color: var(--text-primary) !important;
}

/* Input Styling */
.input-container textarea {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    padding: 14px 18px !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
}

.input-container textarea:focus {
    border-color: var(--accent-gold) !important;
    box-shadow: var(--glow-gold), 0 0 0 3px rgba(212,168,83,0.1) !important;
    outline: none !important;
}

.input-container textarea::placeholder {
    color: var(--text-muted) !important;
}

/* Buttons */
.btn-primary {
    background: linear-gradient(135deg, var(--accent-gold-dim) 0%, var(--accent-gold) 100%) !important;
    color: #0a0e17 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 28px !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 15px rgba(212,168,83,0.3);
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 25px rgba(212,168,83,0.5);
}

.btn-secondary {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 10px !important;
    padding: 12px 20px !important;
    color: var(--text-secondary) !important;
    transition: all 0.3s ease !important;
}

.btn-secondary:hover {
    background: var(--bg-card-hover) !important;
    border-color: var(--text-muted) !important;
    color: var(--text-primary) !important;
}

/* Agent Info Card */
.agent-card {
    background: linear-gradient(145deg, var(--bg-card) 0%, var(--bg-secondary) 100%);
    border: 1px solid var(--border-subtle);
    border-radius: 16px;
    padding: 1.5rem;
    height: 100%;
}

.agent-card h3 {
    font-family: 'Noto Serif SC', serif !important;
    color: var(--accent-gold) !important;
    font-size: 1.1rem !important;
    margin-bottom: 1rem !important;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--border-subtle);
}

.agent-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--bg-secondary);
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 0.85rem;
    margin-bottom: 0.5rem;
}

.badge-investment { color: var(--accent-gold); border: 1px solid rgba(212,168,83,0.3); }
.badge-customer { color: var(--accent-emerald); border: 1px solid rgba(16,185,129,0.3); }
.badge-insurance { color: var(--accent-sapphire); border: 1px solid rgba(59,130,246,0.3); }

/* Examples Section */
.examples-container {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 1rem;
    margin-top: 1rem;
}

.example-chip {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 20px !important;
    padding: 8px 16px !important;
    color: var(--text-secondary) !important;
    font-size: 0.85rem !important;
    cursor: pointer;
    transition: all 0.2s ease !important;
}

.example-chip:hover {
    background: var(--bg-card-hover) !important;
    border-color: var(--accent-gold) !important;
    color: var(--accent-gold) !important;
    transform: translateY(-1px);
}

/* Status Indicator */
.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    display: inline-block;
    margin-right: 6px;
}

.status-online { background: var(--accent-emerald); box-shadow: 0 0 8px var(--accent-emerald); }
.status-offline { background: var(--accent-ruby); }

/* Domain Colors */
.domain-investment { --domain-color: var(--accent-gold); }
.domain-customer { --domain-color: var(--accent-emerald); }
.domain-insurance { --domain-color: var(--accent-sapphire); }

/* Sidebar */
.sidebar {
    background: linear-gradient(180deg, var(--bg-card) 0%, var(--bg-secondary) 100%);
    border-left: 1px solid var(--border-subtle);
    padding: 1.5rem;
}

/* Loading Animation */
.loading-dots::after {
    content: '...';
    animation: dots 1.5s steps(4, end) infinite;
}

@keyframes dots {
    0%, 20% { content: ''; }
    40% { content: '.'; }
    60% { content: '..'; }
    80%, 100% { content: '...'; }
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

::-webkit-scrollbar-track {
    background: var(--bg-secondary);
    border-radius: 3px;
}

::-webkit-scrollbar-thumb {
    background: var(--text-muted);
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--text-secondary);
}

/* Responsive */
@media (max-width: 768px) {
    .main-title { font-size: 1.8rem !important; }
    .sidebar { border-left: none; border-top: 1px solid var(--border-subtle); }
}
"""


def app_gui():
    """Launch Gradio WebUI with tabs for all specialist agents."""
    try:
        import gradio as gr
    except ImportError:
        print("Gradio not installed. Run: pip install gradio")
        return

    investment_bot = init_investment_agent()
    customer_bot = init_customer_agent()
    insurance_bot = init_insurance_agent()

    with gr.Blocks(css=CUSTOM_CSS, title="金融智能顾问统一平台") as demo:
        # Custom Header
        gr.HTML("""
        <div class="header-section">
            <h1 class="main-title">金融智能顾问统一平台</h1>
            <p class="subtitle">AI-DRIVEN FINANCIAL ADVISOR</p>
        </div>
        """)

        with gr.Tabs():
            # Tab 1: 投资分析
            with gr.TabItem(id="investment", label="📈 投资分析助手"):
                gr.HTML('<div class="domain-investment">')

                with gr.Row():
                    with gr.Column(scale=3):
                        with gr.Group():
                            gr.HTML("""
                            <div class="chat-container">
                                <div style="display:flex;align-items:center;gap:8px;margin-bottom:1rem;">
                                    <span class="status-dot status-online"></span>
                                    <span style="color:var(--text-secondary);font-size:0.9rem;">投资分析专家 · 在线</span>
                                </div>
                            </div>
                            """)
                            investment_chatbot = gr.Chatbot(
                                height=420,
                                show_label=False,
                                container=True,
                                bubble_full_width=False
                            )

                    with gr.Column(scale=1):
                        gr.HTML("""
                        <div class="agent-card">
                            <h3>🤖 Agent Info</h3>
                            <div class="agent-badge badge-investment">
                                <span>📈</span> 投资分析专家
                            </div>
                            <p style="color:var(--text-secondary);font-size:0.85rem;margin-top:0.5rem;">
                                持仓查询 · 盈亏计算<br>
                                股价预测 · 布林带检测<br>
                                周期性分析
                            </p>
                            <div style="margin-top:1rem;padding-top:1rem;border-top:1px solid var(--border-subtle);">
                                <span style="color:var(--text-muted);font-size:0.8rem;">Model: qwen-turbo</span>
                            </div>
                        </div>
                        """)

                gr.HTML('</div>')

                with gr.Row():
                    investment_input = gr.Textbox(
                        placeholder=f"输入投资分析问题...",
                        lines=2,
                        show_label=False,
                        container=True,
                        elem_classes=["input-container"]
                    )
                    investment_submit = gr.Button("发送", elem_classes=["btn-primary"])
                    investment_clear = gr.Button("清空", elem_classes=["btn-secondary"])

                gr.HTML("""
                <div class="examples-container">
                    <span style="color:var(--text-muted);font-size:0.85rem;margin-right:1rem;">示例问题:</span>
                """)

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
            with gr.TabItem(id="customer", label="👥 客户经营助手"):
                with gr.Row():
                    with gr.Column(scale=3):
                        gr.HTML("""
                        <div class="chat-container">
                            <div style="display:flex;align-items:center;gap:8px;margin-bottom:1rem;">
                                <span class="status-dot status-online"></span>
                                <span style="color:var(--text-secondary);font-size:0.9rem;">客户经营专家 · 在线</span>
                            </div>
                        </div>
                        """)
                        customer_chatbot = gr.Chatbot(height=420, show_label=False, container=True)

                    with gr.Column(scale=1):
                        gr.HTML("""
                        <div class="agent-card">
                            <h3>🤖 Agent Info</h3>
                            <div class="agent-badge badge-customer">
                                <span>👥</span> 客户经营专家
                            </div>
                            <p style="color:var(--text-secondary);font-size:0.85rem;margin-top:0.5rem;">
                                客户画像 · 分群分析<br>
                                产品关联 · 资产预测<br>
                                流失预警
                            </p>
                            <div style="margin-top:1rem;padding-top:1rem;border-top:1px solid var(--border-subtle);">
                                <span style="color:var(--text-muted);font-size:0.8rem;">Model: qwen-turbo</span>
                            </div>
                        </div>
                        """)

                with gr.Row():
                    customer_input = gr.Textbox(
                        placeholder=f"输入客户经营问题...",
                        lines=2,
                        show_label=False,
                        container=True,
                        elem_classes=["input-container"]
                    )
                    customer_submit = gr.Button("发送", elem_classes=["btn-primary"])
                    customer_clear = gr.Button("清空", elem_classes=["btn-secondary"])

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
            with gr.TabItem(id="insurance", label="🛡️ 保险顾问助手"):
                with gr.Row():
                    with gr.Column(scale=3):
                        gr.HTML("""
                        <div class="chat-container">
                            <div style="display:flex;align-items:center;gap:8px;margin-bottom:1rem;">
                                <span class="status-dot status-online"></span>
                                <span style="color:var(--text-secondary);font-size:0.9rem;">保险顾问专家 · 在线</span>
                            </div>
                        </div>
                        """)
                        insurance_chatbot = gr.Chatbot(height=420, show_label=False, container=True)

                    with gr.Column(scale=1):
                        gr.HTML("""
                        <div class="agent-card">
                            <h3>🤖 Agent Info</h3>
                            <div class="agent-badge badge-insurance">
                                <span>🛡️</span> 保险顾问专家
                            </div>
                            <p style="color:var(--text-secondary);font-size:0.85rem;margin-top:0.5rem;">
                                条款查询 · 保单分析<br>
                                保单贷款计算<br>
                                保障范围解读
                            </p>
                            <div style="margin-top:1rem;padding-top:1rem;border-top:1px solid var(--border-subtle);">
                                <span style="color:var(--text-muted);font-size:0.8rem;">Model: qwen-turbo</span>
                            </div>
                        </div>
                        """)

                with gr.Row():
                    insurance_input = gr.Textbox(
                        placeholder=f"输入保险顾问问题...",
                        lines=2,
                        show_label=False,
                        container=True,
                        elem_classes=["input-container"]
                    )
                    insurance_submit = gr.Button("发送", elem_classes=["btn-primary"])
                    insurance_clear = gr.Button("清空", elem_classes=["btn-secondary"])

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
            with gr.TabItem(id="unified", label="🎯 统一平台"):
                with gr.Row():
                    with gr.Column(scale=3):
                        gr.HTML("""
                        <div class="chat-container">
                            <div style="display:flex;align-items:center;gap:8px;margin-bottom:1rem;">
                                <span class="status-dot status-online"></span>
                                <span style="color:var(--text-secondary);font-size:0.9rem;">智能协调者 · 自动调度专家</span>
                            </div>
                        </div>
                        """)
                        unified_chatbot = gr.Chatbot(height=420, show_label=False, container=True)

                    with gr.Column(scale=1):
                        gr.HTML("""
                        <div class="agent-card">
                            <h3>👤 客户信息</h3>
                            <div style="display:flex;flex-direction:column;gap:0.75rem;">
                                <div>
                                    <label style="color:var(--text-muted);font-size:0.8rem;">客户ID</label>
                                    <input type="text" value="C001" style="width:100%;background:var(--bg-secondary);border:1px solid var(--border-subtle);border-radius:8px;padding:8px 12px;color:var(--text-primary);margin-top:4px;">
                                </div>
                                <div>
                                    <label style="color:var(--text-muted);font-size:0.8rem;">客户姓名</label>
                                    <input type="text" value="王总" style="width:100%;background:var(--bg-secondary);border:1px solid var(--border-subtle);border-radius:8px;padding:8px 12px;color:var(--text-primary);margin-top:4px;">
                                </div>
                                <div>
                                    <label style="color:var(--text-muted);font-size:0.8rem;">总资产(元)</label>
                                    <input type="number" value="5000000" style="width:100%;background:var(--bg-secondary);border:1px solid var(--border-subtle);border-radius:8px;padding:8px 12px;color:var(--text-primary);margin-top:4px;">
                                </div>
                                <div>
                                    <label style="color:var(--text-muted);font-size:0.8rem;">风险等级</label>
                                    <select style="width:100%;background:var(--bg-secondary);border:1px solid var(--border-subtle);border-radius:8px;padding:8px 12px;color:var(--text-primary);margin-top:4px;">
                                        <option>R1 - 保守型</option>
                                        <option>R2 - 稳健型</option>
                                        <option>R3 - 平衡型</option>
                                        <option selected>R4 - 成长型</option>
                                        <option>R5 - 进取型</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        """)

                gr.HTML("""
                <div style="background:var(--bg-card);border:1px solid var(--border-subtle);border-radius:12px;padding:1rem;margin-top:1rem;display:flex;gap:2rem;flex-wrap:wrap;">
                    <div style="flex:1;min-width:150px;">
                        <span style="color:var(--accent-gold);font-weight:600;">📈 投资分析</span>
                        <p style="color:var(--text-muted);font-size:0.8rem;margin-top:4px;">持仓·盈亏·预测</p>
                    </div>
                    <div style="flex:1;min-width:150px;">
                        <span style="color:var(--accent-emerald);font-weight:600;">👥 客户经营</span>
                        <p style="color:var(--text-muted);font-size:0.8rem;margin-top:4px;">画像·分群·关联</p>
                    </div>
                    <div style="flex:1;min-width:150px;">
                        <span style="color:var(--accent-sapphire);font-weight:600;">🛡️ 保险顾问</span>
                        <p style="color:var(--text-muted);font-size:0.8rem;margin-top:4px;">条款·保单·贷款</p>
                    </div>
                </div>
                """)

                with gr.Row():
                    unified_input = gr.Textbox(
                        placeholder=f"描述您的金融需求，协调者将自动调度专家处理...",
                        lines=2,
                        show_label=False,
                        container=True,
                        elem_classes=["input-container"]
                    )
                    unified_submit = gr.Button("发送", elem_classes=["btn-primary"])
                    unified_clear = gr.Button("清空", elem_classes=["btn-secondary"])

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

        # Footer
        gr.HTML("""
        <div style="text-align:center;padding:1.5rem;color:var(--text-muted);font-size:0.8rem;border-top:1px solid var(--border-subtle);margin-top:2rem;">
            <span>FinAgent Unified Platform</span> · <span>Powered by qwen-agent</span>
        </div>
        """)

    print("金融智能顾问统一平台 WebUI 准备就绪...")
    try:
        demo.launch(server_name="0.0.0.0", server_port=7861, show_error=True)
    except Exception as e:
        print(f"启动服务 (后台运行): {e}")
        import time
        time.sleep(3600)


if __name__ == '__main__':
    app_gui()
