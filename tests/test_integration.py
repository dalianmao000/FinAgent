"""End-to-end integration tests for FinAgent Unified."""
import json
import pytest
from unittest.mock import patch, MagicMock


def create_mock_redis():
    """Create a properly configured mock Redis instance."""
    mock_redis = MagicMock()

    # Mock customer data
    customer_data = {
        "customer_id": "C001",
        "name": "张三",
        "risk_level": "R3",
        "total_assets": 1000000.0
    }

    # Configure get to return proper JSON strings
    def mock_get(key):
        if "customer" in key:
            return json.dumps(customer_data).encode()
        return None

    mock_redis.get = mock_get
    mock_redis.set = MagicMock()
    mock_redis.delete = MagicMock()
    mock_redis.expire = MagicMock()

    return mock_redis


def test_full_conversation_flow_single_domain():
    """Test full conversation with single domain query."""
    mock_redis = create_mock_redis()
    with patch('redis.Redis', return_value=mock_redis):
        from src.coordinator.agent import CoordinatorAgent, AgentConfig
        from src.specialists.investment.agent import InvestmentAgent
        from src.specialists.customer.agent import CustomerAgent
        from src.specialists.insurance.agent import InsuranceAgent
        from src.specialists.base import SpecialistConfig
        from src.coordinator.intent_classifier import Domain

        session_id = "test-integration-session"

        # Create coordinator
        config = AgentConfig(agent_name="coordinator", session_id=session_id)
        coordinator = CoordinatorAgent(session_id=session_id, config=config)

        # Register specialists
        inv_config = SpecialistConfig(
            agent_name="investment", domain=Domain.INVESTMENT, session_id=session_id
        )
        cust_config = SpecialistConfig(
            agent_name="customer", domain=Domain.CUSTOMER, session_id=session_id
        )
        ins_config = SpecialistConfig(
            agent_name="insurance", domain=Domain.INSURANCE, session_id=session_id
        )

        coordinator.register_specialist("investment", InvestmentAgent(inv_config))
        coordinator.register_specialist("customer", CustomerAgent(cust_config))
        coordinator.register_specialist("insurance", InsuranceAgent(ins_config))

        # Test single domain query
        response = coordinator.process("查询持仓情况")
        assert len(response) > 0
        assert "贵州茅台" in response or "股票" in response or "持仓" in response


def test_full_conversation_flow_cross_domain():
    """Test full conversation with cross-domain query."""
    mock_redis = create_mock_redis()
    with patch('redis.Redis', return_value=mock_redis):
        from src.coordinator.agent import CoordinatorAgent, AgentConfig
        from src.specialists.investment.agent import InvestmentAgent
        from src.specialists.customer.agent import CustomerAgent
        from src.specialists.insurance.agent import InsuranceAgent
        from src.specialists.base import SpecialistConfig
        from src.coordinator.intent_classifier import Domain

        session_id = "test-integration-session-2"

        # Create coordinator
        config = AgentConfig(agent_name="coordinator", session_id=session_id)
        coordinator = CoordinatorAgent(session_id=session_id, config=config)

        # Register specialists
        inv_config = SpecialistConfig(
            agent_name="investment", domain=Domain.INVESTMENT, session_id=session_id
        )
        cust_config = SpecialistConfig(
            agent_name="customer", domain=Domain.CUSTOMER, session_id=session_id
        )
        ins_config = SpecialistConfig(
            agent_name="insurance", domain=Domain.INSURANCE, session_id=session_id
        )

        coordinator.register_specialist("investment", InvestmentAgent(inv_config))
        coordinator.register_specialist("customer", CustomerAgent(cust_config))
        coordinator.register_specialist("insurance", InsuranceAgent(ins_config))

        # Test cross-domain query
        response = coordinator.process("客户持仓茅台亏了，能办保单贷款吗")
        assert len(response) > 0
        # Should mention both investment and insurance info
        assert "茅台" in response or "投资" in response or "股票" in response or "亏损" in response


