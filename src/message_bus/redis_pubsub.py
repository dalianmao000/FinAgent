"""Redis Pub/Sub implementation for agent messaging."""
import json
import threading
from typing import Callable, Dict, Optional
from dataclasses import dataclass
import redis

from .message_format import AgentMessage, MessageType


@dataclass
class AgentCallback:
    """Callback for an agent's message handler."""
    agent_name: str
    callback: Optional[Callable] = None


class MessageBus:
    """Redis-based publish/subscribe message bus for agent communication."""

    CHANNEL_PREFIX = "finagent:channel:"

    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        self.redis_client = redis.from_url(redis_url, decode_responses=True)
        self.pubsub = self.redis_client.pubsub()
        self.subscribers: Dict[str, AgentCallback] = {}
        self._listener_thread: Optional[threading.Thread] = None
        self._running = False

    def _channel_name(self, agent_name: str) -> str:
        """Get channel name for an agent."""
        return f"{self.CHANNEL_PREFIX}{agent_name}"

    def subscribe(self, agent_name: str, callback: Callable[[AgentMessage], None]):
        """Subscribe an agent to its message channel."""
        channel = self._channel_name(agent_name)
        self.pubsub.subscribe(channel)
        self.subscribers[agent_name] = AgentCallback(agent_name, callback)

    def unsubscribe(self, agent_name: str):
        """Unsubscribe an agent."""
        channel = self._channel_name(agent_name)
        self.pubsub.unsubscribe(channel)
        if agent_name in self.subscribers:
            del self.subscribers[agent_name]

    def publish(self, message: AgentMessage):
        """Publish a message to specified agents."""
        for receiver in message.receivers:
            channel = self._channel_name(receiver)
            self.redis_client.publish(channel, message.model_dump_json())

    def publish_to_agent(self, agent_name: str, message: AgentMessage):
        """Publish a message to a specific agent."""
        channel = self._channel_name(agent_name)
        self.redis_client.publish(channel, message.model_dump_json())

    def start_listening(self):
        """Start the message listener thread."""
        if self._running:
            return

        self._running = True
        self._listener_thread = threading.Thread(target=self._listen, daemon=True)
        self._listener_thread.start()

    def _listen(self):
        """Listen for messages on subscribed channels."""
        for message in self.pubsub.listen():
            if message["type"] != "message":
                continue

            channel = message["channel"]
            agent_name = channel.replace(self.CHANNEL_PREFIX, "")

            if agent_name in self.subscribers:
                callback_obj = self.subscribers[agent_name]
                if callback_obj.callback:
                    try:
                        msg_data = json.loads(message["data"])
                        agent_msg = AgentMessage(**msg_data)
                        callback_obj.callback(agent_msg)
                    except Exception as e:
                        print(f"Error processing message for {agent_name}: {e}")

    def stop_listening(self):
        """Stop the message listener thread."""
        self._running = False
        if self._listener_thread:
            self._listener_thread.join(timeout=1.0)
        self.pubsub.close()