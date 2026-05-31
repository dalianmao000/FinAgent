"""Flask API for FinAgent Unified - qwen-agent based."""
from flask import Flask, request, jsonify
from typing import Dict, Any
import uuid

from ..coordinator.agent import CoordinatorAgent
from ..specialists.investment.agent import InvestmentAgent
from ..specialists.customer.agent import CustomerAgent
from ..specialists.insurance.agent import InsuranceAgent


def create_app() -> Flask:
    """Create and configure Flask application."""
    app = Flask(__name__)
    app.secret_key = "finagent-secret-key-change-in-production"

    # Initialize agents
    _agents: Dict[str, CoordinatorAgent] = {}

    def get_or_create_coordinator(session_id: str) -> CoordinatorAgent:
        """Get or create coordinator for session."""
        if session_id not in _agents:
            # Create specialist agents
            investment_agent = InvestmentAgent(session_id=session_id)
            customer_agent = CustomerAgent(session_id=session_id)
            insurance_agent = InsuranceAgent(session_id=session_id)

            # Create coordinator with specialists
            coordinator = CoordinatorAgent(
                session_id=session_id,
                specialists=[investment_agent, customer_agent, insurance_agent]
            )

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

        return jsonify(status_info)

    @app.route("/api/v1/session/<session_id>/customer", methods=["POST"])
    def set_customer(session_id: str):
        """Set current customer for session (stored in-memory for now)."""
        data = request.get_json()
        customer_id = data.get("customer_id", "")
        name = data.get("name", "未知客户")
        total_assets = data.get("total_assets", 0)
        risk_level = data.get("risk_level", "R1")

        # Store customer info in session (simple in-memory storage)
        if session_id not in _agents:
            get_or_create_coordinator(session_id)

        # Store in a simple dict - in production would use Redis
        if not hasattr(set_customer, '_customer_store'):
            set_customer._customer_store = {}

        set_customer._customer_store[session_id] = {
            "customer_id": customer_id,
            "name": name,
            "total_assets": total_assets,
            "risk_level": risk_level
        }

        return jsonify({
            "status": "success",
            "customer": {
                "customer_id": customer_id,
                "name": name,
                "total_assets": total_assets,
                "risk_level": risk_level
            }
        })

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
