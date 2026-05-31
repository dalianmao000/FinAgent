"""WebUI for FinAgent Unified - Bloomberg Terminal Luxe."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv

from ..specialists.investment.agent import InvestmentAgent
from ..specialists.customer.agent import CustomerAgent
from ..specialists.insurance.agent import InsuranceAgent

load_dotenv()


def init_investment_agent():
    return InvestmentAgent(session_id='webui-investment')


def init_customer_agent():
    return CustomerAgent(session_id='webui-customer')


def init_insurance_agent():
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

CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=DM+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-void: #080b12;
    --bg-deep: #0d1117;
    --bg-surface: #161b22;
    --bg-elevated: #1c2128;
    --bg-hover: #252b33;
    --gold: #c9a227;
    --gold-light: #e8c547;
    --gold-dim: #9a7b1c;
    --gold-glow: rgba(201,162,39,0.15);
    --emerald: #2dd4bf;
    --emerald-dim: #14b8a6;
    --sapphire: #60a5fa;
    --sapphire-dim: #3b82f6;
    --text-bright: #f0f6fc;
    --text-primary: #c9d1d9;
    --text-secondary: #8b949e;
    --text-muted: #6e7681;
    --border: rgba(240,246,252,0.1);
    --border-accent: rgba(201,162,39,0.3);
    --radius-sm: 4px;
    --radius-md: 8px;
    --radius-lg: 12px;
    --radius-xl: 16px;
}

* {
    font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    -webkit-font-smoothing: antialiased;
}

body {
    background: var(--bg-void);
    color: var(--text-primary);
}

.header-section {
    text-align: center;
    padding: 2rem 1rem 1.5rem;
    background: linear-gradient(180deg, var(--bg-deep) 0%, transparent 100%);
    border-bottom: 1px solid var(--border);
}

.main-title {
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-size: 2.75rem !important;
    font-weight: 600 !important;
    color: var(--gold-light) !important;
    letter-spacing: 0.06em;
    margin-bottom: 0.5rem !important;
}

.subtitle {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.7rem !important;
    color: var(--text-muted);
    letter-spacing: 0.2em;
    text-transform: uppercase;
}

.chat-panel {
    background: var(--bg-deep);
    border: 1px solid var(--border);
    border-radius: var(--radius-xl);
    min-height: 520px;
}

.chat-header {
    padding: 0.875rem 1.25rem;
    background: var(--bg-surface);
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 0.75rem;
    border-radius: var(--radius-xl) var(--radius-xl) 0 0;
}

.status-indicator {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--emerald);
    box-shadow: 0 0 10px var(--emerald);
    animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.6; }
}

.chat-title {
    font-size: 0.85rem;
    font-weight: 500;
    color: var(--text-primary);
}

.agent-card {
    background: var(--bg-deep);
    border: 1px solid var(--border);
    border-radius: var(--radius-xl);
    padding: 1.25rem;
    transition: all 0.2s ease;
}

.agent-card:hover {
    border-color: var(--border-accent);
}

.agent-card-header {
    display: flex;
    align-items: center;
    gap: 0.875rem;
    margin-bottom: 1rem;
    padding-bottom: 0.875rem;
    border-bottom: 1px solid var(--border);
}

.agent-icon {
    width: 42px;
    height: 42px;
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
}

.icon-investment { background: linear-gradient(135deg, var(--gold-dim), var(--gold)); }
.icon-customer { background: linear-gradient(135deg, var(--emerald-dim), var(--emerald)); color: var(--bg-void); }
.icon-insurance { background: linear-gradient(135deg, var(--sapphire-dim), var(--sapphire)); color: var(--bg-void); }

.agent-name {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-bright);
    margin-bottom: 0.125rem;
}

.agent-domain {
    font-size: 0.7rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.agent-capabilities {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.capability {
    font-size: 0.85rem;
    color: var(--text-secondary);
    padding-left: 0.75rem;
    border-left: 2px solid var(--gold-dim);
}

.agent-meta {
    margin-top: 1rem;
    padding-top: 0.75rem;
    border-top: 1px solid var(--border);
    font-size: 0.7rem;
    color: var(--text-muted);
    font-family: 'JetBrains Mono', monospace;
}

.input-area {
    padding: 1rem;
    background: var(--bg-surface);
    border-top: 1px solid var(--border);
    border-radius: 0 0 var(--radius-xl) var(--radius-xl);
}

.input-row {
    display: flex;
    gap: 0.75rem;
}

.input-field {
    flex: 1;
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
    padding: 0.75rem 1rem !important;
    font-size: 0.9rem !important;
    transition: all 0.2s ease !important;
}

.input-field:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px var(--gold-glow) !important;
    outline: none !important;
}

.btn-send {
    background: linear-gradient(135deg, var(--gold-dim), var(--gold)) !important;
    color: var(--bg-void) !important;
    border: none !important;
    border-radius: var(--radius-md) !important;
    padding: 0.75rem 1.5rem !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    transition: all 0.2s ease !important;
}

.btn-send:hover {
    box-shadow: 0 4px 16px rgba(201,162,39,0.3);
    transform: translateY(-1px);
}

.btn-clear {
    background: var(--bg-elevated) !important;
    color: var(--text-secondary) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    padding: 0.75rem 1.25rem !important;
    font-size: 0.85rem !important;
}

.btn-clear:hover {
    background: var(--bg-hover) !important;
    color: var(--text-primary) !important;
}

.examples-label {
    font-size: 0.7rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin: 1rem 0 0.5rem;
    display: block;
}

.example-btn {
    display: inline-block;
    background: var(--bg-surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-secondary) !important;
    padding: 0.4rem 0.875rem !important;
    border-radius: 20px !important;
    font-size: 0.75rem !important;
    margin: 0.25rem !important;
    cursor: pointer;
    transition: all 0.15s ease !important;
}

.example-btn:hover {
    background: var(--bg-hover) !important;
    border-color: var(--gold) !important;
    color: var(--gold) !important;
}

.domain-banner {
    background: linear-gradient(135deg, var(--bg-surface), var(--bg-elevated));
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1rem;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.75rem;
    margin-top: 1rem;
}

.domain-item {
    text-align: center;
    padding: 0.75rem 0.5rem;
    border-radius: var(--radius-md);
    background: var(--bg-surface);
}

.domain-icon { font-size: 1.25rem; margin-bottom: 0.25rem; }
.domain-name { font-size: 0.75rem; font-weight: 600; margin-bottom: 0.125rem; }
.domain-tags { font-size: 0.65rem; color: var(--text-muted); }

.domain-investment .domain-name { color: var(--gold); }
.domain-customer .domain-name { color: var(--emerald); }
.domain-insurance .domain-name { color: var(--sapphire); }

.customer-form {
    background: var(--bg-deep);
    border: 1px solid var(--border);
    border-radius: var(--radius-xl);
    padding: 1.25rem;
}

.form-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--text-bright);
    margin-bottom: 1rem;
}

.form-group { margin-bottom: 0.75rem; }

.form-label {
    display: block;
    font-size: 0.7rem;
    color: var(--text-muted);
    margin-bottom: 0.25rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.form-input {
    width: 100%;
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    padding: 0.5rem 0.75rem !important;
    font-size: 0.85rem !important;
}

.form-select {
    width: 100%;
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    padding: 0.5rem 0.75rem !important;
    font-size: 0.85rem !important;
}

.footer {
    text-align: center;
    padding: 1.25rem;
    color: var(--text-muted);
    font-size: 0.7rem;
    border-top: 1px solid var(--border);
    margin-top: 1.5rem;
}

.footer span { color: var(--gold-dim); }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb { background: var(--bg-hover); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }
"""


