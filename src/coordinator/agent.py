"""Coordinator Agent using qwen-agent MultiAgentHub."""
from typing import Dict, List, Any
from qwen_agent.agents import MultiAgentHub
from qwen_agent.llm.schema import Message


class CoordinatorAgent:
    """Coordinator agent using qwen-agent MultiAgentHub."""

    SYSTEM_PROMPT = """你是一个金融智能顾问平台的协调者。用户的请求可能涉及:
- 投资分析 (持仓、盈亏、行情)
- 客户经营 (画像、分群、流失)
- 保险顾问 (条款、保单、贷款)

你需要根据用户问题，协调相应的专家Agent来回答。"""

    def __init__(self, session_id: str, specialists: List = None, **kwargs):
        self.session_id = session_id
        self.specialists = specialists or []

        # Create a MultiAgentHub subclass with the specialists
        class FinAgentHub(MultiAgentHub):
            def __init__(self, agents):
                self._agents = agents
                super().__init__()

        self.agent = FinAgentHub(specialists)

    def process(self, user_message: str) -> str:
        """Process user message through the multi-agent system."""
        messages = [Message(role='user', content=user_message)]
        response = []
        for chunk in self.agent.run(messages):
            if chunk:
                response.extend(chunk)

        if response:
            last_msg = response[-1]
            if hasattr(last_msg, 'content'):
                return last_msg.content
        return "处理完成"

    def get_status(self) -> Dict[str, Any]:
        """Get current status."""
        return {
            "session_id": self.session_id,
            "specialist_count": len(self.specialists),
            "specialists": [s.name for s in self.specialists]
        }