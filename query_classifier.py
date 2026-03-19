"""
query_classifier.py
-------------------
Classifies user queries into three types:
1. FINANCIAL - asks about firm metrics/ratios
2. NETWORK - asks about relationships between entities
3. AGGREGATION - asks for comparative/aggregate data

Uses rule-based keywords + patterns for deterministic classification.
"""

import re
from enum import Enum


class QueryType(Enum):
    FINANCIAL = "financial"
    NETWORK = "network"
    AGGREGATION = "aggregation"
    IMPACT_ANALYSIS = "impact_analysis"  # Risk propagation, impact chains
    UNKNOWN = "unknown"


# ─────────────────────────────────────────────
# Keyword Definitions
# ─────────────────────────────────────────────

FINANCIAL_KEYWORDS = {
    'revenue', 'sales', 'income', 'profit', 'earnings', 'net profit',
    'asset', 'assets', 'liability', 'liabilities', 'equity',
    'margin', 'margin', 'ratio', 'pe ratio', 'roe', 'roa',
    'ratio', 'cash flow', 'ebitda', 'valuation', 'dividend',
    'liquidity', 'debt', 'growth rate', 'growth', 'performance',
    'financial', 'metric', 'metrics', 'quarterly', 'annual'
}

NETWORK_KEYWORDS = {
    'acquire', 'acquired', 'acquisition', 'acquire', 'acquires',
    'merger', 'merge', 'merged', 'partnership', 'partner',
    'supplier', 'supply', 'supply chain', 'dependent', 'depends',
    'relationship', 'related', 'connected', 'connection', 'connect',
    'consortium', 'joint venture', 'collaborate', 'collaboration',
    'subsidiary', 'subsidiaries', 'affiliate', 'affiliation',
    'license', 'reseller', 'distribution', 'agreement'
}

AGGREGATION_KEYWORDS = {
    'all', 'list', 'show all', 'every', 'each', 'compare',
    'highest', 'lowest', 'max', 'min', 'average', 'total',
    'sum', 'count', 'how many', 'which', 'top', 'bottom',
    'ranking', 'rank', 'sorted', 'order', 'across', 'between'
}

IMPACT_ANALYSIS_KEYWORDS = {
    'risk', 'affected', 'impact', 'affect', 'propagate', 'effect',
    'consequence', 'consequence', 'cascade', 'ripple', 'vulnerable',
    'if', 'dependent', 'expose', 'exposure', 'contagion'
}

# Query patterns for specific detection
AGGREGATION_PATTERNS = [
    r'show\s+all\s+\w+',          # "show all firms"
    r'list\s+\w+',                 # "list firms"
    r'compare\s+\w+',              # "compare firms"
    r'top\s+\d+\s+\w+',           # "top 5 firms"
    r'which\s+\w+\s+has\s+(highest|lowest|most|least)',  # "which firm has highest"
    r'\b(all|every)\s+\w+\'?s?\s+\w+',  # "all firms' revenue"
]

NETWORK_PATTERNS = [
    r'who\s+(acquired|acquired|supplies|partners)',
    r'does\s+\w+\s+(acquire|supply|partner)',
    r'relationship\s+between',
    r'connected\s+to',
    r'depend.*on',
]

FINANCIAL_PATTERNS = [
    r'what\s+is\s+\w+\'?s?\s+(revenue|profit|margin|assets)',
    r'how\s+much\s+\w+',
    r'\w+\'?s?\s+(revenue|profit|margin)',
]

IMPACT_ANALYSIS_PATTERNS = [
    r'if\s+\w+\s+is\s+.*risk.*which.*affected',  # "if Firm X at risk which affected"
    r'which\s+firms?\s+affected.*\w+',            # "which firms affected by..."
    r'impact\s+on.*firms?',                       # "impact on firms"
    r'\w+\s+risk.*propagat',                      # "propagation of risk"
    r'cascade.*effect',                           # "cascade effects"
    r'depend.*exposure',                          # "dependency exposure"
]


# ─────────────────────────────────────────────
# Query Classification
# ─────────────────────────────────────────────

def classify_query(query: str) -> QueryType:
    """
    Deterministically classify query into one of four types.
    
    Priority:
    1. Check impact analysis patterns (highest priority - most specific)
    2. Check aggregation patterns
    3. Check network patterns
    4. Check financial patterns
    5. Count keyword occurrences as fallback
    """
    query_lower = query.lower()
    
    # Check impact analysis patterns first (highest priority)
    for pattern in IMPACT_ANALYSIS_PATTERNS:
        if re.search(pattern, query_lower):
            return QueryType.IMPACT_ANALYSIS
    
    # Check if query has both risk/impact keywords + firm reference
    has_impact_kw = any(kw in query_lower for kw in IMPACT_ANALYSIS_KEYWORDS)
    has_firm_ref = bool(re.search(r'firm\s+[a-z]', query_lower))
    if has_impact_kw and has_firm_ref:
        return QueryType.IMPACT_ANALYSIS
    
    # Check aggregation patterns
    for pattern in AGGREGATION_PATTERNS:
        if re.search(pattern, query_lower):
            return QueryType.AGGREGATION
    
    # Check network patterns
    for pattern in NETWORK_PATTERNS:
        if re.search(pattern, query_lower):
            return QueryType.NETWORK
    
    # Check financial patterns
    for pattern in FINANCIAL_PATTERNS:
        if re.search(pattern, query_lower):
            return QueryType.FINANCIAL
    
    # Count keyword occurrences
    imp_count = sum(1 for kw in IMPACT_ANALYSIS_KEYWORDS if kw in query_lower)
    agg_count = sum(1 for kw in AGGREGATION_KEYWORDS if kw in query_lower)
    net_count = sum(1 for kw in NETWORK_KEYWORDS if kw in query_lower)
    fin_count = sum(1 for kw in FINANCIAL_KEYWORDS if kw in query_lower)
    
    # Return type with highest keyword count
    if imp_count > 0 and imp_count > agg_count and imp_count > net_count and imp_count > fin_count:
        return QueryType.IMPACT_ANALYSIS
    elif agg_count > 0 and agg_count >= net_count and agg_count >= fin_count:
        return QueryType.AGGREGATION
    elif net_count > 0 and net_count >= fin_count:
        return QueryType.NETWORK
    elif fin_count > 0:
        return QueryType.FINANCIAL
    
    # Default
    return QueryType.FINANCIAL


def is_aggregation_query(query: str) -> bool:
    """Quick check if query is aggregation type."""
    return classify_query(query) == QueryType.AGGREGATION


def is_network_query(query: str) -> bool:
    """Quick check if query is network type."""
    return classify_query(query) == QueryType.NETWORK


def is_financial_query(query: str) -> bool:
    """Quick check if query is financial type."""
    return classify_query(query) == QueryType.FINANCIAL


def is_impact_analysis_query(query: str) -> bool:
    """Quick check if query is impact analysis type."""
    return classify_query(query) == QueryType.IMPACT_ANALYSIS


# Test patterns
if __name__ == "__main__":
    test_queries = [
        "What is Firm A's revenue?",
        "Show all firms",
        "Which firm has highest profit?",
        "Who did Firm A acquire?",
        "Compare revenues across firms",
        "What are the profits?",
        "List all firms and their revenue",
        "Who supplies to Firm D?",
    ]
    
    for q in test_queries:
        qtype = classify_query(q)
        print(f"{q:45} → {qtype.value}")