def app_gui():
    try:
        import gradio as gr
    except ImportError:
        print("Gradio not installed. Run: pip install gradio")
        return

    investment_bot = init_investment_agent()
    customer_bot = init_customer_agent()
    insurance_bot = init_insurance_agent()

    with gr.Blocks(css=CUSTOM_CSS, title="金融智能顾问统一平台") as demo:
        gr.HTML("""
        <div class="header-section">
            <h1 class="main-title">金融智能顾问</h1>
            <p class="subtitle">Unified Financial Intelligence</p>
        </div>
        """)

        with gr.Tabs():
            with gr.TabItem("📈 投资分析"):
                with gr.Row():
                    with gr.Column(scale=3):
                        gr.HTML('<div class="chat-panel"><div class="chat-header"><div class="status-indicator"></div><span class="chat-title">投资分析专家</span></div></div>')
                        investment_chatbot = gr.Chatbot(height=400, show_label=False)

                        gr.HTML('<span class="examples-label">示例问题</span>')
                        for ex in INVESTMENT_EXAMPLES:
                            gr.HTML(f'<button class="example-btn">{ex}</button>')

                        gr.HTML('<div class="input-area"><div class="input-row">')
                        investment_input = gr.Textbox(placeholder="输入投资分析问题...", lines=1, show_label=False, container=False)
                        investment_send = gr.Button("发送", elem_classes=["btn-send"])
                        investment_clear = gr.Button("清空", elem_classes=["btn-clear"])
                        gr.HTML('</div></div>')

                    with gr.Column(scale=1):
                        gr.HTML("""
                        <div class="agent-card">
                            <div class="agent-card-header">
                                <div class="agent-icon icon-investment">📈</div>
                                <div><div class="agent-name">投资分析</div><div class="agent-domain">Investment</div></div>
                            </div>
                            <div class="agent-capabilities">
                                <div class="capability">持仓查询</div>
                                <div class="capability">盈亏计算</div>
                                <div class="capability">股价预测</div>
                                <div class="capability">布林带检测</div>
                                <div class="capability">周期性分析</div>
                            </div>
                            <div class="agent-meta">qwen-turbo</div>
                        </div>
                        """)

                def investment_chat(msg, hist):
                    if not msg.strip():
                        return hist, ""
                    try:
                        resp = investment_bot.process(msg)
                        hist = hist + [(msg, resp)]
                    except Exception as e:
                        hist = hist + [(msg, f"错误: {str(e)}")]
                    return hist, ""

                investment_send.click(investment_chat, [investment_input, investment_chatbot], [investment_chatbot, investment_input])
                investment_input.submit(investment_chat, [investment_input, investment_chatbot], [investment_chatbot, investment_input])
                investment_clear.click(lambda: ([], ""), outputs=[investment_chatbot, investment_input])

            with gr.TabItem("👥 客户经营"):
                with gr.Row():
                    with gr.Column(scale=3):
                        gr.HTML('<div class="chat-panel"><div class="chat-header"><div class="status-indicator"></div><span class="chat-title">客户经营专家</span></div></div>')
                        customer_chatbot = gr.Chatbot(height=400, show_label=False)

                        gr.HTML('<span class="examples-label">示例问题</span>')
                        for ex in CUSTOMER_EXAMPLES[:4]:
                            gr.HTML(f'<button class="example-btn">{ex}</button>')

                        gr.HTML('<div class="input-area"><div class="input-row">')
                        customer_input = gr.Textbox(placeholder="输入客户经营问题...", lines=1, show_label=False, container=False)
                        customer_send = gr.Button("发送", elem_classes=["btn-send"])
                        customer_clear = gr.Button("清空", elem_classes=["btn-clear"])
                        gr.HTML('</div></div>')

                    with gr.Column(scale=1):
                        gr.HTML("""
                        <div class="agent-card">
                            <div class="agent-card-header">
                                <div class="agent-icon icon-customer">👥</div>
                                <div><div class="agent-name">客户经营</div><div class="agent-domain">Customer</div></div>
                            </div>
                            <div class="agent-capabilities">
                                <div class="capability">客户画像</div>
                                <div class="capability">分群分析</div>
                                <div class="capability">产品关联</div>
                                <div class="capability">资产预测</div>
                                <div class="capability">流失预警</div>
                            </div>
                            <div class="agent-meta">qwen-turbo</div>
                        </div>
                        """)

                def customer_chat(msg, hist):
                    if not msg.strip():
                        return hist, ""
                    try:
                        resp = customer_bot.process(msg)
                        hist = hist + [(msg, resp)]
                    except Exception as e:
                        hist = hist + [(msg, f"错误: {str(e)}")]
                    return hist, ""

                customer_send.click(customer_chat, [customer_input, customer_chatbot], [customer_chatbot, customer_input])
                customer_input.submit(customer_chat, [customer_input, customer_chatbot], [customer_chatbot, customer_input])
                customer_clear.click(lambda: ([], ""), outputs=[customer_chatbot, customer_input])

            with gr.TabItem("🛡️ 保险顾问"):
                with gr.Row():
                    with gr.Column(scale=3):
                        gr.HTML('<div class="chat-panel"><div class="chat-header"><div class="status-indicator"></div><span class="chat-title">保险顾问专家</span></div></div>')
                        insurance_chatbot = gr.Chatbot(height=400, show_label=False)

                        gr.HTML('<span class="examples-label">示例问题</span>')
                        for ex in INSURANCE_EXAMPLES:
                            gr.HTML(f'<button class="example-btn">{ex}</button>')

                        gr.HTML('<div class="input-area"><div class="input-row">')
                        insurance_input = gr.Textbox(placeholder="输入保险顾问问题...", lines=1, show_label=False, container=False)
                        insurance_send = gr.Button("发送", elem_classes=["btn-send"])
                        insurance_clear = gr.Button("清空", elem_classes=["btn-clear"])
                        gr.HTML('</div></div>')

                    with gr.Column(scale=1):
                        gr.HTML("""
                        <div class="agent-card">
                            <div class="agent-card-header">
                                <div class="agent-icon icon-insurance">🛡️</div>
                                <div><div class="agent-name">保险顾问</div><div class="agent-domain">Insurance</div></div>
                            </div>
                            <div class="agent-capabilities">
                                <div class="capability">条款查询</div>
                                <div class="capability">保单分析</div>
                                <div class="capability">贷款计算</div>
                                <div class="capability">保障解读</div>
                            </div>
                            <div class="agent-meta">qwen-turbo</div>
                        </div>
                        """)

                def insurance_chat(msg, hist):
                    if not msg.strip():
                        return hist, ""
                    try:
                        resp = insurance_bot.process(msg)
                        hist = hist + [(msg, resp)]
                    except Exception as e:
                        hist = hist + [(msg, f"错误: {str(e)}")]
                    return hist, ""

                insurance_send.click(insurance_chat, [insurance_input, insurance_chatbot], [insurance_chatbot, insurance_input])
                insurance_input.submit(insurance_chat, [insurance_input, insurance_chatbot], [insurance_chatbot, insurance_input])
                insurance_clear.click(lambda: ([], ""), outputs=[insurance_chatbot, insurance_input])

            with gr.TabItem("🎯 统一平台"):
                with gr.Row():
                    with gr.Column(scale=3):
                        gr.HTML('<div class="chat-panel"><div class="chat-header"><div class="status-indicator"></div><span class="chat-title">智能协调者 · 自动调度</span></div></div>')
                        unified_chatbot = gr.Chatbot(height=300, show_label=False)

                        gr.HTML("""
                        <div class="domain-banner">
                            <div class="domain-item domain-investment"><div class="domain-icon">📈</div><div class="domain-name">投资分析</div><div class="domain-tags">持仓·盈亏·预测</div></div>
                            <div class="domain-item domain-customer"><div class="domain-icon">👥</div><div class="domain-name">客户经营</div><div class="domain-tags">画像·分群·关联</div></div>
                            <div class="domain-item domain-insurance"><div class="domain-icon">🛡️</div><div class="domain-name">保险顾问</div><div class="domain-tags">条款·保单·贷款</div></div>
                        </div>
                        """)

                        gr.HTML('<span class="examples-label">示例问题</span>')
                        for ex in ["查询持仓情况", "客户亏损能办保单贷款吗？", "高净值客户有哪些"]:
                            gr.HTML(f'<button class="example-btn">{ex}</button>')

                        gr.HTML('<div class="input-area"><div class="input-row">')
                        unified_input = gr.Textbox(placeholder="描述您的金融需求，协调者将自动调度...", lines=1, show_label=False, container=False)
                        unified_send = gr.Button("发送", elem_classes=["btn-send"])
                        unified_clear = gr.Button("清空", elem_classes=["btn-clear"])
                        gr.HTML('</div></div>')

                    with gr.Column(scale=1):
                        gr.HTML("""
                        <div class="customer-form">
                            <div class="form-title">客户信息</div>
                            <div class="form-group"><label class="form-label">客户ID</label><input type="text" class="form-input" value="C001"></div>
                            <div class="form-group"><label class="form-label">客户姓名</label><input type="text" class="form-input" value="王总"></div>
                            <div class="form-group"><label class="form-label">总资产 (元)</label><input type="number" class="form-input" value="5000000"></div>
                            <div class="form-group">
                                <label class="form-label">风险等级</label>
                                <select class="form-select">
                                    <option>R1</option><option>R2</option><option>R3</option><option selected>R4</option><option>R5</option>
                                </select>
                            </div>
                        </div>
                        """)

                def unified_chat(msg, hist):
                    if not msg.strip():
                        return hist, ""
                    try:
                        import requests
                        resp = requests.post("http://localhost:5000/api/v1/chat", json={"message": msg, "session_id": "webui-unified"}, timeout=60).json().get("response", "无响应")
                        hist = hist + [(msg, resp)]
                    except Exception as e:
                        hist = hist + [(msg, f"错误: {str(e)}")]
                    return hist, ""

                unified_send.click(unified_chat, [unified_input, unified_chatbot], [unified_chatbot, unified_input])
                unified_input.submit(unified_chat, [unified_input, unified_chatbot], [unified_chatbot, unified_input])
                unified_clear.click(lambda: ([], ""), outputs=[unified_chatbot, unified_input])

        gr.HTML('<div class="footer">FinAgent Unified · <span>Powered by qwen-agent</span></div>')

    print("金融智能顾问统一平台 WebUI 准备就绪...")
    try:
        demo.launch(server_name="0.0.0.0", server_port=7861, show_error=True)
    except Exception as e:
        print(f"启动服务: {e}")
        import time
        time.sleep(3600)


if __name__ == '__main__':
    app_gui()
