"""
subgraph_extractor.py
--------------------
Extracts query-specific subgraphs:
- FINANCIAL: Only firm → financial metrics relationships
- NETWORK: Only firm-to-firm relationships

Keeps graphs clean and focused.
"""

import networkx as nx
from kg_builder import KG, get_entity_facts, get_relationships


# ─────────────────────────────────────────────
# Financial Subgraph
# ─────────────────────────────────────────────

def get_financial_subgraph(entities: list[str]) -> nx.DiGraph:
    """
    Extract financial subgraph containing only:
    - Query-mentioned entities
    - Their financial metrics (value-bearing nodes)
    
    Excludes:
    - Other firms
    - Network relationships
    """
    sub_graph = nx.DiGraph()
    
    # Financial metric prefixes
    financial_prefixes = [
        'Revenue_', 'Profit_', 'Assets_', 'Liabilities_',
        'PE_Ratio_', 'ROE_', 'ROA_', 'GrowthRate_',
        'Margin', 'Cash', 'Equity_', 'Bond_',
        'EBITDA_', 'QuickRatio_', 'EmployeeCount_'
    ]
    
    for entity in entities:
        if entity not in KG:
            continue
        
        facts = get_entity_facts(entity)
        sub_graph.add_node(entity,
                          entity_type=facts.get("entity_type", "Unknown"),
                          description=facts.get("description", ""),
                          value=facts.get("value"),
                          unit=facts.get("unit"),
                          year=facts.get("year"),
        )
        
        # Add only financial metric relationships
        for rel in get_relationships(entity):
            target = rel["object"]
            
            # Include if target is a financial metric
            is_financial = any(target.startswith(p) for p in financial_prefixes)
            is_value_bearing = get_entity_facts(target).get("value") is not None
            
            if is_financial or is_value_bearing:
                target_facts = get_entity_facts(target)
                sub_graph.add_node(target,
                                  entity_type=target_facts.get("entity_type", "Unknown"),
                                  description=target_facts.get("description", ""),
                                  value=target_facts.get("value"),
                                  unit=target_facts.get("unit"),
                                  year=target_facts.get("year"),
                )
                sub_graph.add_edge(entity, target, relation=rel["relation"])
    
    return sub_graph


# ─────────────────────────────────────────────
# Network Subgraph
# ─────────────────────────────────────────────

def get_network_subgraph(entities: list[str]) -> nx.DiGraph:
    """
    Extract network subgraph containing only:
    - Query-mentioned entities
    - Firm-to-firm relationships
    
    Excludes:
    - Financial metrics
    """
    sub_graph = nx.DiGraph()
    
    # Network relationship types
    network_relations = [
        'acquired', 'acquired_by', 'partnership', 'supplies',
        'supply_chain', 'joint_venture', 'reseller', 'supplier',
        'technology_license', 'distribution_agreement', 'consortium'
    ]
    
    for entity in entities:
        if entity not in KG:
            continue
        
        facts = get_entity_facts(entity)
        sub_graph.add_node(entity,
                          entity_type=facts.get("entity_type", "Unknown"),
                          description=facts.get("description", ""),
                          value=facts.get("value"),
                          unit=facts.get("unit"),
                          year=facts.get("year"),
        )
        
        # Add only network relationships
        for rel in get_relationships(entity):
            relation_type = rel["relation"]
            target = rel["object"]
            
            # Include if relationship is network-type
            if relation_type in network_relations:
                target_facts = get_entity_facts(target)
                sub_graph.add_node(target,
                                  entity_type=target_facts.get("entity_type", "Unknown"),
                                  description=target_facts.get("description", ""),
                                  value=target_facts.get("value"),
                                  unit=target_facts.get("unit"),
                                  year=target_facts.get("year"),
                )
                sub_graph.add_edge(entity, target, relation=relation_type)
    
    return sub_graph


# ─────────────────────────────────────────────
# Subgraph Serialization
# ─────────────────────────────────────────────

def serialize_subgraph_for_d3(subgraph: nx.DiGraph) -> dict:
    """Convert NetworkX subgraph to D3-ready format."""
    nodes = []
    for node, attrs in subgraph.nodes(data=True):
        nodes.append({
            "id": node,
            "entity_type": attrs.get("entity_type", "Unknown"),
            "value": attrs.get("value"),
            "unit": attrs.get("unit"),
            "year": attrs.get("year"),
            "description": attrs.get("description", ""),
        })
    
    links = []
    for src, dst, attrs in subgraph.edges(data=True):
        links.append({
            "source": src,
            "target": dst,
            "relation": attrs.get("relation", ""),
        })
    
    return {"nodes": nodes, "links": links}


def get_context_for_subgraph(subgraph: nx.DiGraph) -> str:
    """Generate human-readable context from subgraph."""
    lines = []
    
    for node in subgraph.nodes():
        attrs = subgraph.nodes[node]
        entity_type = attrs.get("entity_type", "Unknown")
        description = attrs.get("description", "")
        value = attrs.get("value")
        unit = attrs.get("unit", "")
        
        lines.append(f"[{entity_type}] {node}: {description}")
        if value is not None:
            lines.append(f"  VALUE: {value} {unit}")
        
        # Add outgoing edges
        for successor in subgraph.successors(node):
            edge_data = subgraph.edges[node, successor]
            relation = edge_data.get("relation", "unknown")
            succ_attrs = subgraph.nodes[successor]
            succ_value = succ_attrs.get("value")
            succ_unit = succ_attrs.get("unit", "")
            
            lines.append(f"  → {node} --[{relation}]--> {successor}")
            if succ_value is not None:
                lines.append(f"     └─ VALUE: {succ_value} {succ_unit}")
    
    return "\n".join(lines)
