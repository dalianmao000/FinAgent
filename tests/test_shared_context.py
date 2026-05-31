"""Tests for shared context."""
import pytest
from unittest.mock import MagicMock, patch
from src.message_bus.shared_context import SharedContext, CustomerContext


def test_customer_context():
    """Test CustomerContext model."""
    ctx = CustomerContext(
        customer_id="C001",
        name="王总",
        total_assets=5000000,
        risk_level="R4"
    )
    assert ctx.customer_id == "C001"
    assert ctx.name == "王总"
    assert ctx.total_assets == 5000000
    assert ctx.risk_level == "R4"


def test_shared_context_set_get():
    """Test setting and getting values."""
    with patch('redis.Redis') as mock_redis_class:
        mock_redis = MagicMock()
        mock_redis_class.return_value = mock_redis

        ctx = SharedContext("test-session-001", redis_client=mock_redis)

        # Test customer context
        customer = CustomerContext(
            customer_id="C001",
            name="王总",
            total_assets=5000000,
            risk_level="R4"
        )
        ctx.set_customer(customer)

        # Verify redis was called correctly
        assert mock_redis.set.called

        # Mock get to return the customer data
        mock_redis.get.return_value = customer.model_dump_json()
        retrieved = ctx.get_customer()

        assert retrieved is not None
        assert retrieved.customer_id == "C001"
        assert retrieved.name == "王总"


def test_shared_context_history():
    """Test conversation history."""
    with patch('redis.Redis') as mock_redis_class:
        mock_redis = MagicMock()
        mock_redis_class.return_value = mock_redis
        mock_redis.lrange.return_value = []

        ctx = SharedContext("test-session-001", redis_client=mock_redis)

        ctx.add_history("user", "查询持仓", ["investment"])
        assert mock_redis.rpush.called

        mock_redis.lrange.return_value = [
            '{"role": "user", "content": "查询持仓", "agents": ["investment"]}'
        ]
        history = ctx.get_history()
        assert len(history) == 1
        assert history[0]["role"] == "user"


def test_shared_context_agent_data():
    """Test agent data storage."""
    with patch('redis.Redis') as mock_redis_class:
        mock_redis = MagicMock()
        mock_redis_class.return_value = mock_redis
        mock_redis.hget.return_value = None

        ctx = SharedContext("test-session-001", redis_client=mock_redis)

        ctx.set_agent_data("investment", {"positions": [{"stock": "茅台"}]})
        assert mock_redis.hset.called

        mock_redis.hget.return_value = '{"positions": [{"stock": "茅台"}]}'
        data = ctx.get_agent_data("investment")
        assert data["positions"][0]["stock"] == "茅台"


def test_shared_context_tasks():
    """Test task tracking."""
    with patch('redis.Redis') as mock_redis_class:
        mock_redis = MagicMock()
        mock_redis_class.return_value = mock_redis
        mock_redis.hget.return_value = None
        mock_redis.hgetall.return_value = {}

        ctx = SharedContext("test-session-001", redis_client=mock_redis)

        ctx.set_task("task_001", "investment", "pending")
        assert mock_redis.hset.called