"""
fusion.py
---------
KG + RAG Context Fusion Pipeline.

Flow:
  User Query
    → Extract synthetic entity mentions
    → Retrieve KG facts for those entities
    → Retrieve top-k documents via RAG
    → Merge into a single context string
"""

import re
from kg_builder import get_kg_context_for_entities, KG
from rag_engine import get_docs_text

# ─────────────────────────────────────────────
# Synthetic Entity Patterns (corrected to match actual entity names)
# ─────────────────────────────────────────────
ENTITY_PATTERNS = [
    r"\bFirm_[A-Z]\b",
    r"\b[A-Z][a-zA-Z]*_[A-Z]_Y\d\b",  # Revenue_A_Y1, Profit_B_Y1, etc.
    r"\b[A-Z][a-zA-Z]*_[A-Z]\b",      # PE_Ratio_A, GrowthRate_B, etc.
    r"\bBond_[A-Z]\b",                # Bond_A, Bond_B, etc.
    r"\bEquity_[A-Z]\b",              # Equity_A, Equity_B, etc.
]

_COMBINED_PATTERN = re.compile("|".join(ENTITY_PATTERNS), re.IGNORECASE)

# Canonical casing map (for case-insensitive matching)
_CANONICAL = {
    "firm_a": "Firm_A", "firm_b": "Firm_B", "firm_c": "Firm_C",
    "firm_d": "Firm_D", "firm_e": "Firm_E", "firm_f": "Firm_F",
    "firm_g": "Firm_G", "firm_h": "Firm_H", "firm_i": "Firm_I", "firm_j": "Firm_J",
}


def extract_entities(query: str) -> list[str]:
    """
    Extract synthetic entity names from user query using regex patterns and semantic matching.
    Also attempts to resolve natural language metric names to KG entity names.
    Returns list of canonical entity names found in the KG.
    """
    found_entities = set()
    query_lower = query.lower()
    
    # Step 1: Regex extraction - find explicitly mentioned entities
    explicit_matches = _COMBINED_PATTERN.findall(query)
    for match in explicit_matches:
        key = match.lower()
        canonical = _CANONICAL.get(key, match)
        if canonical in KG:
            found_entities.add(canonical)
    
    # Step 2: Extract firm references from natural language
    firms_mentioned = []
    firm_refs = re.findall(r'\bfirm\s+([a-z])\b|\bfirm_?([a-z])\b', query_lower)
    for match in firm_refs:
        firm_letter = match[0] if match[0] else match[1]
        firm_name = f"Firm_{firm_letter.upper()}"
        if firm_name in KG:
            found_entities.add(firm_name)
            firms_mentioned.append(firm_name)
    
    # Step 3: If asking about "all" firms or general metrics, include ALL firms
    # (e.g., "Show me all revenues", "What are profits", "Compare revenues")
    query_wants_all = any(kw in query_lower for kw in ['all', 'show', 'list', 'every', 'each', 'compare'])
    if query_wants_all:
        # This is a bulk query - add ALL firms
        for node in KG.nodes():
            if node.startswith('Firm_'):
                if node not in firms_mentioned:
                    firms_mentioned.append(node)
                found_entities.add(node)
    
    # Step 4: Match query keywords to metric types
    metric_keywords = {
        'revenue|sales|income|income': ['Revenue_'],
        'profit|earnings|net income|net profit': ['Profit_'],
        'asset|assets': ['Assets_'],
        'liability|liabilities|debt': ['Liabilities_'],
        'growth|increase|grew|growth rate': ['GrowthRate_'],
        'employee|employees|headcount|staff': ['EmployeeCount_'],
        'pe ratio|price.?earnings|pe': ['PE_Ratio_'],
        'roe|return.*equity': ['ROE_'],
        'roa|return.*asset': ['ROA_'],
        'margin|profitability': ['ProfitMargin_', 'GrossMargin_', 'EBITDAMargin_'],
        'liquidity|quick ratio|current ratio': ['QuickRatio_'],
        'cash flow|operating cash|cashflow': ['OperatingCashFlow_'],
        'ebitda': ['EBITDA_'],
        'equity|stock': ['Equity_'],
        'bond': ['Bond_'],
        'acquire|acquisition|acquired|merger|subsidiary': ['Firm_'],
    }
    
    # Match keywords in query and find corresponding entities
    matched_keywords = False
    for keyword_pattern, entity_prefixes in metric_keywords.items():
        if re.search(keyword_pattern, query_lower):
            matched_keywords = True
            
            # Strategy 1: If we have specific firms, find their metrics
            if firms_mentioned:
                for firm in firms_mentioned:
                    firm_letter = firm.split("_")[1]
                    for entity_prefix in entity_prefixes:
                        # Find all entities that match this prefix and firm letter combo
                        for node in KG.nodes():
                            if node.startswith(entity_prefix) and firm_letter in node:
                                found_entities.add(node)
            
            # Strategy 2: Also look for ANY metric that matches the pattern
            # (helps with "what is revenue" without specifying firm)
            for entity_prefix in entity_prefixes:
                for node in KG.nodes():
                    if node.startswith(entity_prefix):
                        # Only add if it ends with a year or firm letter (not intermediate nodes)
                        if re.search(r'_[A-J](_Y\d)?$', node):
                            found_entities.add(node)
    
    # Step 5: Add entities explicitly mentioned in the query string
    for node in KG.nodes():
        if node.lower() in query_lower or node in query:
            found_entities.add(node)
    
    return list(found_entities)


