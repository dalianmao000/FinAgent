"""Tests for specialist base class."""
from typing import Dict
import pytest
from src.specialists.base import SpecialistAgent, SpecialistConfig, Tool
from src.coordinator.intent_classifier import Domain


def test_tool_model():
    """Test Tool model."""
    tool = Tool(
        name="query_positions",
        description="查询客户持仓情况"
    )
    assert tool.name == "query_positions"
    assert tool.description == "查询客户持仓情况"


def test_specialist_config():
    """Test SpecialistConfig."""
    config = SpecialistConfig(
        agent_name="investment",
        domain=Domain.INVESTMENT,
        session_id="test-session"
    )
    assert config.agent_name == "investment"
    assert config.domain == Domain.INVESTMENT
    assert config.session_id == "test-session"


def test_specialist_initialization():
    """Test SpecialistAgent initialization with a concrete subclass."""
    # Create a concrete implementation for testing
    class TestAgent(SpecialistAgent):
        def _initialize_tools(self):
            self.register_tool(Tool(name="test_tool", description="A test tool"))

        def _execute_tool(self, tool_name: str, parameters: Dict) -> Dict:
            return {"status": "success", "tool": tool_name}

    config = SpecialistConfig(
        agent_name="test",
        domain=Domain.INVESTMENT,
        session_id="test-session"
    )
    agent = TestAgent(config)
    assert agent.agent_name == "test"
    assert agent.domain == Domain.INVESTMENT
    assert len(agent.tools) == 1
    assert agent.tools[0].name == "test_tool"


def test_specialist_register_tool():
    """Test registering tools."""
    class TestAgent(SpecialistAgent):
        def _initialize_tools(self):
            pass

        def _execute_tool(self, tool_name: str, parameters: Dict) -> Dict:
            return {}

    config = SpecialistConfig(
        agent_name="test",
        domain=Domain.CUSTOMER,
        session_id="test-session"
    )
    agent = TestAgent(config)

    agent.register_tool(Tool(name="tool1", description="First tool"))
    agent.register_tool(Tool(name="tool2", description="Second tool"))

    assert len(agent.tools) == 2
    tools = agent.get_tools()
    assert len(tools) == 2
    assert tools[0]["name"] == "tool1"


def test_specialist_execute():
    """Test executing a task."""
    class TestAgent(SpecialistAgent):
        def _initialize_tools(self):
            self.register_tool(Tool(name="query", description="Query tool"))

        def _execute_tool(self, tool_name: str, parameters: Dict) -> Dict:
            return {"status": "success", "executed": tool_name}

    config = SpecialistConfig(
        agent_name="test",
        domain=Domain.INVESTMENT,
        session_id="test-session"
    )
    agent = TestAgent(config)

    class MockTask:
        description = "query something"

    result = agent.execute(MockTask())
    assert result["status"] == "success"
    assert result["executed"] == "query"


def test_specialist_get_tools():
    """Test getting tools list."""
    class TestAgent(SpecialistAgent):
        def _initialize_tools(self):
            self.register_tool(Tool(name="tool1", description="First"))
            self.register_tool(Tool(name="tool2", description="Second"))

        def _execute_tool(self, tool_name: str, parameters: Dict) -> Dict:
            return {}

    config = SpecialistConfig(
        agent_name="test",
        domain=Domain.INSURANCE,
        session_id="test-session"
    )
    agent = TestAgent(config)
    tools = agent.get_tools()

    assert len(tools) == 2
    assert tools[0]["name"] == "tool1"
    assert tools[1]["name"] == "tool2"