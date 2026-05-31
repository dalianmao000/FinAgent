"""Tests for intent classifier."""
import pytest
from src.coordinator.intent_classifier import IntentClassifier, IntentType, Domain, ClassificationResult


def test_intent_type_enum():
    """Test IntentType enum values."""
    assert IntentType.SINGLE_DOMAIN.value == "single_domain"
    assert IntentType.CROSS_DOMAIN.value == "cross_domain"


def test_domain_enum():
    """Test Domain enum values."""
    assert Domain.INVESTMENT.value == "investment"
    assert Domain.CUSTOMER.value == "customer"
    assert Domain.INSURANCE.value == "insurance"
    assert Domain.UNKNOWN.value == "unknown"


def test_intent_classifier_investment():
    """Test classifying investment query."""
    classifier = IntentClassifier()
    result = classifier.classify("帮我查一下茅台的持仓情况")
    assert result.primary_domain == Domain.INVESTMENT
    assert result.intent_type == IntentType.SINGLE_DOMAIN
    assert not result.requires_collaboration


def test_intent_classifier_customer():
    """Test classifying customer query."""
    classifier = IntentClassifier()
    result = classifier.classify("查询VIP客户的风险等级")
    assert result.primary_domain == Domain.CUSTOMER
    assert result.intent_type == IntentType.SINGLE_DOMAIN


def test_intent_classifier_insurance():
    """Test classifying insurance query."""
    classifier = IntentClassifier()
    result = classifier.classify("保单贷款能贷多少钱")
    assert result.primary_domain == Domain.INSURANCE
    assert result.intent_type == IntentType.SINGLE_DOMAIN


def test_intent_classifier_cross_domain():
    """Test classifying cross-domain query."""
    classifier = IntentClassifier()
    result = classifier.classify("我客户持仓茅台亏了，能办保单贷款吗")
    assert result.primary_domain in [Domain.INVESTMENT, Domain.CUSTOMER, Domain.INSURANCE]
    assert result.intent_type == IntentType.CROSS_DOMAIN
    assert result.requires_collaboration
    assert len(result.involved_domains) >= 2


def test_intent_classifier_unknown():
    """Test classifying unknown query."""
    classifier = IntentClassifier()
    result = classifier.classify("今天天气怎么样")
    assert result.primary_domain == Domain.UNKNOWN
    assert result.intent_type == IntentType.SINGLE_DOMAIN
    assert not result.requires_collaboration


def test_find_keywords_investment():
    """Test finding investment keywords."""
    classifier = IntentClassifier()
    keywords = classifier._find_keywords("查询茅台持仓和盈亏")
    assert any("investment" in kw for kw in keywords)


def test_find_keywords_customer():
    """Test finding customer keywords."""
    classifier = IntentClassifier()
    keywords = classifier._find_keywords("查询VIP高净值客户")
    assert any("customer" in kw for kw in keywords)


def test_find_keywords_insurance():
    """Test finding insurance keywords."""
    classifier = IntentClassifier()
    keywords = classifier._find_keywords("保单贷款条款")
    assert any("insurance" in kw for kw in keywords)


def test_classification_result_model():
    """Test ClassificationResult model."""
    result = ClassificationResult(
        intent_type=IntentType.CROSS_DOMAIN,
        primary_domain=Domain.CUSTOMER,
        involved_domains=[Domain.CUSTOMER, Domain.INVESTMENT],
        query_summary="测试查询",
        requires_collaboration=True
    )
    assert result.intent_type == IntentType.CROSS_DOMAIN
    assert result.requires_collaboration is True