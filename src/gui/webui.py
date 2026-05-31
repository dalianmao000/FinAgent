"""WebUI for FinAgent Unified - Clean Ocean Shell."""
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
]

INSURANCE_EXAMPLES = [
    '查询保险条款：重疾险保障范围',
    '查询保险条款：意外医疗报销比例',
    '保单贷款能贷多少钱？',
    '查询万能险的收益规则',
]

CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap');

:root {
    --bg-shell: #f8f6f3;
    --bg-white: #ffffff;
    --bg-pearl: #faf9f7;
    --bg-cloud: #f0eeeb;

    --ocean: #4a90a4;
    --ocean-light: #6bb3c9;
    --ocean-dark: #357a8a;
    --ocean-glow: rgba(74,144,164,0.12);

    --gold: #c9a227;
    --gold-light: #e8c547;
    --gold-dim: #9a7b1c;

    --rose: #d4a5a5;
    --sage: #a5c4b5;

    --text-primary: #2c3e50;
    --text-secondary: #5a6c7d;
    --text-muted: #8a9cad;

    --border: rgba(44,62,80,0.08);
    --border-light: rgba(44,62,80,0.04);
    --shadow: 0 4px 24px rgba(44,62,80,0.06);
    --shadow-hover: 0 8px 32px rgba(44,62,80,0.1);

    --radius-sm: 6px;
    --radius-md: 10px;
    --radius-lg: 16px;
    --radius-xl: 20px;
}

* {
    font-family: 'Inter', 'Noto Serif SC', -apple-system, sans-serif;
    -webkit-font-smoothing: antialiased;
}

body {
    background: var(--bg-shell);
    color: var(--text-primary);
    min-height: 100vh;
}

.header-section {
    text-align: center;
    padding: 2.5rem 1.5rem 2rem;
    background: linear-gradient(180deg, var(--bg-white) 0%, var(--bg-shell) 100%);
    border-bottom: 1px solid var(--border);
}

.main-title {
    font-family: 'Noto Serif SC', serif !important;
    font-size: 2.5rem !important;
    font-weight: 600 !important;
    color: var(--ocean-dark) !important;
    letter-spacing: 0.04em;
    margin-bottom: 0.5rem !important;
}

.subtitle {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.75rem !important;
    color: var(--text-muted);
    letter-spacing: 0.15em;
    text-transform: uppercase;
}

.tabs-container {
    background: var(--bg-white);
    border-bottom: 1px solid var(--border);
    padding: 0;
}

.tab-button {
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    color: var(--text-secondary) !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    padding: 1rem 1.5rem !important;
    transition: all 0.2s ease !important;
}

.tab-button:hover {
    color: var(--ocean) !important;
    background: var(--bg-pearl) !important;
}

.tab-button.selected {
    color: var(--ocean) !important;
    border-bottom-color: var(--ocean) !important;
    background: var(--bg-pearl) !important;
}

.main-content {
    max-width: 1400px;
    margin: 0 auto;
    padding: 2rem 1.5rem;
}

.chat-section {
    display: grid;
    grid-template-columns: 1fr 280px;
    gap: 1.5rem;
    margin-bottom: 1.5rem;
}

@media (max-width: 1024px) {
    .chat-section { grid-template-columns: 1fr; }
}

.chat-panel {
    background: var(--bg-white);
    border-radius: var(--radius-xl);
    box-shadow: var(--shadow);
    overflow: hidden;
    min-height: 480px;
}

.chat-header {
    padding: 1rem 1.25rem;
    background: linear-gradient(135deg, var(--ocean) 0%, var(--ocean-light) 100%);
    color: white;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: white;
    box-shadow: 0 0 8px rgba(255,255,255,0.5);
    animation: blink 2s ease-in-out infinite;
}

@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.chat-title {
    font-size: 0.9rem;
    font-weight: 500;
}

.chat-messages {
    padding: 1.25rem;
    min-height: 360px;
    max-height: 50vh;
    overflow-y: auto;
}

.message-wrap {
    margin-bottom: 1rem;
    animation: slideIn 0.3s ease;
}

