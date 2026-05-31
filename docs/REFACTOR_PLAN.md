# FinAgent Unified - qwen-agent核心重构计划

## 重构目标

将自定义框架替换为以 qwen-agent 为核心的架构，确保结果风格与qwen-agent一致。

## 新架构

```
┌─────────────────────────────────────────────────────────────┐
│                   Coordinator (qwen-agent)                   │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ ReActChat with function calling                      │ │
│  │ - Intent detection via LLM                          │ │
│  │ - Task decomposition via tool calling                │ │
│  │ - Result synthesis via LLM                          │ │
│  └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                    dispatch via tool calls
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│ Investment    │◄───►│ Customer      │◄───►│ Insurance     │
│ Specialist    │     │ Specialist    │     │ Specialist    │
│ (qwen-agent) │     │ (qwen-agent)  │     │ (qwen-agent)  │
│ Assistant     │     │ Assistant      │     │ Assistant     │
└───────────────┘     └───────────────┘     └───────────────┘
        │                     │                     │
        ▼                     ▼                     ▼
   MySQL/股票            MySQL/客户            ES/保险条款
```

## 文件改动清单

### 1. src/specialists/base.py - 改用qwen-agent Assistant
- 继承 qwen_agent.agents.Assistant
- 使用 @register_tool 装饰器注册工具
- 移除自定义 tool_execute 模式

### 2. src/specialists/investment/agent.py
- tools/ 目录下的函数使用 @register_tool 装饰
- 查询/计算逻辑保持，适配 qwen-agent tool 格式

### 3. src/specialists/customer/agent.py
- 同上

### 4. src/specialists/insurance/agent.py
- RAG 查询适配 qwen-agent memory

### 5. src/coordinator/agent.py
- 使用 qwen_agent.agents.ReActChat
- 意图识别通过 prompt 让 LLM 判断
- 任务分解通过 tool calling
- 结果整合通过 LLM 生成

### 6. 保留不变
- src/message_bus/* - Redis通信保持
- src/api/* - API保持不变
- src/tools/config.py - 配置保持
- tests/* - 测试适配新接口

## qwen-agent 关键API

```python
# Specialist基类
from qwen_agent import Assistant

class InvestmentAgent(Assistant):
    def __init__(self, ...):
        super().__init__(
            model="qwen-turbo",
            api_key=api_key,
            tools=[...],  # qwen-agent tools list
            system_message="你是一个投资分析专家..."
        )

# Coordinator使用ReActChat
from qwen_agent import ReActChat

coordinator = ReActChat(
    model="qwen-turbo",
    tools=[dispatch_tool],  # 分发任务的工具
    system_message="你是一个协调者..."
)
```

## 执行步骤

1. 读取现有qwen-agent框架代码结构
2. 重写 specialists/base.py
3. 重写各 Specialist Agent
4. 重写 Coordinator Agent
5. 适配测试
6. 端到端验证
