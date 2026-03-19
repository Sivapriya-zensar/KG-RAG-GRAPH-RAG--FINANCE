"""
impact_analysis.py
------------------
Handles impact/risk propagation queries.

Examples:
- "If Firm D is at financial risk, which firms are affected?"
- "What's the impact of Firm A's acquisition on supply chain?"
- "Cascade effects of Firm B default"

Flow:
1. Extract source firm from query
2. Assess financial health (risky metrics)
3. Find all connected firms
4. Determine impact type (supplier risk, acquisition risk, etc.)
5. Return combined graph + analysis
"""

import re
from kg_builder import KG, get_entity_facts, get_relationships
from synthetic_data import ENTITY_ATTRIBUTES, TRIPLES


# ─────────────────────────────────────────────
# Risk Assessment
# ─────────────────────────────────────────────

RISK_INDICATORS = {
    'high_debt': ['Liabilities', 'leverage', 'debt_to_equity'],
    'low_liquidity': ['QuickRatio', 'current_ratio', 'liquidity'],
    'declining_revenue': ['Revenue', 'sales_decline'],
    'low_profitability': ['Profit', 'margin'],
    'high_pe_ratio': ['PE_Ratio'],
}


def assess_financial_risk(firm: str) -> dict:
    """
    Assess financial risk level of a firm.
    
    Returns:
        {
            "risk_level": "high" | "medium" | "low",
            "risk_factors": [list of risky metrics],
            "metrics": {metric_name: value}
        }
    """
    firm_letter = firm.split("_")[1]
    risk_factors = []
    metrics = {}
    
    # Scan for risky metrics
    for entity in ENTITY_ATTRIBUTES:
        if firm_letter not in entity:
            continue
        
        attrs = ENTITY_ATTRIBUTES[entity]
        value = attrs.get("value")
        
        if value is None:
            continue
        
        # Check for high debt/liabilities
        if "Liabilities" in entity and value > 100:
            risk_factors.append(f"High liabilities: {value}M")
            metrics[entity] = value
        
        # Check for low profit margin
        if "Margin" in entity and value < 15:
            risk_factors.append(f"Low profit margin: {value}%")
            metrics[entity] = value
        
        # Check for low profitability
        if "Profit" in entity and value < 10:
            risk_factors.append(f"Low profit: {value}M")
            metrics[entity] = value
        
        # Check for very high PE ratio
        if "PE_Ratio" in entity and value > 25:
            risk_factors.append(f"High PE ratio: {value}x")
            metrics[entity] = value
    
    # Determine risk level
    if len(risk_factors) >= 2:
        risk_level = "high"
    elif len(risk_factors) == 1:
        risk_level = "medium"
    else:
        risk_level = "low"
    
    return {
        "risk_level": risk_level,
        "risk_factors": risk_factors,
        "metrics": metrics,
    }


# ─────────────────────────────────────────────
# Impact/Dependency Analysis
# ─────────────────────────────────────────────

def find_affected_firms(source_firm: str) -> dict:
    """
    Find firms affected by source firm's risk.
    
    Returns:
        {
            "affected_firms": [list of firm names],
            "impact_type": "supplier" | "customer" | "partner" | "acquisition",
            "impact_paths": [chain of dependencies]
        }
    """
    affected = []
    impact_paths = []
    impact_types = set()
    
    # Find all relationships from source firm
    for (subj, pred, obj) in TRIPLES:
        if subj == source_firm:
            # This firm affects something
            if obj.startswith("Firm_"):
                affected.append(obj)
                
                # Categorize impact type
                if "supply" in pred.lower():
                    impact_types.add("supplier")
                elif "acquire" in pred.lower() or "acquired" in pred.lower():
                    impact_types.add("acquisition")
                elif "partner" in pred.lower():
                    impact_types.add("partnership")
                elif "distribute" in pred.lower():
                    impact_types.add("distribution")
                
                impact_paths.append({
                    "from": source_firm,
                    "relationship": pred,
                    "to": obj,
                })
        
        # Also find firms that depend ON source firm
        elif obj == source_firm:
            if subj.startswith("Firm_"):
                affected.append(subj)
                
                # Categorize impact type
                if "supply" in pred.lower():
                    impact_types.add("dependent_supplier")
                elif "partner" in pred.lower():
                    impact_types.add("partnership")
                
                impact_paths.append({
                    "from": subj,
                    "relationship": pred,
                    "to": source_firm,
                })
    
    return {
        "affected_firms": list(set(affected)),
        "impact_types": list(impact_types),
        "impact_paths": impact_paths,
    }


