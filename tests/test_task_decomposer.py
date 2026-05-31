"""Tests for task decomposer."""
import pytest
from src.coordinator.task_decomposer import TaskDecomposer, Task, TaskType
from src.coordinator.intent_classifier import Domain, IntentType, ClassificationResult


def test_task_model():
    """Test Task model."""
    task = Task(
        task_id="task_001",
        domain=Domain.INVESTMENT,
        task_type=TaskType.QUERY,
        description="查询客户持仓",
        parallel=True
    )
    assert task.task_id == "task_001"
    assert task.domain == Domain.INVESTMENT
    assert task.task_type == TaskType.QUERY
    assert task.parallel is True


def test_task_model_auto_id():
    """Test Task model auto-generated ID."""
    task = Task(
        domain=Domain.INVESTMENT,
        task_type=TaskType.QUERY,
        description="测试"
    )
    assert task.task_id is not None
    assert task.task_id.startswith("task_")


def test_task_type_enum():
    """Test TaskType enum values."""
    assert TaskType.QUERY.value == "query"
    assert TaskType.ANALYSIS.value == "analysis"
    assert TaskType.PREDICTION.value == "prediction"
    assert TaskType.RAG.value == "rag"


def test_task_decomposer_single_domain_investment():
    """Test decomposing single domain query."""
    decomposer = TaskDecomposer()
    classification = ClassificationResult(
        intent_type=IntentType.SINGLE_DOMAIN,
        primary_domain=Domain.INVESTMENT,
        involved_domains=[Domain.INVESTMENT],
        query_summary="查询茅台持仓",
        requires_collaboration=False
    )
    tasks = decomposer.decompose("查询茅台持仓", classification)
    assert len(tasks) >= 1
    assert all(t.domain == Domain.INVESTMENT for t in tasks)


def test_task_decomposer_single_domain_customer():
    """Test decomposing customer query."""
    decomposer = TaskDecomposer()
    classification = ClassificationResult(
        intent_type=IntentType.SINGLE_DOMAIN,
        primary_domain=Domain.CUSTOMER,
        involved_domains=[Domain.CUSTOMER],
        query_summary="查询VIP客户",
        requires_collaboration=False
    )
    tasks = decomposer.decompose("查询VIP客户", classification)
    assert len(tasks) >= 1
    assert all(t.domain == Domain.CUSTOMER for t in tasks)


def test_task_decomposer_single_domain_insurance():
    """Test decomposing insurance query."""
    decomposer = TaskDecomposer()
    classification = ClassificationResult(
        intent_type=IntentType.SINGLE_DOMAIN,
        primary_domain=Domain.INSURANCE,
        involved_domains=[Domain.INSURANCE],
        query_summary="查询保单贷款",
        requires_collaboration=False
    )
    tasks = decomposer.decompose("查询保单贷款", classification)
    assert len(tasks) >= 1
    assert all(t.domain == Domain.INSURANCE for t in tasks)


def test_task_decomposer_cross_domain():
    """Test decomposing cross-domain query."""
    decomposer = TaskDecomposer()
    classification = ClassificationResult(
        intent_type=IntentType.CROSS_DOMAIN,
        primary_domain=Domain.CUSTOMER,
        involved_domains=[Domain.CUSTOMER, Domain.INVESTMENT, Domain.INSURANCE],
        query_summary="客户持仓茅台亏了能办保单贷款吗",
        requires_collaboration=True
    )
    tasks = decomposer.decompose("客户持仓茅台亏了能办保单贷款吗", classification)
    assert len(tasks) >= 3
    domain_set = {t.domain for t in tasks}
    assert Domain.INVESTMENT in domain_set
    assert Domain.INSURANCE in domain_set
    assert Domain.CUSTOMER in domain_set


def test_task_decomposer_mark_dependencies():
    """Test dependency marking for cross-domain tasks."""
    decomposer = TaskDecomposer()
    classification = ClassificationResult(
        intent_type=IntentType.CROSS_DOMAIN,
        primary_domain=Domain.INVESTMENT,
        involved_domains=[Domain.INVESTMENT, Domain.CUSTOMER],
        query_summary="客户持仓分析",
        requires_collaboration=True
    )
    tasks = decomposer.decompose("客户持仓茅台亏了", classification)
    # After marking dependencies, customer task should depend on investment task
    customer_tasks = [t for t in tasks if t.domain == Domain.CUSTOMER]
    if customer_tasks and len(tasks) > 1:
        assert len(customer_tasks[0].depends_on) > 0