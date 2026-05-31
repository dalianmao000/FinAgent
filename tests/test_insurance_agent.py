"""Tests for Insurance Agent."""
import pytest
from unittest.mock import patch, MagicMock
from src.specialists.insurance.agent import InsuranceAgent
from src.specialists.base import SpecialistConfig
from src.coordinator.intent_classifier import Domain


def test_insurance_agent_initialization():
    """Test InsuranceAgent initialization."""
    config = SpecialistConfig(
        agent_name="insurance",
        domain=Domain.INSURANCE,
        session_id="test-session"
    )
    agent = InsuranceAgent(config)

    assert agent.agent_name == "insurance"
    assert agent.domain == Domain.INSURANCE
    assert len(agent.tools) == 3
    tool_names = [t.name for t in agent.tools]
    assert "rag_query" in tool_names
    assert "query_policy" in tool_names
    assert "calculate_loan" in tool_names


def test_insurance_agent_rag_query():
    """Test RAG query for insurance clauses."""
    config = SpecialistConfig(
        agent_name="insurance",
        domain=Domain.INSURANCE,
        session_id="test-session"
    )
    agent = InsuranceAgent(config)

    result = agent._rag_query()

    assert result["status"] == "success"
    assert "results" in result
    assert len(result["results"]) == 2
    assert result["results"][0]["title"] == "寿险保单贷款条款"
    assert "现金价值80%" in result["results"][0]["content"]


def test_insurance_agent_query_policy():
    """Test querying insurance policies."""
    config = SpecialistConfig(
        agent_name="insurance",
        domain=Domain.INSURANCE,
        session_id="test-session"
    )
    agent = InsuranceAgent(config)

    result = agent._query_policy()

    assert result["status"] == "success"
    assert "policies" in result
    assert len(result["policies"]) == 2
    assert result["policies"][0]["type"] == "寿险"
    assert result["policies"][0]["cash_value"] == 500000


def test_insurance_agent_calculate_loan():
    """Test calculating loan amount."""
    config = SpecialistConfig(
        agent_name="insurance",
        domain=Domain.INSURANCE,
        session_id="test-session"
    )
    agent = InsuranceAgent(config)

    result = agent._calculate_loan()

    assert result["status"] == "success"
    assert "total_loanable" in result
    assert "policies" in result
    # Only 寿险 has cash_value (500000), 80% = 400000
    assert result["total_loanable"] == 400000
    assert "40万" in result["summary"]


def test_insurance_agent_execute():
    """Test executing task through agent."""
    config = SpecialistConfig(
        agent_name="insurance",
        domain=Domain.INSURANCE,
        session_id="test-session"
    )
    agent = InsuranceAgent(config)

    class MockTask:
        description = "rag_query"

    result = agent.execute(MockTask())

    assert result["status"] == "success"
    assert "results" in result


def test_insurance_agent_rag_with_task():
    """Test RAG query with task description."""
    config = SpecialistConfig(
        agent_name="insurance",
        domain=Domain.INSURANCE,
        session_id="test-session"
    )
    agent = InsuranceAgent(config)

    class MockTask:
        description = "重大疾病保险条款"

    result = agent._rag_query(MockTask())

    assert result["status"] == "success"
    assert result["query"] == "重大疾病保险条款"