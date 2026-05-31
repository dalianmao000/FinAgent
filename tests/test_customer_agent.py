"""Tests for Customer Agent."""
import pytest
from unittest.mock import patch, MagicMock
from src.specialists.customer.agent import CustomerAgent
from src.specialists.base import SpecialistConfig
from src.coordinator.intent_classifier import Domain


def test_customer_agent_initialization():
    """Test CustomerAgent initialization."""
    config = SpecialistConfig(
        agent_name="customer",
        domain=Domain.CUSTOMER,
        session_id="test-session"
    )
    agent = CustomerAgent(config)

    assert agent.agent_name == "customer"
    assert agent.domain == Domain.CUSTOMER
    assert len(agent.tools) == 4
    tool_names = [t.name for t in agent.tools]
    assert "query_customer_profile" in tool_names
    assert "customer_clustering" in tool_names
    assert "churn_prediction" in tool_names
    assert "lightgbm_predict" in tool_names


def test_customer_agent_query_profile_no_customer():
    """Test querying profile when no customer is set."""
    config = SpecialistConfig(
        agent_name="customer",
        domain=Domain.CUSTOMER,
        session_id="test-session"
    )
    agent = CustomerAgent(config)

    with patch.object(agent.shared_context, 'get_customer', return_value=None):
        result = agent._query_customer_profile()

    assert result["status"] == "success"
    assert "profile" in result
    assert result["profile"]["name"] == "王总"
    assert result["profile"]["total_assets"] == 5000000


def test_customer_agent_clustering_placeholder():
    """Test clustering returns placeholder."""
    config = SpecialistConfig(
        agent_name="customer",
        domain=Domain.CUSTOMER,
        session_id="test-session"
    )
    agent = CustomerAgent(config)

    result = agent._customer_clustering()

    assert result["status"] == "placeholder"
    assert "KMeans" in result["message"]


def test_customer_agent_churn_prediction_placeholder():
    """Test churn prediction returns placeholder."""
    config = SpecialistConfig(
        agent_name="customer",
        domain=Domain.CUSTOMER,
        session_id="test-session"
    )
    agent = CustomerAgent(config)

    result = agent._churn_prediction()

    assert result["status"] == "placeholder"
    assert "历史流失数据" in result["message"]


def test_customer_agent_lightgbm_placeholder():
    """Test LightGBM prediction returns placeholder."""
    config = SpecialistConfig(
        agent_name="customer",
        domain=Domain.CUSTOMER,
        session_id="test-session"
    )
    agent = CustomerAgent(config)

    result = agent._lightgbm_predict()

    assert result["status"] == "placeholder"
    assert "训练好的模型" in result["message"]


def test_customer_agent_execute():
    """Test executing task through agent."""
    config = SpecialistConfig(
        agent_name="customer",
        domain=Domain.CUSTOMER,
        session_id="test-session"
    )
    agent = CustomerAgent(config)

    class MockTask:
        description = "查询客户画像"

    with patch.object(agent.shared_context, 'get_customer', return_value=None):
        result = agent.execute(MockTask())

    assert result["status"] == "success"
    assert "profile" in result