# ─────────────────────────────────────────────
# Risk Propagation Graph Builder
# ─────────────────────────────────────────────

def build_impact_graph(query: str, source_firm: str) -> dict:
    """
    Build a knowledge graph showing risk propagation.
    
    Includes:
    - Source firm with risk indicators
    - Affected firms
    - Relationship paths
    - Impact chains
    """
    import networkx as nx
    
    impact_kg = nx.DiGraph()
    
    # 1. Add source firm with risk assessment
    risk_assessment = assess_financial_risk(source_firm)
    facts = get_entity_facts(source_firm)
    
    impact_kg.add_node(
        source_firm,
        entity_type="Firm",
        description=facts.get("description", ""),
        risk_level=risk_assessment["risk_level"],
        risk_factors=risk_assessment["risk_factors"],
        value=None,
        unit=None,
        year=None,
    )
    
    # 2. Add risk factor nodes
    for risk_factor in risk_assessment["risk_factors"]:
        risk_node_id = f"RISK_{len(impact_kg.nodes())}"
        impact_kg.add_node(
            risk_node_id,
            entity_type="Risk",
            description=risk_factor,
            value=None,
            unit=None,
            year=None,
        )
        impact_kg.add_edge(source_firm, risk_node_id, relation="has_risk")
    
    # 3. Find and add affected firms
    impact_data = find_affected_firms(source_firm)
    for affected_firm in impact_data["affected_firms"]:
        if affected_firm in KG:
            aff_facts = get_entity_facts(affected_firm)
            impact_kg.add_node(
                affected_firm,
                entity_type="Firm",
                description=aff_facts.get("description", ""),
                value=None,
                unit=None,
                year=None,
            )
    
    # 4. Add relationship edges
    for path in impact_data["impact_paths"]:
        if path["from"] in impact_kg and path["to"] in impact_kg:
            impact_kg.add_edge(path["from"], path["to"], relation=path["relationship"])
    
    # 5. Serialization for D3
    nodes = []
    for node, attrs in impact_kg.nodes(data=True):
        nodes.append({
            "id": node,
            "entity_type": attrs.get("entity_type", "Unknown"),
            "value": attrs.get("value"),
            "unit": attrs.get("unit"),
            "year": attrs.get("year"),
            "description": attrs.get("description", ""),
            "risk_level": attrs.get("risk_level"),
            "risk_factors": attrs.get("risk_factors", []),
        })
    
    links = []
    for src, dst, attrs in impact_kg.edges(data=True):
        links.append({
            "source": src,
            "target": dst,
            "relation": attrs.get("relation", ""),
        })
    
    return {
        "nodes": nodes,
        "links": links,
        "risk_assessment": risk_assessment,
        "impact_data": impact_data,
    }


def extract_source_firm(query: str) -> str:
    """Extract firm name from impact query."""
    match = re.search(r'\bfirm\s+([a-z])\b|\bfirm_?([a-z])\b', query.lower())
    if match:
        firm_letter = (match.group(1) or match.group(2)).upper()
        return f"Firm_{firm_letter}"
    return None


def generate_impact_analysis(query: str, source_firm: str) -> str:
    """
    Generate human-readable impact analysis.
    
    Returns:
        Analysis text describing risk propagation
    """
    risk = assess_financial_risk(source_firm)
    impact = find_affected_firms(source_firm)
    
    lines = []
    lines.append(f"IMPACT ANALYSIS: {source_firm}\n")
    
    # Risk summary
    lines.append(f"Financial Risk Level: {risk['risk_level'].upper()}")
    if risk['risk_factors']:
        lines.append("Risk Factors:")
        for factor in risk['risk_factors']:
            lines.append(f"  • {factor}")
    
    # Impact summary
    if impact['affected_firms']:
        lines.append(f"\nAffected Firms ({len(impact['affected_firms'])}):")
        for firm in impact['affected_firms']:
            lines.append(f"  • {firm}")
        
        lines.append(f"\nImpact Types: {', '.join(impact['impact_types'])}")
        
        lines.append("\nImpact Paths:")
        for path in impact['impact_paths']:
            lines.append(f"  {path['from']} --[{path['relationship']}]--> {path['to']}")
    else:
        lines.append("\nNo direct firm dependencies detected.")
    
    return "\n".join(lines)