def build_merged_context(query: str, top_k: int = 3) -> dict:
    """
    Full fusion pipeline:
      1. Extract entity mentions from query
      2. NO automatic expansion (keep context focused)
      3. Fetch KG facts for those entities
      4. Fetch top-k relevant documents via RAG
      5. Merge into unified context

    Returns:
        {
          "kg_context": str,
          "doc_context": str,
          "merged_context": str,
          "entities_found": [str],
        }
    """
    entities = extract_entities(query)
    
    # IMPROVED: Do NOT auto-expand unless explicitly asked about relationships
    expanded_entities = set(entities)
    
    # Only expand to neighbors IF query explicitly asks about relationships
    query_lower = query.lower()
    is_relationship_query = bool(re.search(r'\b(acquired|merger|partnership|related|connect|depend|affect|impact|relationship|relationship|whose|who)\b', query_lower))
    
    if is_relationship_query and entities:
        # For relationship queries, add only direct neighbors
        for entity in entities:
            if entity in KG:
                successors = list(KG.successors(entity))
                # Only add metrics/measurements, not other firms
                for succ in successors:
                    if '_' in succ and not succ.startswith('Firm_'):
                        expanded_entities.add(succ)
                
                # Add some predecessors if they're not firms
                predecessors = list(KG.predecessors(entity))
                for pred in predecessors:
                    if not pred.startswith('Firm_'):
                        expanded_entities.add(pred)
    
    # Step 1: KG facts (use expanded entities with prioritization)
    kg_ctx = get_kg_context_for_entities(list(expanded_entities), priority_entities=entities) if expanded_entities else ""
    
    # Step 2: RAG documents (use original query)
    doc_ctx = get_docs_text(query, k=top_k)
    
    # Step 3: Merge with KG FACTS FIRST (prioritized)
    parts = []
    if kg_ctx:
        parts.append("PRIMARY SOURCE: KNOWLEDGE GRAPH FACTS\n" + kg_ctx)
    if doc_ctx:
        parts.append("\nSUPPLEMENTARY CONTEXT: RETRIEVED DOCUMENTS\n" + doc_ctx)
    
    merged = "\n\n".join(parts) if parts else ""
    
    return {
        "kg_context": kg_ctx,
        "doc_context": doc_ctx,
        "merged_context": merged,
        "entities_found": list(entities),
    }
