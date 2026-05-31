"""Intent classification for user queries."""
from enum import Enum
from typing import List, Set
from pydantic import BaseModel

from ..tools.llm import get_llm


class IntentType(str, Enum):
    """Type of user intent."""
    SINGLE_DOMAIN = "single_domain"
    CROSS_DOMAIN = "cross_domain"


class Domain(str, Enum):
    """Domain areas."""
    INVESTMENT = "investment"  # 股票、基金、持仓
    CUSTOMER = "customer"     # 客户画像、分群、流失
    INSURANCE = "insurance"   # 保险条款、保单、贷款
    UNKNOWN = "unknown"


class ClassificationResult(BaseModel):
    """Result of intent classification."""
    intent_type: IntentType
    primary_domain: Domain
    involved_domains: List[Domain]
    query_summary: str
    requires_collaboration: bool


class IntentClassifier:
    """Classifier for user query intent."""

    # Keyword patterns for each domain
    INVESTMENT_KEYWORDS = {
        "股票", "持仓", "盈亏", "茅台", "股价", "上证", "深证",
        "基金", "指数", "涨跌", "市值", "浮亏", "浮盈",
        "ARIMA", "布林带", "技术指标", "预测", "行情"
    }

    CUSTOMER_KEYWORDS = {
        "客户", "VIP", "高净值", "分群", "聚类", "流失",
        "资产预测", "客户画像", "复购", "营销", "转化",
        "KMeans", "LightGBM", "SHAP", "决策树"
    }

    INSURANCE_KEYWORDS = {
        "保险", "保单", "条款", "理赔", "贷款", "寿险",
        "重疾", "医疗", "意外", "投保", "受益人",
        "现金价值", "犹豫期", "等待期"
    }

    def __init__(self, llm=None):
        self.llm = llm or get_llm()

    def classify(self, query: str) -> ClassificationResult:
        """Classify user query intent."""
        # Keyword-based quick classification
        keywords_found = self._find_keywords(query)
        involved_domains = self._keywords_to_domains(keywords_found)

        if len(involved_domains) == 0:
            return ClassificationResult(
                intent_type=IntentType.SINGLE_DOMAIN,
                primary_domain=Domain.UNKNOWN,
                involved_domains=[Domain.UNKNOWN],
                query_summary=query,
                requires_collaboration=False
            )

        if len(involved_domains) == 1:
            return ClassificationResult(
                intent_type=IntentType.SINGLE_DOMAIN,
                primary_domain=involved_domains[0],
                involved_domains=involved_domains,
                query_summary=query,
                requires_collaboration=False
            )

        # Cross-domain query
        return ClassificationResult(
            intent_type=IntentType.CROSS_DOMAIN,
            primary_domain=involved_domains[0],
            involved_domains=involved_domains,
            query_summary=query,
            requires_collaboration=True
        )

    def _find_keywords(self, query: str) -> Set[str]:
        """Find domain keywords in query."""
        keywords = set()
        for kw in self.INVESTMENT_KEYWORDS:
            if kw in query:
                keywords.add(f"investment:{kw}")
        for kw in self.CUSTOMER_KEYWORDS:
            if kw in query:
                keywords.add(f"customer:{kw}")
        for kw in self.INSURANCE_KEYWORDS:
            if kw in query:
                keywords.add(f"insurance:{kw}")
        return keywords

    def _keywords_to_domains(self, keywords: Set[str]) -> List[Domain]:
        """Convert keywords to domains."""
        domains = []
        for kw in keywords:
            domain = kw.split(":")[0]
            if domain == "investment" and Domain.INVESTMENT not in domains:
                domains.append(Domain.INVESTMENT)
            elif domain == "customer" and Domain.CUSTOMER not in domains:
                domains.append(Domain.CUSTOMER)
            elif domain == "insurance" and Domain.INSURANCE not in domains:
                domains.append(Domain.INSURANCE)
        return domains