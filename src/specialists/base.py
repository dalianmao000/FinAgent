"""Base class for specialist agents."""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from ..message_bus.shared_context import SharedContext
from ..coordinator.intent_classifier import Domain


class Tool(BaseModel):
    """Tool definition for a specialist agent."""
    name: str
    description: str
    parameters: Dict[str, Any] = Field(default_factory=dict)


class SpecialistConfig(BaseModel):
    """Configuration for specialist agent."""
    agent_name: str
    domain: Domain
    session_id: str


class SpecialistAgent(ABC):
    """Abstract base class for specialist agents."""

    def __init__(self, config: SpecialistConfig):
        self.agent_name = config.agent_name
        self.domain = config.domain
        self.session_id = config.session_id
        self.tools: List[Tool] = []
        self.shared_context = SharedContext(self.session_id)
        self._initialize_tools()

    @abstractmethod
    def _initialize_tools(self):
        """Initialize the tools available to this agent."""
        pass

    @abstractmethod
    def _execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific tool."""
        pass

    def execute(self, task) -> Dict[str, Any]:
        """Execute a task using appropriate tool."""
        tool_name = self._select_tool(task)
        if tool_name:
            return self._execute_tool(tool_name, {"task": task})
        return {"status": "no_tool", "message": f"No tool available for task: {getattr(task, 'description', 'unknown')}"}

    def _select_tool(self, task) -> Optional[str]:
        """Select appropriate tool for a task."""
        for tool in self.tools:
            if tool.name in getattr(task, 'description', ''):
                return tool.name
        return self.tools[0].name if self.tools else None

    def register_tool(self, tool: Tool):
        """Register a new tool."""
        self.tools.append(tool)

    def get_tools(self) -> List[Dict[str, Any]]:
        """Get all available tools as dict."""
        return [{"name": t.name, "description": t.description} for t in self.tools]