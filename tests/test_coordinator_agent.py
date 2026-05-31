"""Tests for Coordinator Agent."""
import pytest
from unittest.mock import MagicMock, patch
from src.coordinator.agent import CoordinatorAgent, AgentConfig
from src.coordinator.intent_classifier import Domain


def test_agent_config():
    """Test Coordinator configuration."""
    config = AgentConfig(
        agent_name="coordinator",
        session_id="test-session-001"
    )
    assert config.agent_name == "coordinator"
    assert config.session_id == "test-session-001"


def test_coordinator_initialization():
    """Test Coordinator initialization."""
    with patch('redis.Redis'):
        agent = CoordinatorAgent(session_id="test-session-001")
        assert agent.agent_name == "coordinator"
        assert agent.session_id == "test-session-001"
        assert agent.intent_classifier is not None
        assert agent.task_decomposer is not None
        assert agent.result_integrator is not None


def test_coordinator_register_specialist():
    """Test registering specialist agents."""
    with patch('redis.Redis'):
        agent = CoordinatorAgent(session_id="test-session-001")

        mock_specialist = MagicMock()
        agent.register_specialist("investment", mock_specialist)

        assert "investment" in agent.specialist_agents
        assert agent.specialist_agents["investment"] == mock_specialist


def test_coordinator_process_single_domain():
    """Test processing single domain query."""
    with patch('redis.Redis') as mock_redis:
        mock_redis_instance = MagicMock()
        mock_redis.return_value = mock_redis_instance

        agent = CoordinatorAgent(session_id="test-session-001")

        # Mock the specialist
        mock_specialist = MagicMock()
        mock_specialist.execute.return_value = {
            "status": "success",
            "positions": [{"stock": "茅台", "shares": 500}],
            "summary": "持仓茅台500股"
        }
        agent.register_specialist("investment", mock_specialist)

        response = agent.process("查询持仓情况")

        assert len(response) > 0
        assert mock_specialist.execute.called


def test_coordinator_process_cross_domain():
    """Test processing cross-domain query."""
    with patch('redis.Redis') as mock_redis:
        mock_redis_instance = MagicMock()
        mock_redis.return_value = mock_redis_instance

        agent = CoordinatorAgent(session_id="test-session-001")

        # Mock specialists
        mock_inv = MagicMock()
        mock_inv.execute.return_value = {
            "positions": [{"stock": "茅台", "pnl": -0.2}],
            "summary": "亏损20%"
        }

        mock_ins = MagicMock()
        mock_ins.execute.return_value = {
            "total_loanable": 400000,
            "summary": "可贷40万"
        }

        agent.register_specialist("investment", mock_inv)
        agent.register_specialist("insurance", mock_ins)

        response = agent.process("持仓茅台亏了，能办保单贷款吗")

        assert len(response) > 0
        assert mock_inv.execute.called
        assert mock_ins.execute.called


def test_coordinator_get_status():
    """Test getting agent status."""
    with patch('redis.Redis') as mock_redis:
        mock_redis_instance = MagicMock()
        mock_redis.return_value = mock_redis_instance
        # Mock redis.get to return None for customer context
        mock_redis_instance.get.return_value = None
        mock_redis_instance.lrange.return_value = []

        agent = CoordinatorAgent(session_id="test-session-001")
        status = agent.get_status()

        assert "session_id" in status
        assert status["session_id"] == "test-session-001"
        assert "pending_tasks" in status
        assert "completed_tasks" in status
        assert "registered_agents" in status


def test_coordinator_no_specialist():
    """Test handling when no specialist is registered."""
    with patch('redis.Redis') as mock_redis:
        mock_redis_instance = MagicMock()
        mock_redis.return_value = mock_redis_instance

        agent = CoordinatorAgent(session_id="test-session-001")

        response = agent.process("查询持仓情况")

        # Should handle gracefully without crashing
        assert response is not None