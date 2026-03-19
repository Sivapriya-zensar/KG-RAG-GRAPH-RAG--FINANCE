"""
app.py
------
Flask backend for the Synthetic Finance KG-RAG system.

Endpoints:
  POST /query  — run KG+RAG pipeline and return LLM answer
  GET  /graph  — return D3-ready KG JSON
  GET  /       — serve frontend index.html
"""

import os
import sys
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Ensure backend directory is on the path
sys.path.insert(0, os.path.dirname(__file__))

from kg_builder import serialize_graph_for_d3
from fusion import build_merged_context
from llm_handler import generate_answer
from query_classifier import classify_query, QueryType
from impact_analysis import build_impact_graph, extract_source_firm, generate_impact_analysis
from aggregation_handler import handle_aggregation_query
from query_classifier import classify_query, QueryType
from aggregation_handler import build_aggregation_response
from subgraph_extractor import (
    get_financial_subgraph, 
    get_network_subgraph, 
    serialize_subgraph_for_d3,
    get_context_for_subgraph
)

# ─────────────────────────────────────────────
# App Setup
# ─────────────────────────────────────────────
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")

app = Flask(__name__, static_folder=FRONTEND_DIR)
CORS(app)  # Allow cross-origin requests during development


# ─────────────────────────────────────────────
# Query-Specific KG Builder
# ─────────────────────────────────────────────

def build_query_specific_kg(query: str, entities_found: list, answer: str) -> dict:
    """
    Build a minimal, focused Knowledge Graph specific to the query and its answer.
    Shows ONLY the path from query → entity → answer (no extra nodes).
    
    Example:
      Query: "What is Firm_A's revenue?"
      Returns KG with nodes: [Query, Firm_A, Revenue_A_Y1] 
      Links: Query→Firm_A, Firm_A→Revenue_A_Y1
    """
    import networkx as nx
    from kg_builder import KG, get_entity_facts, get_relationships
    
    query_kg = nx.DiGraph()
    
    # Add query node only
    query_kg.add_node("USER_QUERY", 
                      entity_type="Query", 
                      description=query,
                      value=None,
                      unit=None,
                      year=None,
    )
    
    # Find the most relevant entity to show as answer
    answer_entity = None
    best_score = 0
    
    # Only add entities that were actually found (primary entities)
    # Do NOT expand to neighbors - keep graph minimal and focused
    for entity in entities_found:
        if entity not in KG:
            continue
            
        facts = get_entity_facts(entity)
        
        # Add this entity to the graph
        query_kg.add_node(entity, 
                        entity_type=facts.get("entity_type", "Unknown"),
                        description=facts.get("description", ""),
                        value=facts.get("value"),
                        unit=facts.get("unit"),
                        year=facts.get("year"),
        )
        
        # Link query to entity
        query_kg.add_edge("USER_QUERY", entity, relation="queries")
        
        # Track which entity is most likely the answer (has a value)
        if facts.get("value") is not None:
            score = 1
            # Boost score if entity is a metric type
            if facts.get("entity_type") == "Metric":
                score += 10
            # Boost if entity name appears in the answer
            if entity.lower() in answer.lower():
                score += 5
            
            if score > best_score:
                best_score = score
                answer_entity = entity
    
    # Add single best answer entity if found
    if answer_entity and best_score > 0:
        query_kg.add_edge("USER_QUERY", answer_entity, relation="answered_by")
    
    # Serialize for D3 (exclude USER_QUERY node for clean visualization)
    nodes = []
    for node, attrs in query_kg.nodes(data=True):
        # Skip the query node - only show entities and answers
        if node == "USER_QUERY":
            continue
        nodes.append({
            "id": node,
            "entity_type": attrs.get("entity_type", "Unknown"),
            "value": attrs.get("value"),
            "unit": attrs.get("unit"),
            "year": attrs.get("year"),
            "description": attrs.get("description", ""),
        })
    
    links = []
    for src, dst, attrs in query_kg.edges(data=True):
        # Skip links from USER_QUERY node
        if src == "USER_QUERY":
            continue
        links.append({
            "source": src,
            "target": dst,
            "relation": attrs.get("relation", ""),
        })
    
    return {"nodes": nodes, "links": links}

# ─────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────

@app.route("/")
def index():
    """Serve the D3.js frontend."""
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/graph", methods=["GET"])
def get_graph():
    """
    Return the Knowledge Graph serialized for D3.js.

    Response:
        {
          "nodes": [{id, entity_type, value, unit, year, description}, ...],
          "links": [{source, target, relation}, ...]
        }
    """
    graph_data = serialize_graph_for_d3()
    return jsonify(graph_data)


@app.route("/query", methods=["POST"])
def query():
    """
    Accept a user query and route it based on query type.
    
    Query Types:
    1. FINANCIAL - financial metrics queries → KG+RAG+LLM
    2. NETWORK - relationship queries → Network subgraph
    3. AGGREGATION - aggregate queries → Structured data
    4. IMPACT_ANALYSIS - risk propagation → Impact graph
    
    Request body (JSON):
        { "query": "..." }
    
    Response varies by query type.
    """
    body = request.get_json(force=True, silent=True) or {}
    user_query = body.get("query", "").strip()

    if not user_query:
        return jsonify({"error": "Missing 'query' field in request body."}), 400

    # Classify query type
    query_type = classify_query(user_query)
    
    # ─────────────────────────────────────────────
    # IMPACT ANALYSIS QUERIES
    # ─────────────────────────────────────────────
    if query_type == QueryType.IMPACT_ANALYSIS:
        source_firm = extract_source_firm(user_query)
        if not source_firm:
            return jsonify({"error": "Could not identify firm in impact query."}), 400
        
        # Build impact graph
        impact_graph = build_impact_graph(user_query, source_firm)
        impact_text = generate_impact_analysis(user_query, source_firm)
        
        return jsonify({
            "query_type": "impact_analysis",
            "answer": impact_text,
            "entities_found": [source_firm],
            "query_kg": impact_graph,
            "risk_assessment": impact_graph.get("risk_assessment", {}),
            "impact_data": impact_graph.get("impact_data", {}),
        })
    
    # ─────────────────────────────────────────────
    # AGGREGATION QUERIES
    # ─────────────────────────────────────────────
    elif query_type == QueryType.AGGREGATION:
        agg_result = handle_aggregation_query(user_query)
        
        return jsonify({
            "query_type": "aggregation",
            "answer": agg_result.get("answer", ""),
            "data": agg_result.get("data", []),
            "metadata": agg_result.get("metadata", {}),
            "query_kg": None,  # No graph for aggregation
        })
    
    # ─────────────────────────────────────────────
    # FINANCIAL & NETWORK QUERIES (standard pipeline)
    # ─────────────────────────────────────────────
    else:
        # Fusion pipeline
        fusion_result = build_merged_context(user_query, top_k=3)

        # LLM answer generation
        answer = generate_answer(user_query, fusion_result["merged_context"])

        # Build query-specific KG
        query_kg = build_query_specific_kg(user_query, fusion_result["entities_found"], answer)

        return jsonify({
            "query_type": query_type.value,
            "answer": answer,
            "entities_found": fusion_result["entities_found"],
            "kg_context": fusion_result["kg_context"],
            "doc_context": fusion_result["doc_context"],
            "query_kg": query_kg,
        })


# ─────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 55)
    print("  Synthetic Finance KG-RAG System")
    print("  Backend: http://localhost:5000")
    print("=" * 55)
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
