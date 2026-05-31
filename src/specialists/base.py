"""Base class for specialist agents using qwen-agent."""
from typing import Dict, List, Optional
from qwen_agent.agents import Assistant
from qwen_agent.llm.schema import Message

from ..tools.config import get_settings


class SpecialistAgent(Assistant):
    """Specialist agent based on qwen-agent Assistant."""

    NAME: str = "specialist"
    DESCRIPTION: str = "A financial specialist agent"
    SYSTEM_MESSAGE: str = """你是一个专业的金融领域助手。"""

    def __init__(
        self,
        session_id: str,
        llm_config: Optional[Dict] = None,
        tools: Optional[List] = None,
        **kwargs
    ):
        self.session_id = session_id
        if llm_config is None:
            settings = get_settings()
            llm_config = {
                'model': settings.model_name,
                'model_type': settings.model_type,
            }
        super().__init__(
            llm=llm_config,
            system_message=self.SYSTEM_MESSAGE,
            function_list=tools or [],
            name=self.NAME,
            description=self.DESCRIPTION,
            **kwargs
        )
