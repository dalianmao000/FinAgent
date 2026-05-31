"""Task decomposition for user queries."""
from enum import Enum
from typing import List
from pydantic import BaseModel, Field
import uuid

from .intent_classifier import ClassificationResult, Domain


class TaskType(str, Enum):
    """Type of task."""
    QUERY = "query"
    ANALYSIS = "analysis"
    PREDICTION = "prediction"
    RAG = "rag"


class Task(BaseModel):
    """Decomposed task."""
    task_id: str = Field(default_factory=lambda: f"task_{uuid.uuid4().hex[:8]}")
    domain: Domain
    task_type: TaskType
    description: str
    parallel: bool = True
    depends_on: List[str] = Field(default_factory=list)


class TaskDecomposer:
    """Decomposes user queries into executable tasks."""

    def __init__(self):
        pass

    def decompose(self, query: str, classification: ClassificationResult) -> List[Task]:
        """Decompose query into tasks based on classification."""
        tasks = []

        for domain in classification.involved_domains:
            domain_tasks = self._decompose_for_domain(query, domain)
            tasks.extend(domain_tasks)

        # Mark dependencies for cross-domain tasks
        if classification.requires_collaboration:
            tasks = self._mark_dependencies(tasks)

        return tasks

    def _decompose_for_domain(self, query: str, domain: Domain) -> List[Task]:
        """Decompose tasks for a specific domain."""
        tasks = []

        if domain == Domain.INVESTMENT:
            if any(kw in query for kw in ["持仓", "持有", "买"]):
                tasks.append(Task(
                    domain=Domain.INVESTMENT,
                    task_type=TaskType.QUERY,
                    description="查询客户持仓情况"
                ))
            if any(kw in query for kw in ["亏", "盈", "赚", "赔"]):
                tasks.append(Task(
                    domain=Domain.INVESTMENT,
                    task_type=TaskType.ANALYSIS,
                    description="计算盈亏情况"
                ))
            if any(kw in query for kw in ["预测", "未来", "走势"]):
                tasks.append(Task(
                    domain=Domain.INVESTMENT,
                    task_type=TaskType.PREDICTION,
                    description="预测股价走势"
                ))
            if any(kw in query for kw in ["技术指标", "布林带", "K线"]):
                tasks.append(Task(
                    domain=Domain.INVESTMENT,
                    task_type=TaskType.ANALYSIS,
                    description="技术指标分析"
                ))
            if not tasks:
                tasks.append(Task(
                    domain=Domain.INVESTMENT,
                    task_type=TaskType.QUERY,
                    description="查询投资相关信息"
                ))

        elif domain == Domain.CUSTOMER:
            if any(kw in query for kw in ["客户", "VIP", "高净值"]):
                tasks.append(Task(
                    domain=Domain.CUSTOMER,
                    task_type=TaskType.QUERY,
                    description="查询客户画像"
                ))
            if any(kw in query for kw in ["分群", "聚类", "分类"]):
                tasks.append(Task(
                    domain=Domain.CUSTOMER,
                    task_type=TaskType.ANALYSIS,
                    description="客户分群分析"
                ))
            if any(kw in query for kw in ["流失", "离开", "不续"]):
                tasks.append(Task(
                    domain=Domain.CUSTOMER,
                    task_type=TaskType.PREDICTION,
                    description="流失预警分析"
                ))
            if not tasks:
                tasks.append(Task(
                    domain=Domain.CUSTOMER,
                    task_type=TaskType.QUERY,
                    description="查询客户信息"
                ))

        elif domain == Domain.INSURANCE:
            if any(kw in query for kw in ["保险", "条款", "保障"]):
                tasks.append(Task(
                    domain=Domain.INSURANCE,
                    task_type=TaskType.RAG,
                    description="查询保险条款"
                ))
            if any(kw in query for kw in ["保单", "保单贷款", "现金价值"]):
                tasks.append(Task(
                    domain=Domain.INSURANCE,
                    task_type=TaskType.QUERY,
                    description="查询保单信息"
                ))
            if any(kw in query for kw in ["贷款", "能贷"]):
                tasks.append(Task(
                    domain=Domain.INSURANCE,
                    task_type=TaskType.ANALYSIS,
                    description="保单贷款计算"
                ))
            if not tasks:
                tasks.append(Task(
                    domain=Domain.INSURANCE,
                    task_type=TaskType.RAG,
                    description="查询保险相关信息"
                ))

        return tasks

    def _mark_dependencies(self, tasks: List[Task]) -> List[Task]:
        """Mark dependencies between tasks."""
        for i, task in enumerate(tasks):
            if task.domain == Domain.CUSTOMER and i > 0:
                task.depends_on = [tasks[0].task_id]
        return tasks