def test_intent_classification_accuracy():
    """Test intent classification accuracy."""
    from src.coordinator.intent_classifier import IntentClassifier, Domain

    classifier = IntentClassifier()

    # Test investment queries
    result = classifier.classify("查询茅台的持仓和盈亏")
    assert result.primary_domain == Domain.INVESTMENT

    # Test customer queries
    result = classifier.classify("这个客户的风险等级和资产情况")
    assert result.primary_domain == Domain.CUSTOMER

    # Test insurance queries
    result = classifier.classify("保单贷款能贷多少")
    assert result.primary_domain == Domain.INSURANCE

    # Test cross-domain
    result = classifier.classify("客户持仓亏损，保单能贷款吗")
    assert len(result.involved_domains) >= 2


def test_all_specialist_agents_function():
    """Test all specialist agents can execute tasks."""
    mock_redis = create_mock_redis()
    with patch('redis.Redis', return_value=mock_redis):
        from src.specialists.investment.agent import InvestmentAgent
        from src.specialists.customer.agent import CustomerAgent
        from src.specialists.insurance.agent import InsuranceAgent
        from src.specialists.base import SpecialistConfig
        from src.coordinator.intent_classifier import Domain

        session_id = "test-all-agents"

        # Test Investment Agent
        inv_config = SpecialistConfig(
            agent_name="investment", domain=Domain.INVESTMENT, session_id=session_id
        )
        inv_agent = InvestmentAgent(inv_config)
        inv_result = inv_agent._query_positions()
        assert inv_result["status"] == "success"
        assert len(inv_result["positions"]) == 2

        # Test Customer Agent
        cust_config = SpecialistConfig(
            agent_name="customer", domain=Domain.CUSTOMER, session_id=session_id
        )
        cust_agent = CustomerAgent(cust_config)
        cust_result = cust_agent._query_customer_profile()
        assert cust_result["status"] == "success"
        assert "profile" in cust_result

        # Test Insurance Agent
        ins_config = SpecialistConfig(
            agent_name="insurance", domain=Domain.INSURANCE, session_id=session_id
        )
        ins_agent = InsuranceAgent(ins_config)
        ins_result = ins_agent._query_policy()
        assert ins_result["status"] == "success"
        assert len(ins_result["policies"]) == 2


def test_coordinator_with_all_agents_registered():
    """Test coordinator with all agents registered."""
    mock_redis = create_mock_redis()
    with patch('redis.Redis', return_value=mock_redis):
        from src.coordinator.agent import CoordinatorAgent, AgentConfig
        from src.specialists.investment.agent import InvestmentAgent
        from src.specialists.customer.agent import CustomerAgent
        from src.specialists.insurance.agent import InsuranceAgent
        from src.specialists.base import SpecialistConfig
        from src.coordinator.intent_classifier import Domain

        session_id = "test-full-coordinator"

        config = AgentConfig(agent_name="coordinator", session_id=session_id)
        coordinator = CoordinatorAgent(session_id=session_id, config=config)

        # Register all specialists
        inv_config = SpecialistConfig(
            agent_name="investment", domain=Domain.INVESTMENT, session_id=session_id
        )
        cust_config = SpecialistConfig(
            agent_name="customer", domain=Domain.CUSTOMER, session_id=session_id
        )
        ins_config = SpecialistConfig(
            agent_name="insurance", domain=Domain.INSURANCE, session_id=session_id
        )

        coordinator.register_specialist("investment", InvestmentAgent(inv_config))
        coordinator.register_specialist("customer", CustomerAgent(cust_config))
        coordinator.register_specialist("insurance", InsuranceAgent(ins_config))

        # Verify all registered
        status = coordinator.get_status()
        assert len(status["registered_agents"]) == 3
        assert "investment" in status["registered_agents"]
        assert "customer" in status["registered_agents"]
        assert "insurance" in status["registered_agents"]


def test_task_decomposition_for_cross_domain():
    """Test that cross-domain queries generate multiple tasks."""
    from src.coordinator.intent_classifier import IntentClassifier, IntentType, Domain
    from src.coordinator.task_decomposer import TaskDecomposer

    classifier = IntentClassifier()
    decomposer = TaskDecomposer()

    result = classifier.classify("客户持仓亏损，保单能贷多少")
    assert result.intent_type == IntentType.CROSS_DOMAIN
    assert len(result.involved_domains) >= 2

    tasks = decomposer.decompose("客户持仓亏损，保单能贷多少", result)
    assert len(tasks) >= 2

    domains = {t.domain for t in tasks}
    assert Domain.INVESTMENT in domains
    assert Domain.INSURANCE in domains