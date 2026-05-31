"""Message format definitions for inter-agent communication."""
from datetime import datetime
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import uuid


class MessageType(str, Enum):
    """Message types for agent communication."""
    TASK = "task"
    RESULT = "result"
    EVENT = "event"
    ERROR = "error"
    DATA_REQUEST = "data.request"
    DATA_RESPONSE = "data.response"


class EventType(str, Enum):
    """Event types for the message bus."""
    # Coordinator -> Specialist
    TASK_DISPATCH = "task.dispatch"
    TASK_CANCEL = "task.cancel"
    # Specialist -> Coordinator
    TASK_COMPLETE = "task.complete"
    TASK_FAILED = "task.failed"
    # Specialist <-> Specialist
    DATA_REQUEST = "data.request"
    DATA_RESPONSE = "data.response"
    SYNC_REQUIRED = "sync.required"
    # System events
    SESSION_START = "session.start"
    SESSION_END = "session.end"


class AgentMessage(BaseModel):
    """Base message format for agent communication."""

    msg_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    sender: str  # "coordinator" | "investment" | "customer" | "insurance"
    receivers: List[str]  # Target agent names
    msg_type: MessageType
    content: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.now)
    correlation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    class Config:
        use_enum_values = True


class TaskMessage(AgentMessage):
    """Task dispatch message."""
    def __init__(self, **data):
        data["msg_type"] = MessageType.TASK
        super().__init__(**data)


class ResultMessage(AgentMessage):
    """Result return message."""
    def __init__(self, **data):
        data["msg_type"] = MessageType.RESULT
        super().__init__(**data)