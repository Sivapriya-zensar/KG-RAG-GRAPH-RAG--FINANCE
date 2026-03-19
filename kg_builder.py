"""
kg_builder.py
-------------
Builds and queries the synthetic Finance Knowledge Graph using NetworkX.
"""

import networkx as nx
from synthetic_data import TRIPLES, ENTITY_ATTRIBUTES


def build_kg() -> nx.DiGraph:
    """
    Construct a directed knowledge graph from synthetic triples.
    Each node is annotated with its entity attributes.
    Each edge carries a 'relation' attribute.
    """
    G = nx.DiGraph()

    # Add nodes with attributes
    for entity, attrs in ENTITY_ATTRIBUTES.items():
        G.add_node(entity, **attrs)

    # Add edges from triples
    for (subj, pred, obj) in TRIPLES:
        # Ensure both endpoints exist as nodes even if not in ENTITY_ATTRIBUTES
        if subj not in G:
            G.add_node(subj, entity_type="Unknown")
        if obj not in G:
            G.add_node(obj, entity_type="Unknown")
        G.add_edge(subj, obj, relation=pred)

    return G


# Singleton KG instance
KG = build_kg()


# ─────────────────────────────────────────────
# Query Functions
# ─────────────────────────────────────────────

def get_entity_facts(entity: str) -> dict:
    """
    Return all attributes of a given entity node.
    Returns empty dict if entity is not in the graph.
    """
    if entity not in KG:
        return {}
    attrs = dict(KG.nodes[entity])
    attrs["entity"] = entity
    return attrs


def get_neighbors(entity: str) -> list[str]:
    """
    Return all directly connected entities (successors + predecessors).
    """
    if entity not in KG:
        return []
    successors = list(KG.successors(entity))
    predecessors = list(KG.predecessors(entity))
    return list(set(successors + predecessors))


def get_relationships(entity: str) -> list[dict]:
    """
    Return all typed relationships where *entity* is the subject or object.
    Each item: {subject, relation, object}
    """
    if entity not in KG:
        return []
    rels = []
    # Outgoing edges
    for _, obj, data in KG.out_edges(entity, data=True):
        rels.append({
            "subject": entity,
            "relation": data.get("relation", "unknown"),
            "object": obj,
        })
    # Incoming edges
    for subj, _, data in KG.in_edges(entity, data=True):
        rels.append({
            "subject": subj,
            "relation": data.get("relation", "unknown"),
            "object": entity,
        })
    return rels


def get_kg_context_for_entities(entities: list[str], priority_entities: list[str] = None) -> str:
    """
    Given a list of entity names, build a human-readable KG context string.
    Prioritizes primary queried entities first, then related entities separately.
    
    Args:
        entities: All entities to include in context
        priority_entities: Entities that were directly queried (shown first, clearly marked)
    
    Returns:
        Formatted KG context with prioritized entities clearly separated
    """
    if priority_entities is None:
        priority_entities = []
    
    lines = []
    priority_set = set(priority_entities)
    
    # SECTION 1: Primary entities (those directly queried)
    if priority_entities:
        lines.append("═══ PRIMARY QUERY ENTITIES ═══")
        for entity in priority_entities:
            if entity in entities:
                facts = get_entity_facts(entity)
                rels = get_relationships(entity)

                if facts:
                    desc = facts.get("description", "")
                    val = facts.get("value")
                    unit = facts.get("unit", "")
                    year = facts.get("year", "")
                    lines.append(f"[DIRECT] {entity}: {desc}")
                    if val is not None:
                        lines.append(f"  ✓ VALUE: {val} {unit} (Year {year})")
                else:
                    lines.append(f"[DIRECT] {entity}")

                for rel in rels:
                    lines.append(
                        f"  → {rel['subject']} --[{rel['relation']}]--> {rel['object']}"
                    )
                    # Include value of direct metric relationships only
                    related_facts = get_entity_facts(rel['object'])
                    if related_facts and related_facts.get("value") is not None:
                        rel_val = related_facts.get("value")
                        rel_unit = related_facts.get("unit", "")
                        lines.append(f"     └─ VALUE: {rel_val} {rel_unit}")
    
    # SECTION 2: Related entities (if any exist beyond primary)
    other_entities = [e for e in entities if e not in priority_set]
    if other_entities:
        lines.append("\n═══ RELATED ENTITIES (CONTEXT ONLY) ═══")
        for entity in other_entities:
            facts = get_entity_facts(entity)
            rels = get_relationships(entity)

            if facts:
                desc = facts.get("description", "")
                val = facts.get("value")
                unit = facts.get("unit", "")
                year = facts.get("year", "")
                lines.append(f"[RELATED] {entity}: {desc}")
                if val is not None:
                    lines.append(f"  VALUE: {val} {unit} (Year {year})")

            for rel in rels:
                lines.append(
                    f"  → {rel['subject']} --[{rel['relation']}]--> {rel['object']}"
                )
                # Also include the value of related entity if it exists
                related_facts = get_entity_facts(rel['object'])
                if related_facts and related_facts.get("value") is not None:
                    rel_val = related_facts.get("value")
                    rel_unit = related_facts.get("unit", "")
                    lines.append(f"     └─ VALUE: {rel_val} {rel_unit}")

    return "\n".join(lines) if lines else ""


def serialize_graph_for_d3() -> dict:
    """
    Serialize the KG into a D3-compatible {nodes, links} structure.
    """
    nodes = []
    for node, attrs in KG.nodes(data=True):
        nodes.append({
            "id": node,
            "entity_type": attrs.get("entity_type", "Unknown"),
            "value": attrs.get("value"),
            "unit": attrs.get("unit"),
            "year": attrs.get("year"),
            "description": attrs.get("description", ""),
        })

    links = []
    for src, dst, attrs in KG.edges(data=True):
        links.append({
            "source": src,
            "target": dst,
            "relation": attrs.get("relation", ""),
        })

    return {"nodes": nodes, "links": links}
