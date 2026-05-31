"""Tests for qwen-agent integration - new tests for the refactored qwen-agent based agents."""
import os
import pytest


# Check for DashScope API key - skip tests if not available
SKIP_REASON = "DashScope API key not available"
needs_api_key = pytest.mark.skipif(
    not os.environ.get("DASHSCOPE_API_KEY"),
    reason=SKIP_REASON
)


@needs_api_key
def test_specialist_base_import():
    """Test that SpecialistAgent can be imported and instantiated."""
    from src.specialists.base import SpecialistAgent

    agent = SpecialistAgent(session_id="test_session")
    assert agent.session_id == "test_session"
    assert agent.NAME == "specialist"
    assert agent.DESCRIPTION == "A financial specialist agent"


@needs_api_key
def test_investment_agent_import():
    """Test that InvestmentAgent can be imported and instantiated."""
    from src.specialists.investment.agent import InvestmentAgent

    agent = InvestmentAgent(session_id="test_session")
    assert agent.session_id == "test_session"
    assert agent.NAME == "investment"
    assert agent.DESCRIPTION == "投资分析专家，可以查询持仓和计算盈亏"


@needs_api_key
def test_customer_agent_import():
    """Test that CustomerAgent can be imported and instantiated."""
    from src.specialists.customer.agent import CustomerAgent

    agent = CustomerAgent(session_id="test_session")
    assert agent.session_id == "test_session"
    assert agent.NAME == "customer"
    assert agent.DESCRIPTION == "客户经营专家，可以查询客户画像和进行分群分析"


@needs_api_key
def test_insurance_agent_import():
    """Test that InsuranceAgent can be imported and instantiated."""
    from src.specialists.insurance.agent import InsuranceAgent

    agent = InsuranceAgent(session_id="test_session")
    assert agent.session_id == "test_session"
    assert agent.NAME == "insurance"
    assert agent.DESCRIPTION == "保险顾问专家，可以查询保险条款和保单信息"


@needs_api_key
def test_coordinator_agent_import():
    """Test that CoordinatorAgent can be imported and instantiated."""
    from src.coordinator.agent import CoordinatorAgent

    agent = CoordinatorAgent(session_id="test_session", specialists=[])
    assert agent.session_id == "test_session"
    assert agent.specialists == []
    assert agent.get_status()["specialist_count"] == 0


@needs_api_key
def test_investment_agent_with_specialists():
    """Test InvestmentAgent with multiple specialists in Coordinator."""
    from src.specialists.investment.agent import InvestmentAgent
    from src.coordinator.agent import CoordinatorAgent

    investment_agent = InvestmentAgent(session_id="test_session")
    coordinator = CoordinatorAgent(
        session_id="test_session",
        specialists=[investment_agent]
    )

    status = coordinator.get_status()
    assert status["specialist_count"] == 1
    assert status["specialists"] == ["investment"]


@needs_api_key
def test_coordinator_with_multiple_specialists():
    """Test CoordinatorAgent with multiple specialist agents."""
    from src.specialists.investment.agent import InvestmentAgent
    from src.specialists.customer.agent import CustomerAgent
    from src.specialists.insurance.agent import InsuranceAgent
    from src.coordinator.agent import CoordinatorAgent

    investment = InvestmentAgent(session_id="test_session")
    customer = CustomerAgent(session_id="test_session")
    insurance = InsuranceAgent(session_id="test_session")

    coordinator = CoordinatorAgent(
        session_id="test_session",
        specialists=[investment, customer, insurance]
    )

    status = coordinator.get_status()
    assert status["specialist_count"] == 3
    assert status["specialists"] == ["investment", "customer", "insurance"]


@needs_api_key
def test_tool_functions_exist():
    """Test that tool functions are properly registered on agents."""
    from src.specialists.investment.agent import InvestmentAgent, QueryPositionsTool, CalculatePnLTool

    agent = InvestmentAgent(session_id="test_session")
    # Check that function_map contains the registered tools
    function_names = list(agent.function_map.keys())
    assert "investment_query_positions" in function_names or "QueryPositionsTool" in function_names
    assert "investment_calculate_pnl" in function_names or "CalculatePnLTool" in function_names


@needs_api_key
def test_insurance_tools_exist():
    """Test that insurance tools are properly registered."""
    from src.specialists.insurance.agent import InsuranceAgent

    agent = InsuranceAgent(session_id="test_session")
    function_names = list(agent.function_map.keys())
    # At least some tools should be registered
    assert len(function_names) >= 3


def test_qwen_agent_sdk_available():
    """Test that qwen-agent SDK is available."""
    try:
        from qwen_agent.agents import Assistant, MultiAgentHub
        from qwen_agent.tools.base import BaseTool, register_tool
        from qwen_agent.llm.schema import Message
        assert True
    except ImportError as e:
        pytest.fail(f"qwen-agent SDK not available: {e}")


def test_import_without_api_key():
    """Test that agents can be imported even without API key (constructor may fail later)."""
    # These should import fine - it's only at runtime that API key is needed
    from src.specialists.base import SpecialistAgent
    from src.specialists.investment.agent import InvestmentAgent
    from src.specialists.customer.agent import CustomerAgent
    from src.specialists.insurance.agent import InsuranceAgent
    from src.coordinator.agent import CoordinatorAgent

    # All should be classes that can be instantiated without API call
    assert SpecialistAgent is not None
    assert InvestmentAgent is not None
    assert CustomerAgent is not None
    assert InsuranceAgent is not None
    assert CoordinatorAgent is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])