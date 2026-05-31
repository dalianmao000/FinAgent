"""Tests for Investment Agent."""
import pytest
from unittest.mock import patch, MagicMock
from src.specialists.investment.agent import InvestmentAgent
from src.specialists.base import SpecialistConfig
from src.coordinator.intent_classifier import Domain


def test_investment_agent_initialization():
    """Test InvestmentAgent initialization."""
    config = SpecialistConfig(
        agent_name="investment",
        domain=Domain.INVESTMENT,
        session_id="test-session"
    )
    agent = InvestmentAgent(config)

    assert agent.agent_name == "investment"
    assert agent.domain == Domain.INVESTMENT
    assert len(agent.tools) == 4
    tool_names = [t.name for t in agent.tools]
    assert "query_positions" in tool_names
    assert "calculate_pnl" in tool_names
    assert "arima_forecast" in tool_names
    assert "bollinger_detection" in tool_names


def test_investment_agent_query_positions():
    """Test querying positions."""
    config = SpecialistConfig(
        agent_name="investment",
        domain=Domain.INVESTMENT,
        session_id="test-session"
    )
    agent = InvestmentAgent(config)

    result = agent._query_positions()

    assert result["status"] == "success"
    assert "positions" in result
    assert len(result["positions"]) == 2
    assert result["positions"][0]["stock"] == "贵州茅台"


def test_investment_agent_calculate_pnl():
    """Test calculating profit and loss."""
    config = SpecialistConfig(
        agent_name="investment",
        domain=Domain.INVESTMENT,
        session_id="test-session"
    )
    agent = InvestmentAgent(config)

    result = agent._calculate_pnl()

    assert result["status"] == "success"
    assert "positions" in result
    assert "total_pnl" in result
    assert "total_pnl_pct" in result
    assert "summary" in result
    # Total cost = 500*1800 + 200*450 = 900000 + 90000 = 990000
    # Total value = 500*1440 + 200*380 = 720000 + 76000 = 796000
    # PnL = 796000 - 990000 = -194000
    assert result["total_pnl"] == -194000


def test_investment_agent_execute():
    """Test executing task through agent."""
    config = SpecialistConfig(
        agent_name="investment",
        domain=Domain.INVESTMENT,
        session_id="test-session"
    )
    agent = InvestmentAgent(config)

    class MockTask:
        description = "查询持仓"

    result = agent.execute(MockTask())

    assert result["status"] == "success"
    assert "positions" in result


def test_investment_agent_arima_placeholder():
    """Test ARIMA forecast placeholder."""
    config = SpecialistConfig(
        agent_name="investment",
        domain=Domain.INVESTMENT,
        session_id="test-session"
    )
    agent = InvestmentAgent(config)

    result = agent._arima_forecast()

    assert result["status"] == "placeholder"
    assert "开发中" in result["message"]


def test_investment_agent_bollinger_placeholder():
    """Test Bollinger detection placeholder."""
    config = SpecialistConfig(
        agent_name="investment",
        domain=Domain.INVESTMENT,
        session_id="test-session"
    )
    agent = InvestmentAgent(config)

    result = agent._bollinger_detection()

    assert result["status"] == "placeholder"