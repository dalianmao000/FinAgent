"""Specialist Agent Base Class"""
__version__ = "0.1.0"


class SpecialistAgent:
    """Base class for specialist agents in the FinAgent platform."""

    def __init__(self, agent_id: str, agent_type: str):
        self.agent_id = agent_id
        self.agent_type = agent_type

    def process(self, message: dict) -> dict:
        """Process a message and return a response."""
        raise NotImplementedError("Subclasses must implement process()")