@keyframes slideIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.message-user {
    background: linear-gradient(135deg, var(--ocean) 0%, var(--ocean-dark) 100%);
    color: white !important;
    padding: 0.75rem 1rem !important;
    border-radius: var(--radius-lg) var(--radius-lg) var(--radius-sm) var(--radius-lg) !important;
    max-width: 80%;
    margin-left: auto;
    font-size: 0.9rem;
    line-height: 1.5;
}

.message-bot {
    background: var(--bg-pearl) !important;
    border: 1px solid var(--border-light) !important;
    color: var(--text-primary) !important;
    padding: 1rem 1.25rem !important;
    border-radius: var(--radius-lg) var(--radius-lg) var(--radius-lg) var(--radius-sm) !important;
    max-width: 85%;
    font-size: 0.9rem;
    line-height: 1.7;
}

.input-section {
    padding: 1rem 1.25rem;
    background: var(--bg-pearl);
    border-top: 1px solid var(--border);
}

.input-row {
    display: flex;
    gap: 0.75rem;
    align-items: flex-end;
}

.input-field {
    flex: 1;
    background: var(--bg-white) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
    padding: 0.875rem 1rem !important;
    font-size: 0.9rem !important;
    transition: all 0.2s ease !important;
}

.input-field:focus {
    border-color: var(--ocean) !important;
    box-shadow: 0 0 0 3px var(--ocean-glow) !important;
    outline: none !important;
}

.btn-send {
    background: linear-gradient(135deg, var(--ocean) 0%, var(--ocean-dark) 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-md) !important;
    padding: 0.875rem 1.5rem !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 12px rgba(74,144,164,0.25);
}

.btn-send:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(74,144,164,0.35);
}

.btn-clear {
    background: var(--bg-white) !important;
    color: var(--text-secondary) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    padding: 0.875rem 1.25rem !important;
    font-size: 0.85rem !important;
}

.btn-clear:hover {
    background: var(--bg-cloud) !important;
    color: var(--text-primary) !important;
}

/* Sidebar */
.sidebar-card {
    background: var(--bg-white);
    border-radius: var(--radius-xl);
    box-shadow: var(--shadow);
    overflow: hidden;
    height: fit-content;
}

.sidebar-header {
    padding: 1rem 1.25rem;
    background: linear-gradient(135deg, var(--ocean) 0%, var(--ocean-light) 100%);
    color: white;
}

.sidebar-title {
    font-size: 0.9rem;
    font-weight: 600;
}

.agent-info {
    padding: 1.25rem;
}

.agent-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: var(--bg-pearl);
    padding: 0.5rem 0.875rem;
    border-radius: 20px;
    font-size: 0.8rem;
    color: var(--ocean);
    margin-bottom: 1rem;
}

.agent-capabilities {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.capability {
    font-size: 0.85rem;
    color: var(--text-secondary);
    padding: 0.375rem 0;
    border-bottom: 1px solid var(--border-light);
}

.capability:last-child { border-bottom: none; }

.agent-meta {
    margin-top: 1rem;
    padding-top: 0.875rem;
    border-top: 1px solid var(--border);
    font-size: 0.7rem;
    color: var(--text-muted);
    font-family: 'Inter', monospace;
}

/* Examples Section - Collapsible */
.examples-section {
    background: var(--bg-white);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow);
    margin-top: 1rem;
    overflow: hidden;
}

.examples-toggle {
    width: 100%;
    background: var(--bg-white);
    border: none;
    padding: 0.875rem 1.25rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    cursor: pointer;
    font-size: 0.85rem;
    color: var(--text-secondary);
    transition: all 0.2s ease;
}

.examples-toggle:hover {
    background: var(--bg-pearl);
    color: var(--ocean);
}

.examples-toggle-icon {
    transition: transform 0.3s ease;
}

.examples-toggle-icon.open {
    transform: rotate(180deg);
}

.examples-content {
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.3s ease;
    padding: 0 1.25rem;
}

.examples-content.open {
    max-height: 300px;
    padding: 0.75rem 1.25rem 1.25rem;
}

