"""Tests for Redis pub/sub."""
import pytest
from unittest.mock import MagicMock, patch
from src.message_bus.redis_pubsub import MessageBus, AgentCallback


def test_message_bus_subscribe():
    """Test message bus subscription."""
    with patch('redis.Redis') as mock_redis_class:
        mock_redis = MagicMock()
        mock_redis_class.return_value = mock_redis
        mock_pubsub = MagicMock()
        mock_redis.pubsub.return_value = mock_pubsub

        bus = MessageBus()
        assert bus.pubsub is not None
        assert bus.subscribers == {}


def test_agent_callback():
    """Test agent callback."""
    callback = AgentCallback("investment")
    assert callback.agent_name == "investment"
    assert callback.callback is None

    def test_handler(msg):
        pass

    callback = AgentCallback("investment", test_handler)
    assert callback.agent_name == "investment"
    assert callback.callback is test_handler


def test_message_bus_publish():
    """Test message publishing."""
    with patch('redis.Redis') as mock_redis_class:
        mock_redis = MagicMock()
        mock_redis_class.return_value = mock_redis

        bus = MessageBus()
        bus.redis_client = mock_redis

        from src.message_bus.message_format import AgentMessage, MessageType
        msg = AgentMessage(
            session_id="test",
            sender="coordinator",
            receivers=["investment"],
            msg_type=MessageType.TASK,
            content={"task_id": "t1"}
        )

        bus.publish(msg)
        assert mock_redis.publish.called


def test_channel_name():
    """Test channel name generation."""
    with patch('redis.Redis') as mock_redis_class:
        mock_redis = MagicMock()
        mock_redis_class.return_value = mock_redis

        bus = MessageBus()
        channel = bus._channel_name("investment")
        assert channel == "finagent:channel:investment"