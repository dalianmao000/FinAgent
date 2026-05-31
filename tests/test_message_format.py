"""Tests for message format."""
import pytest
from datetime import datetime
from src.message_bus.message_format import AgentMessage, EventType, MessageType, TaskMessage, ResultMessage


def test_agent_message_creation():
    """Test creating an AgentMessage."""
    msg = AgentMessage(
        session_id="test-session-001",
        sender="coordinator",
        receivers=["investment", "customer"],
        msg_type=MessageType.TASK,
        content={"task_id": "task_001", "description": "test task"}
    )
    assert msg.session_id == "test-session-001"
    assert msg.sender == "coordinator"
    assert msg.receivers == ["investment", "customer"]
    assert msg.msg_type == MessageType.TASK
    assert msg.content["task_id"] == "task_001"


def test_agent_message_auto_fields():
    """Test auto-generated fields."""
    msg = AgentMessage(
        session_id="test-session-001",
        sender="coordinator",
        receivers=["investment"],
        msg_type=MessageType.TASK,
        content={}
    )
    assert msg.msg_id is not None
    assert len(msg.msg_id) > 0
    assert msg.timestamp is not None
    assert isinstance(msg.timestamp, datetime)
    assert msg.correlation_id is not None


def test_message_type_enum():
    """Test MessageType enum values."""
    assert MessageType.TASK.value == "task"
    assert MessageType.RESULT.value == "result"
    assert MessageType.EVENT.value == "event"


def test_event_type_enum():
    """Test EventType enum values."""
    assert EventType.TASK_DISPATCH.value == "task.dispatch"
    assert EventType.TASK_COMPLETE.value == "task.complete"
    assert EventType.SESSION_START.value == "session.start"


def test_task_message():
    """Test TaskMessage convenience class."""
    msg = TaskMessage(
        session_id="test-session",
        sender="coordinator",
        receivers=["investment"],
        content={"task_id": "t1"}
    )
    assert msg.msg_type == MessageType.TASK


def test_result_message():
    """Test ResultMessage convenience class."""
    msg = ResultMessage(
        session_id="test-session",
        sender="investment",
        receivers=["coordinator"],
        content={"task_id": "t1", "result": "success"}
    )
    assert msg.msg_type == MessageType.RESULT