.example-chip {
    display: inline-block;
    background: var(--bg-pearl);
    border: 1px solid var(--border);
    color: var(--text-secondary);
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-size: 0.8rem;
    margin: 0.25rem;
    cursor: pointer;
    transition: all 0.15s ease;
}

.example-chip:hover {
    background: var(--ocean-glow);
    border-color: var(--ocean);
    color: var(--ocean);
}

/* Domain Banner */
.domain-banner {
    background: linear-gradient(135deg, var(--bg-white) 0%, var(--bg-pearl) 100%);
    border-radius: var(--radius-lg);
    padding: 1.25rem;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 1rem;
    box-shadow: var(--shadow);
}

.domain-item {
    text-align: center;
    padding: 0.75rem;
}

.domain-icon { font-size: 1.5rem; margin-bottom: 0.375rem; }

.domain-name {
    font-size: 0.8rem;
    font-weight: 600;
    margin-bottom: 0.125rem;
}

.domain-tags {
    font-size: 0.7rem;
    color: var(--text-muted);
}

.domain-investment .domain-name { color: var(--gold-dim); }
.domain-customer .domain-name { color: var(--ocean); }
.domain-insurance .domain-name { color: var(--rose); }

/* Customer Form */
.customer-form {
    background: var(--bg-white);
    border-radius: var(--radius-xl);
    padding: 1.25rem;
    box-shadow: var(--shadow);
}

.form-title {
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--border);
}

.form-group { margin-bottom: 0.75rem; }

.form-label {
    display: block;
    font-size: 0.7rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.25rem;
}

.form-input {
    width: 100%;
    background: var(--bg-pearl) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    padding: 0.5rem 0.75rem !important;
    font-size: 0.85rem !important;
}

.form-select {
    width: 100%;
    background: var(--bg-pearl) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    padding: 0.5rem 0.75rem !important;
    font-size: 0.85rem !important;
}

/* Footer */
.footer {
    text-align: center;
    padding: 1.5rem;
    color: var(--text-muted);
    font-size: 0.75rem;
    border-top: 1px solid var(--border);
    margin-top: 2rem;
}

