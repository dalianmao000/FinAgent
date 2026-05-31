# FinAgent Unified - 金融智能顾问统一平台

[![qwen-agent](https://img.shields.io/badge/qwen--agent-v1.0-blue)](https://github.com/QwenLM/qwen-agent)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-green)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-orange)](https://flask.palletsprojects.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green)](https://fastapi.tiangolo.com/)
[![Gradio](https://img.shields.io/badge/Gradio-4.0-yellow)](https://gradio.app/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-blue)](https://www.mysql.com/)
[![Elasticsearch](https://img.shields.io/badge/Elasticsearch-8.0-RED)](https://www.elastic.co/)
[![Redis](https://img.shields.io/badge/Redis-7.0-red)](https://redis.io/)
[![RAG](https://img.shields.io/badge/RAG-Retrieval--Augmented--Generation-blue)](https://python.langchain.com/docs/get_started/introduction)
[![BM25](https://img.shields.io/badge/BM25-Keyword--Search-green)](https://www.elastic.co/guide/en/elasticsearch/reference/current/pluggable-similarity.html)
[![Text--Embedding](https://img.shields.io/badge/Text--Embedding-Vector--Search-orange)](https://python.langchain.com/docs/modules/data_connection/text_embedding)
[![scikit--learn](https://img.shields.io/badge/ML-scikit--learn_1.4-orange)](https://scikit-learn.org/)
[![Docker](https://img.shields.io/badge/Docker-24.0-blue)](https://www.docker.com/)
[![Claude--Code](https://img.shields.io/badge/Claude--Code-AI--Programming-yellow)](https://claude.com/claude-code)

基于 qwen-agent 框架的多智能体金融顾问系统，支持投资分析、客户经营、保险顾问三大领域。

## 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                   Coordinator (MultiAgentHub)                │
│              协调者 - 根据问题调度专家 Agent                  │
└─────────────────────────────────────────────────────────────┘
                              │
                    dispatch via tool calls
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│   Investment   │     │   Customer   │     │   Insurance   │
│   Specialist   │     │   Specialist  │     │   Specialist  │
│  (qwen-agent) │     │  (qwen-agent)│     │  (qwen-agent)│
└───────────────┘     └───────────────┘     └───────────────┘
        │                     │                     │
        ▼                     ▼                     ▼
   MySQL/股票            MySQL/客户            ES/保险条款
```

## 目录结构

```
finagent_unified/
├── .env                    # 环境配置（密码、API Key）
├── .env.example             # 环境配置模板
├── src/
│   ├── api/
│   │   ├── main.py         # Flask API
│   │   ├── fastapi_app.py  # FastAPI API (可选)
│   │   └── gradio_ui.py    # Gradio WebUI
│   ├── coordinator/
│   │   └── agent.py       # 协调者 Agent
│   ├── gui/
│   │   └── webui.py       # WebUI 启动器
│   ├── specialists/
│   │   ├── base.py         # Specialist 基类
│   │   ├── investment/     # 投资专家
│   │   │   ├── agent.py
│   │   │   └── tools/     # 投资工具
│   │   │       ├── query_positions.py
│   │   │       ├── calculate_pnl.py
│   │   │       ├── arima_prediction.py
│   │   │       ├── boll_detection.py
│   │   │       └── prophet_analysis.py
│   │   ├── customer/      # 客户经营专家
│   │   │   ├── agent.py
│   │   │   └── tools/     # 客户工具
│   │   │       ├── execute_sql.py
│   │   │       ├── high_value_insight.py
│   │   │       ├── decision_tree_prediction.py
│   │   │       ├── customer_clustering.py
│   │   │       ├── product_association.py
│   │   │       ├── arima_asset_forecast.py
│   │   │       └── lightgbm_prediction.py
│   │   └── insurance/      # 保险专家
│   │       ├── agent.py
│   │       └── tools/     # 保险工具
│   │           ├── es_text_retrieval.py
│   │           ├── es_vector_retrieval.py
│   │           ├── es_hybrid_retrieval.py
│   │           └── text_embedding.py  # 文本向量生成
│   └── tools/
│       ├── config.py       # 配置管理
│       └── llm.py          # LLM 封装
├── tests/
│   └── test_qwen_agent_integration.py
└── docs/
    └── REFACTOR_PLAN.md
```

## 快速开始

### 1. 配置环境

```bash
# 复制配置模板
cp .env.example .env

# 编辑 .env 填入实际值
vim .env
```

### 2. 启动服务

```bash
# Flask API
python -m src.api.main

# FastAPI (可选)
python -m src.api.fastapi_app
# 或 uvicorn src.api.fastapi_app:app --host 0.0.0.0 --port 8000

# Gradio WebUI
python -m src.gui.webui --unified

# 单独测试 Investment Agent
python -m src.specialists.investment.agent
```

### 3. 访问

- Flask API: http://localhost:5000
- FastAPI: http://localhost:8000
- FastAPI Docs: http://localhost:8000/docs
- Gradio WebUI: http://localhost:7860

## 配置说明

所有配置通过 `.env` 文件管理：

```bash
# ==================
# 模型配置
# ==================
MODEL_NAME=qwen-turbo
MODEL_TYPE=qwen_dashscope
MODEL_TEMPERATURE=0.7
MODEL_MAX_TOKENS=2000

# ==================
# API Keys
# ==================
DASHSCOPE_API_KEY=your_api_key

# ==================
# MySQL 数据库
# ==================
# 投资工具用
STOCK_DB_HOST=localhost
STOCK_DB_PORT=3306
STOCK_DB_USER=root
STOCK_DB_PASSWORD=
STOCK_DB_NAME=stock

# 客户工具用
CUSTOMER_DB_HOST=localhost
CUSTOMER_DB_PORT=3306
CUSTOMER_DB_USER=root
CUSTOMER_DB_PASSWORD=
CUSTOMER_DB_NAME=enterprise_credit_clients

# ==================
# Elasticsearch
# ==================
ES_HOST=localhost
ES_PORT=9200
ES_USERNAME=elastic
ES_PASSWORD=
ES_INDEX_NAME=qwen_agent_docs_vector
```

## Agent 工具清单

### Investment Specialist（投资专家）

| 工具 | 说明 |
|------|------|
| QueryPositionsTool | 查询客户持仓 |
| CalculatePnLTool | 计算盈亏 |
| ArimaPredictionTool | ARIMA 股价预测 |
| BollDetectionTool | 布林带异常检测 |
| ProphetAnalysisTool | Prophet 周期性分析 |

### Customer Specialist（客户专家）

| 工具 | 说明 |
|------|------|
| ExecuteSQLTool | SQL 查询 + 可视化 |
| HighValueUserInsightTool | 逻辑回归高价值用户画像 |
| DecisionTreeAssetPredictionTool | 决策树资产预测 |
| KMeansClusteringTool | KMeans 客户聚类 |
| ProductAssociationRulesTool | Apriori 产品关联分析 |
| ARIMAAssetForecastTool | ARIMA 资产预测 |
| LightGBMAssetPredictionTool | LightGBM + SHAP 预测 |

### Insurance Specialist（保险专家）

| 工具 | 说明 |
|------|------|
| ESTextRetrievalTool | ES 文本检索 (BM25) |
| ESVectorRetrievalTool | ES 向量检索 (RAG) |
| ESHybridRetrievalTool | ES 混合检索 |
| TextEmbeddingTool | DashScope 文本向量生成 |

## API 接口

```
POST /api/v1/chat
     - body: {"message": "问题", "session_id": "可选"}

GET  /api/v1/session/{session_id}/status
POST /api/v1/session/{session_id}/customer
     - body: {"customer_id", "name", "total_assets", "risk_level"}

GET  /api/v1/sessions
GET  /api/v1/health
```

## 开发指南

### 添加新工具

1. 在对应 `tools/` 目录创建新文件：

```python
# src/specialists/investment/tools/my_tool.py
from qwen_agent.tools.base import BaseTool, register_tool

@register_tool('my_tool_name')
class MyTool(BaseTool):
    name = 'my_tool_name'
    description = '工具描述'
    parameters = []

    def call(self, params: str, **kwargs) -> str:
        return "结果"
```

2. 在 `tools/__init__.py` 导出：

```python
from .my_tool import MyTool
__all__ = [..., 'MyTool']
```

3. 在 `agent.py` 注册：

```python
from .tools import MyTool

function_list=[
    ...
    MyTool(),
]
```

### 添加新的 Specialist

1. 创建 `src/specialists/new_domain/agent.py`
2. 创建 `src/specialists/new_domain/tools/`
3. 在 `src/api/main.py` 注册到 Coordinator

## 技术栈

- **框架**: qwen-agent (qwen-agent)
- **API**: Flask + FastAPI + Gradio
- **数据库**: MySQL, Elasticsearch
- **检索**: RAG, BM25, Text-Embedding
- **机器学习**: scikit-learn, LightGBM, Prophet, ARIMA, SHAP
- **部署**: Docker Compose

## License

MIT
