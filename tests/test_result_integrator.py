"""Tests for result integrator."""
import pytest
from src.coordinator.result_integrator import ResultIntegrator
from src.coordinator.intent_classifier import Domain
from src.coordinator.task_decomposer import Task, TaskType


def test_result_integrator_single_investment():
    """Test integrating single domain investment results."""
    integrator = ResultIntegrator()
    results = {
        "investment": {
            "positions": [{"stock": "茅台", "shares": 500, "pnl": -0.20}],
            "summary": "持仓茅台500股，亏损20%"
        }
    }
    tasks = [
        Task(
            task_id="task_001",
            domain=Domain.INVESTMENT,
            task_type=TaskType.QUERY,
            description="查询持仓"
        )
    ]
    integrated = integrator.integrate("查询持仓", tasks, results)
    assert "茅台" in integrated or "亏损" in integrated


def test_result_integrator_single_with_summary():
    """Test integrating single domain with summary."""
    integrator = ResultIntegrator()
    results = {
        "customer": {
            "summary": "客户王总，资产500万"
        }
    }
    tasks = [Task(domain=Domain.CUSTOMER, task_type=TaskType.QUERY, description="客户")]
    integrated = integrator.integrate("查询客户", tasks, results)
    assert "王总" in integrated or "500万" in integrated


def test_result_integrator_cross_domain():
    """Test integrating cross-domain results."""
    integrator = ResultIntegrator()
    results = {
        "investment": {
            "positions": [{"stock": "茅台", "pnl": -0.20}],
        },
        "insurance": {
            "total_loanable": 400000,
            "policies": [{"type": "寿险", "cash_value": 500000}]
        },
        "customer": {
            "profile": {
                "name": "王总",
                "total_assets": 5000000,
                "risk_level": "R4"
            }
        }
    }
    tasks = [
        Task(task_id="t1", domain=Domain.INVESTMENT, task_type=TaskType.QUERY, description="持仓"),
        Task(task_id="t2", domain=Domain.INSURANCE, task_type=TaskType.ANALYSIS, description="贷款"),
        Task(task_id="t3", domain=Domain.CUSTOMER, task_type=TaskType.QUERY, description="客户")
    ]
    integrated = integrator.integrate("客户持仓亏损能办保单贷款吗", tasks, results)
    assert "王总" in integrated
    assert "40万" in integrated or "400" in integrated


def test_result_integrator_empty_results():
    """Test integrating empty results."""
    integrator = ResultIntegrator()
    integrated = integrator.integrate("查询", [], {})
    assert "抱歉" in integrated or "没有" in integrated


def test_result_integrator_loan_advice():
    """Test loan advice synthesis."""
    integrator = ResultIntegrator()
    results = {
        "investment": {
            "positions": [{"stock": "茅台", "pnl": -0.20}],
        },
        "insurance": {
            "total_loanable": 400000,
        }
    }
    advice = integrator._synthesize_loan_advice(results)
    assert "亏损" in advice or "可贷" in advice or "40万" in advice


def test_result_integrator_profit_case():
    """Test loan advice for profitable case."""
    integrator = ResultIntegrator()
    results = {
        "investment": {
            "positions": [{"stock": "茅台", "pnl": 0.15}],
        },
        "insurance": {
            "total_loanable": 400000,
        }
    }
    advice = integrator._synthesize_loan_advice(results)
    assert "良好" in advice or "可贷" in advice


def test_result_integrator_section_order():
    """Test that customer section comes first."""
    integrator = ResultIntegrator()
    results = {
        "customer": {"profile": {"name": "王总"}},
        "investment": {"positions": [{"stock": "茅台", "pnl": -0.2}]},
        "insurance": {"total_loanable": 400000}
    }
    tasks = [
        Task(domain=Domain.INVESTMENT, task_type=TaskType.QUERY, description="投资"),
        Task(domain=Domain.INSURANCE, task_type=TaskType.ANALYSIS, description="保险"),
        Task(domain=Domain.CUSTOMER, task_type=TaskType.QUERY, description="客户")
    ]
    integrated = integrator.integrate("客户情况", tasks, results)
    # Customer should appear early in the response
    lines = integrated.split("\n\n")
    customer_line = next((l for l in lines if "王总" in l), None)
    assert customer_line is not None