.footer span { color: var(--ocean); }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-pearl); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }
"""


JAVASCRIPT = """
<script>
function toggleExamples(id) {
    var content = document.getElementById(id);
    var icon = document.getElementById(id + '-icon');
    if (content.classList.contains('open')) {
        content.classList.remove('open');
        icon.classList.remove('open');
    } else {
        content.classList.add('open');
        icon.classList.add('open');
    }
}
</script>
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
        gr.HTML(JAVASCRIPT)
        gr.HTML("""
        <div class="header-section">
            <h1 class="main-title">金融智能顾问</h1>
            <p class="subtitle">Unified Financial Intelligence</p>
        </div>
        """)

        with gr.Tabs():
            with gr.TabItem("📈 投资分析"):
                with gr.Column():
                    with gr.Row():
                        with gr.Column(scale=3):
                            gr.HTML('<div class="chat-panel"><div class="chat-header"><div class="status-dot"></div><span class="chat-title">投资分析专家</span></div></div>')
                            investment_chatbot = gr.Chatbot(height=400, show_label=False)

                        with gr.Column(scale=1):
                            gr.HTML("""
                            <div class="sidebar-card">
                                <div class="sidebar-header">
                                    <div class="sidebar-title">Agent Info</div>
                                </div>
                                <div class="agent-info">
                                    <div class="agent-badge">📈 投资分析</div>
                                    <div class="agent-capabilities">
                                        <div class="capability">持仓查询</div>
                                        <div class="capability">盈亏计算</div>
                                        <div class="capability">股价预测</div>
                                        <div class="capability">布林带检测</div>
                                        <div class="capability">周期性分析</div>
                                    </div>
                                    <div class="agent-meta">qwen-turbo</div>
                                </div>
                            </div>
                            """)

                    gr.HTML("""
                    <div class="examples-section">
                        <button class="examples-toggle" onclick="toggleExamples('investment-examples')">
                            <span>📋 示例问题</span>
                            <span class="examples-toggle-icon" id="investment-examples-icon">▼</span>
                        </button>
                        <div class="examples-content" id="investment-examples">
                            <button class="example-chip">查询我的持仓情况</button>
                            <button class="example-chip">贵州茅台亏了多少？</button>
                            <button class="example-chip">预测贵州茅台未来10天股价</button>
                            <button class="example-chip">检测贵州茅台近一年超买超卖点</button>
                            <button class="example-chip">分析五粮液近一年周期性规律</button>
                        </div>
                    </div>
                    """)

                    gr.HTML('<div class="input-section"><div class="input-row">')
                    investment_input = gr.Textbox(placeholder="输入投资分析问题...", lines=1, show_label=False, container=False)
                    gr.Button("发送", elem_classes=["btn-send"])
                    gr.Button("清空", elem_classes=["btn-clear"])
                    gr.HTML('</div></div>')

                    def investment_chat(msg, hist):
                        if not msg.strip():
                            return hist, ""
                        try:
                            resp = investment_bot.process(msg)
                            hist = hist + [(msg, resp)]
                        except Exception as e:
                            hist = hist + [(msg, f"错误: {str(e)}")]
                        return hist, ""

                    investment_chatbot.change(investment_chat, [investment_input, investment_chatbot], [investment_chatbot, investment_input])

            with gr.TabItem("👥 客户经营"):
                with gr.Column():
                    with gr.Row():
                        with gr.Column(scale=3):
                            gr.HTML('<div class="chat-panel"><div class="chat-header"><div class="status-dot"></div><span class="chat-title">客户经营专家</span></div></div>')
                            customer_chatbot = gr.Chatbot(height=400, show_label=False)

                        with gr.Column(scale=1):
                            gr.HTML("""
                            <div class="sidebar-card">
                                <div class="sidebar-header">
                                    <div class="sidebar-title">Agent Info</div>
                                </div>
                                <div class="agent-info">
                                    <div class="agent-badge">👥 客户经营</div>
                                    <div class="agent-capabilities">
                                        <div class="capability">客户画像</div>
                                        <div class="capability">分群分析</div>
                                        <div class="capability">产品关联</div>
                                        <div class="capability">资产预测</div>
                                        <div class="capability">流失预警</div>
                                    </div>
                                    <div class="agent-meta">qwen-turbo</div>
                                </div>
                            </div>
                            """)

                    gr.HTML("""
                    <div class="examples-section">
                        <button class="examples-toggle" onclick="toggleExamples('customer-examples')">
                            <span>📋 示例问题</span>
                            <span class="examples-toggle-icon" id="customer-examples-icon">▼</span>
                        </button>
                        <div class="examples-content" id="customer-examples">
                            <button class="example-chip">我行目前有多少客户？</button>
                            <button class="example-chip">客户的平均资产是多少？</button>
                            <button class="example-chip">高价值客户预测</button>
                            <button class="example-chip">产品关联规则分析</button>
                        </div>
                    </div>
                    """)

                    gr.HTML('<div class="input-section"><div class="input-row">')
                    customer_input = gr.Textbox(placeholder="输入客户经营问题...", lines=1, show_label=False, container=False)
                    gr.Button("发送", elem_classes=["btn-send"])
                    gr.Button("清空", elem_classes=["btn-clear"])
                    gr.HTML('</div></div>')

                    def customer_chat(msg, hist):
                        if not msg.strip():
                            return hist, ""
                        try:
                            resp = customer_bot.process(msg)
                            hist = hist + [(msg, resp)]
                        except Exception as e:
                            hist = hist + [(msg, f"错误: {str(e)}")]
                        return hist, ""

                    customer_chatbot.change(customer_chat, [customer_input, customer_chatbot], [customer_chatbot, customer_input])

            with gr.TabItem("🛡️ 保险顾问"):
                with gr.Column():
                    with gr.Row():
                        with gr.Column(scale=3):
                            gr.HTML('<div class="chat-panel"><div class="chat-header"><div class="status-dot"></div><span class="chat-title">保险顾问专家</span></div></div>')
                            insurance_chatbot = gr.Chatbot(height=400, show_label=False)

                        with gr.Column(scale=1):
                            gr.HTML("""
                            <div class="sidebar-card">
                                <div class="sidebar-header">
                                    <div class="sidebar-title">Agent Info</div>
                                </div>
                                <div class="agent-info">
                                    <div class="agent-badge">🛡️ 保险顾问</div>
                                    <div class="agent-capabilities">
                                        <div class="capability">条款查询</div>
                                        <div class="capability">保单分析</div>
                                        <div class="capability">贷款计算</div>
                                        <div class="capability">保障解读</div>
                                    </div>
                                    <div class="agent-meta">qwen-turbo</div>
                                </div>
                            </div>
                            """)

                    gr.HTML("""
                    <div class="examples-section">
                        <button class="examples-toggle" onclick="toggleExamples('insurance-examples')">
                            <span>📋 示例问题</span>
                            <span class="examples-toggle-icon" id="insurance-examples-icon">▼</span>
                        </button>
                        <div class="examples-content" id="insurance-examples">
                            <button class="example-chip">查询重疾险保障范围</button>
                            <button class="example-chip">意外医疗报销比例</button>
                            <button class="example-chip">保单贷款能贷多少钱</button>
                            <button class="example-chip">万能险收益规则</button>
                        </div>
                    </div>
                    """)

                    gr.HTML('<div class="input-section"><div class="input-row">')
                    insurance_input = gr.Textbox(placeholder="输入保险顾问问题...", lines=1, show_label=False, container=False)
                    gr.Button("发送", elem_classes=["btn-send"])
                    gr.Button("清空", elem_classes=["btn-clear"])
                    gr.HTML('</div></div>')

                    def insurance_chat(msg, hist):
                        if not msg.strip():
                            return hist, ""
                        try:
                            resp = insurance_bot.process(msg)
                            hist = hist + [(msg, resp)]
                        except Exception as e:
                            hist = hist + [(msg, f"错误: {str(e)}")]
                        return hist, ""

                    insurance_chatbot.change(insurance_chat, [insurance_input, insurance_chatbot], [insurance_chatbot, insurance_input])

            with gr.TabItem("🎯 统一平台"):
                with gr.Column():
                    gr.HTML("""
                    <div class="domain-banner">
                        <div class="domain-item domain-investment">
                            <div class="domain-icon">📈</div>
                            <div class="domain-name">投资分析</div>
                            <div class="domain-tags">持仓·盈亏·预测</div>
                        </div>
                        <div class="domain-item domain-customer">
                            <div class="domain-icon">👥</div>
                            <div class="domain-name">客户经营</div>
                            <div class="domain-tags">画像·分群·关联</div>
                        </div>
                        <div class="domain-item domain-insurance">
                            <div class="domain-icon">🛡️</div>
                            <div class="domain-name">保险顾问</div>
                            <div class="domain-tags">条款·保单·贷款</div>
                        </div>
                    </div>
                    """)

                    with gr.Row():
                        with gr.Column(scale=3):
                            gr.HTML('<div class="chat-panel"><div class="chat-header"><div class="status-dot"></div><span class="chat-title">智能协调者 · 自动调度</span></div></div>')
                            unified_chatbot = gr.Chatbot(height=320, show_label=False)

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

                    gr.HTML("""
                    <div class="examples-section">
                        <button class="examples-toggle" onclick="toggleExamples('unified-examples')">
                            <span>📋 示例问题</span>
                            <span class="examples-toggle-icon" id="unified-examples-icon">▼</span>
                        </button>
                        <div class="examples-content" id="unified-examples">
                            <button class="example-chip">查询持仓情况</button>
                            <button class="example-chip">客户亏损能办保单贷款吗？</button>
                            <button class="example-chip">高净值客户有哪些</button>
                            <button class="example-chip">预测股价</button>
                        </div>
                    </div>
                    """)

                    gr.HTML('<div class="input-section"><div class="input-row">')
                    unified_input = gr.Textbox(placeholder="描述您的金融需求，协调者将自动调度...", lines=1, show_label=False, container=False)
                    gr.Button("发送", elem_classes=["btn-send"])
                    gr.Button("清空", elem_classes=["btn-clear"])
                    gr.HTML('</div></div>')

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

                    unified_chatbot.change(unified_chat, [unified_input, unified_chatbot], [unified_chatbot, unified_input])

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
