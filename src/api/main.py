"""Flask API for FinAgent Unified."""
from flask import Flask, request, jsonify
from typing import Dict, Any
import uuid

from ..coordinator.agent import CoordinatorAgent, AgentConfig
from ..coordinator.intent_classifier import Domain
from ..specialists.investment.agent import InvestmentAgent
from ..specialists.customer.agent import CustomerAgent
from ..specialists.insurance.agent import InsuranceAgent
from ..specialists.base import SpecialistConfig


def create_app() -> Flask:
    """Create and configure Flask application."""
    app = Flask(__name__)
    app.secret_key = "finagent-secret-key-change-in-production"

    # Initialize agents
    _agents: Dict[str, CoordinatorAgent] = {}

    def get_or_create_coordinator(session_id: str) -> CoordinatorAgent:
        """Get or create coordinator for session."""
        if session_id not in _agents:
            config = AgentConfig(agent_name="coordinator", session_id=session_id)
            coordinator = CoordinatorAgent(session_id=session_id, config=config)

            # Register specialist agents
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

            _agents[session_id] = coordinator

        return _agents[session_id]

    @app.route("/api/v1/chat", methods=["POST"])
    def chat():
        """Handle chat requests."""
        data = request.get_json()
        message = data.get("message", "")
        session_id = data.get("session_id", str(uuid.uuid4()))

        coordinator = get_or_create_coordinator(session_id)
        response = coordinator.process(message)

        return jsonify({
            "session_id": session_id,
            "response": response
        })

    @app.route("/api/v1/session/<session_id>/status", methods=["GET"])
    def status(session_id: str):
        """Get session status."""
        if session_id not in _agents:
            return jsonify({"error": "Session not found"}), 404

        coordinator = _agents[session_id]
        status_info = coordinator.get_status()

        # Convert CustomerContext to dict for JSON serialization
        if status_info.get("customer"):
            status_info["customer"] = status_info["customer"].model_dump()

        return jsonify(status_info)

    @app.route("/api/v1/session/<session_id>/customer", methods=["POST"])
    def set_customer(session_id: str):
        """Set current customer for session."""
        data = request.get_json()
        customer_id = data.get("customer_id")
        name = data.get("name", "未知客户")
        total_assets = data.get("total_assets", 0)
        risk_level = data.get("risk_level", "R1")
        lifecycle_stage = data.get("lifecycle_stage", "")

        coordinator = get_or_create_coordinator(session_id)

        from ..message_bus.shared_context import CustomerContext
        customer = CustomerContext(
            customer_id=customer_id or "unknown",
            name=name,
            total_assets=total_assets,
            risk_level=risk_level,
            lifecycle_stage=lifecycle_stage
        )
        coordinator.shared_context.set_customer(customer)

        return jsonify({"status": "success", "customer": customer.model_dump()})

    @app.route("/api/v1/health", methods=["GET"])
    def health():
        """Health check endpoint."""
        return jsonify({"status": "healthy", "service": "finagent-unified"})

    @app.route("/api/v1/sessions", methods=["GET"])
    def list_sessions():
        """List all active sessions."""
        return jsonify({
            "sessions": list(_agents.keys()),
            "count": len(_agents)
        })

    return app


# Application instance
app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)