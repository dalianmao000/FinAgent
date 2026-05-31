"""Coordinator Agent implementation."""
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

from ..message_bus.message_format import AgentMessage, MessageType, EventType
from ..message_bus.shared_context import SharedContext
from .intent_classifier import IntentClassifier, IntentType, Domain
from .task_decomposer import TaskDecomposer, Task
from .result_integrator import ResultIntegrator


class AgentConfig(BaseModel):
    """Configuration for an agent."""
    agent_name: str
    session_id: str
    redis_url: Optional[str] = None


class CoordinatorAgent:
    """Coordinator agent that manages conversation flow and agent dispatch."""

    SYSTEM_PROMPT = """
你是一个金融智能顾问平台的协调者。你的职责是:
1. 理解用户的金融问题
2. 判断问题涉及哪些领域(投资/客户/保险)
3. 分解任务并调度合适的专家Agent
4. 整合各Agent返回的结果，给出统一回答

用户的问题可能涉及:
- 投资分析: 持仓查询、盈亏分析、股价预测、技术指标
- 客户经营: 客户画像、分群分析、流失预警、资产预测
- 保险顾问: 条款查询、保单信息、贷款计算、理赔规则

当问题涉及多个领域时，需要协调多个Agent协作完成。
"""

    def __init__(self, session_id: str, config: Optional[AgentConfig] = None):
        self.agent_name = "coordinator"
        self.session_id = session_id
        self.config = config or AgentConfig(
            agent_name="coordinator",
            session_id=session_id
        )

        # Initialize components
        self.intent_classifier = IntentClassifier()
        self.task_decomposer = TaskDecomposer()
        self.result_integrator = ResultIntegrator()

        # Shared context
        self.shared_context = SharedContext(session_id)

        # Task tracking
        self.pending_tasks: Dict[str, Task] = {}
        self.completed_tasks: Dict[str, Dict[str, Any]] = {}

        # Agent registry
        self.specialist_agents: Dict[str, Any] = {}

    def register_specialist(self, agent_name: str, agent_instance: Any):
        """Register a specialist agent."""
        self.specialist_agents[agent_name] = agent_instance

    def process(self, user_message: str) -> str:
        """Process user message and return response."""
        # Step 1: Intent classification
        classification = self.intent_classifier.classify(user_message)

        # Step 2: Task decomposition
        tasks = self.task_decomposer.decompose(user_message, classification)

        # Step 3: Store tasks in context
        for task in tasks:
            self.pending_tasks[task.task_id] = task
            self.shared_context.set_task(task.task_id, task.domain.value, "pending")

        # Step 4: Dispatch tasks to specialists (in parallel)
        results = self._dispatch_tasks(tasks)

        # Step 5: Integrate results
        response = self.result_integrator.integrate(user_message, tasks, results)

        # Step 6: Add to history
        self.shared_context.add_history(
            role="user",
            content=user_message,
            agents=[t.domain.value for t in tasks]
        )
        self.shared_context.add_history(
            role="assistant",
            content=response,
            agents=list(results.keys())
        )

        return response

    def _dispatch_tasks(self, tasks: List[Task]) -> Dict[str, Dict[str, Any]]:
        """Dispatch tasks to specialist agents."""
        results = {}

        # For simplicity, execute sequentially
        # In production, this would use async/celery for parallel execution
        for task in tasks:
            agent_name = task.domain.value

            if agent_name in self.specialist_agents:
                agent = self.specialist_agents[agent_name]
                result = agent.execute(task)
                results[agent_name] = result

                # Update context
                self.completed_tasks[task.task_id] = result
                self.shared_context.set_task(task.task_id, agent_name, "completed")
                self.shared_context.set_agent_data(agent_name, result)
            else:
                # No agent registered, return mock result
                results[agent_name] = {"status": "no_agent", "message": f"No agent registered for {agent_name}"}

        return results

    def get_status(self) -> Dict[str, Any]:
        """Get current agent status."""
        return {
            "session_id": self.session_id,
            "pending_tasks": len(self.pending_tasks),
            "completed_tasks": len(self.completed_tasks),
            "registered_agents": list(self.specialist_agents.keys()),
            "customer": self.shared_context.get_customer(),
            "history_length": len(self.shared_context.get_history())
        }