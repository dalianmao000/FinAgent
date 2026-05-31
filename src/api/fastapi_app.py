"""FastAPI for FinAgent Unified - 可选的 FastAPI 替代方案."""
from typing import Dict, Any, Optional
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from ..coordinator.agent import CoordinatorAgent
from ..specialists.investment.agent import InvestmentAgent
from ..specialists.customer.agent import CustomerAgent
from ..specialists.insurance.agent import InsuranceAgent


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class CustomerRequest(BaseModel):
    customer_id: str
    name: str = "未知客户"
    total_assets: float = 0
    risk_level: str = "R1"


class ChatResponse(BaseModel):
    session_id: str
    response: str


class StatusResponse(BaseModel):
    session_id: str
    specialist_count: int
    specialists: list


class CustomerResponse(BaseModel):
    status: str
    customer: Dict[str, Any]


class HealthResponse(BaseModel):
    status: str
    service: str


class SessionsResponse(BaseModel):
    sessions: list
    count: int


_agents: Dict[str, CoordinatorAgent] = {}


def get_or_create_coordinator(session_id: str) -> CoordinatorAgent:
    """Get or create coordinator for session."""
    if session_id not in _agents:
        investment_agent = InvestmentAgent(session_id=session_id)
        customer_agent = CustomerAgent(session_id=session_id)
        insurance_agent = InsuranceAgent(session_id=session_id)

        coordinator = CoordinatorAgent(
            session_id=session_id,
            specialists=[investment_agent, customer_agent, insurance_agent]
        )

        _agents[session_id] = coordinator

    return _agents[session_id]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events."""
    print("FinAgent Unified FastAPI started")
    yield
    print("FinAgent Unified FastAPI shutdown")


app = FastAPI(
    title="FinAgent Unified API",
    description="金融智能顾问统一平台 API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/v1/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """Handle chat requests."""
    session_id = request.session_id or str(uuid.uuid4())
    coordinator = get_or_create_coordinator(session_id)
    response = coordinator.process(request.message)

    return ChatResponse(session_id=session_id, response=response)


@app.get("/api/v1/session/{session_id}/status", response_model=StatusResponse)
def status(session_id: str):
    """Get session status."""
    if session_id not in _agents:
        raise HTTPException(status_code=404, detail="Session not found")

    coordinator = _agents[session_id]
    status_info = coordinator.get_status()

    return StatusResponse(**status_info)


@app.post("/api/v1/session/{session_id}/customer", response_model=CustomerResponse)
def set_customer(session_id: str, request: CustomerRequest):
    """Set current customer for session."""
    if session_id not in _agents:
        get_or_create_coordinator(session_id)

    _customer_store = {}
    _customer_store[session_id] = {
        "customer_id": request.customer_id,
        "name": request.name,
        "total_assets": request.total_assets,
        "risk_level": request.risk_level
    }

    return CustomerResponse(
        status="success",
        customer={
            "customer_id": request.customer_id,
            "name": request.name,
            "total_assets": request.total_assets,
            "risk_level": request.risk_level
        }
    )


@app.get("/api/v1/health", response_model=HealthResponse)
def health():
    """Health check endpoint."""
    return HealthResponse(status="healthy", service="finagent-unified")


@app.get("/api/v1/sessions", response_model=SessionsResponse)
def list_sessions():
    """List all active sessions."""
    return SessionsResponse(sessions=list(_agents.keys()), count=len(_agents))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
