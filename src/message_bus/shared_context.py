"""Shared context store using Redis."""
import json
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
import redis


class CustomerContext(BaseModel):
    """Customer context data."""
    customer_id: str
    name: str
    total_assets: float = 0
    risk_level: str = "R1"
    lifecycle_stage: str = ""
    other_info: Dict[str, Any] = Field(default_factory=dict)


class SharedContext:
    """Shared context store for multi-agent conversation."""

    CUSTOMER_KEY = "customer"
    HISTORY_KEY = "history"
    DATA_KEY = "data"
    TASKS_KEY = "tasks"
    META_KEY = "meta"

    def __init__(self, session_id: str, redis_client: Optional[redis.Redis] = None):
        self.session_id = session_id
        self.prefix = f"session:{session_id}"
        if redis_client:
            self.redis = redis_client
        else:
            self.redis = redis.Redis(host='localhost', port=6379, decode_responses=True)

    def _key(self, suffix: str) -> str:
        """Get full key with prefix."""
        return f"{self.prefix}:{suffix}"

    # Session metadata
    def set_meta(self, user_id: str, user_name: str, org: str = ""):
        """Set session metadata."""
        meta = {"user_id": user_id, "user_name": user_name, "org": org}
        self.redis.set(self._key(self.META_KEY), json.dumps(meta))

    def get_meta(self) -> Dict[str, str]:
        """Get session metadata."""
        data = self.redis.get(self._key(self.META_KEY))
        if data:
            return json.loads(data)
        return {}

    # Customer context
    def set_customer(self, customer: CustomerContext):
        """Set current customer context."""
        self.redis.set(self._key(self.CUSTOMER_KEY), customer.model_dump_json())

    def get_customer(self) -> Optional[CustomerContext]:
        """Get current customer context."""
        data = self.redis.get(self._key(self.CUSTOMER_KEY))
        if data:
            return CustomerContext.model_validate_json(data)
        return None

    def clear_customer(self):
        """Clear customer context."""
        self.redis.delete(self._key(self.CUSTOMER_KEY))

    # Conversation history
    def add_history(self, role: str, content: str, agents: List[str]):
        """Add to conversation history."""
        entry = {"role": role, "content": content, "agents": agents}
        self.redis.rpush(self._key(self.HISTORY_KEY), json.dumps(entry))

    def get_history(self) -> List[Dict[str, Any]]:
        """Get conversation history."""
        entries = self.redis.lrange(self._key(self.HISTORY_KEY), 0, -1)
        return [json.loads(e) for e in entries]

    # Agent data collection
    def set_agent_data(self, agent_name: str, data: Dict[str, Any]):
        """Store data collected by an agent."""
        self.redis.hset(self._key(self.DATA_KEY), agent_name, json.dumps(data))

    def get_agent_data(self, agent_name: str) -> Dict[str, Any]:
        """Get data collected by an agent."""
        data = self.redis.hget(self._key(self.DATA_KEY), agent_name)
        if data:
            return json.loads(data)
        return {}

    def get_all_agent_data(self) -> Dict[str, Dict[str, Any]]:
        """Get all agent data."""
        all_data = self.redis.hgetall(self._key(self.DATA_KEY))
        return {k: json.loads(v) for k, v in all_data.items()}

    # Task tracking
    def set_task(self, task_id: str, agent: str, status: str):
        """Set task status."""
        self.redis.hset(self._key(self.TASKS_KEY), task_id, json.dumps({
            "agent": agent, "status": status
        }))

    def get_task(self, task_id: str) -> Optional[Dict[str, str]]:
        """Get task status."""
        data = self.redis.hget(self._key(self.TASKS_KEY), task_id)
        if data:
            return json.loads(data)
        return None

    def get_pending_tasks(self) -> List[str]:
        """Get list of pending task IDs."""
        all_tasks = self.redis.hgetall(self._key(self.TASKS_KEY))
        return [
            task_id for task_id, data in all_tasks.items()
            if json.loads(data).get("status") == "pending"
        ]

    # Cleanup
    def clear_all(self):
        """Clear all context data for this session."""
        keys = [
            self._key(self.CUSTOMER_KEY),
            self._key(self.HISTORY_KEY),
            self._key(self.DATA_KEY),
            self._key(self.TASKS_KEY),
            self._key(self.META_KEY)
        ]
        for key in keys:
            self.redis.delete(key)