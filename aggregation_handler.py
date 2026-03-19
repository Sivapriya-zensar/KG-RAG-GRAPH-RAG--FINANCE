"""
aggregation_handler.py
---------------------
Handles aggregation queries by returning structured data directly.
No RAG, no KG - just data retrieval and computation.

Supports:
- List all firms
- List firms with metrics
- Find highest/lowest values
- Comparisons
- Aggregations (sum, average)
"""

import re
from synthetic_data import ENTITY_ATTRIBUTES, TRIPLES


# ─────────────────────────────────────────────
# Data Extraction
# ─────────────────────────────────────────────

def get_all_firms() -> list[str]:
    """Return list of all firms in the KG."""
    firms = []
    for entity in ENTITY_ATTRIBUTES.keys():
        if entity.startswith("Firm_"):
            firms.append(entity)
    return sorted(firms)


def get_metric_for_firm(firm: str, metric_pattern: str) -> dict:
    """
    Get all metrics matching pattern for a specific firm.
    
    Args:
        firm: "Firm_A", "Firm_B", etc.
        metric_pattern: "Revenue", "Profit", "Assets", etc.
    
    Returns:
        {metric_name: value (with unit)}
    """
    firm_letter = firm.split("_")[1]
    results = {}
    
    for entity, attrs in ENTITY_ATTRIBUTES.items():
        # Match pattern like Revenue_A_Y1
        if metric_pattern in entity and firm_letter in entity:
            value = attrs.get("value")
            unit = attrs.get("unit", "")
            if value is not None:
                results[entity] = {
                    "value": value,
                    "unit": unit,
                    "description": attrs.get("description", "")
                }
    
    return results


def get_all_metrics_of_type(metric_type: str) -> dict:
    """
    Get all metrics of a specific type across all firms.
    
    Args:
        metric_type: "Revenue", "Profit", "Assets", etc.
    
    Returns:
        {firm: {metric_name: {value, unit}}}
    """
    results = {}
    
    for entity, attrs in ENTITY_ATTRIBUTES.items():
        if metric_type in entity and any(f.startswith("Firm_") for f in [e for e, _ in ENTITY_ATTRIBUTES.items()]):
            # Extract firm letter
            match = re.search(r'_([A-J])', entity)
            if match:
                firm_letter = match.group(1)
                firm_name = f"Firm_{firm_letter}"
                
                value = attrs.get("value")
                unit = attrs.get("unit", "")
                
                if value is not None:
                    if firm_name not in results:
                        results[firm_name] = {}
                    results[firm_name][entity] = {
                        "value": value,
                        "unit": unit,
                        "description": attrs.get("description", "")
                    }
    
    return results


def find_highest_metric(metric_type: str) -> dict:
    """
    Find firm with highest value for a metric type.
    
    Returns:
        {firm: value, entity: metric_name, unit: unit}
    """
    highest = None
    highest_firm = None
    highest_entity = None
    highest_unit = None
    
    metrics = get_all_metrics_of_type(metric_type)
    
    for firm, firm_metrics in metrics.items():
        for entity, data in firm_metrics.items():
            value = data.get("value", 0)
            if highest is None or value > highest:
                highest = value
                highest_firm = firm
                highest_entity = entity
                highest_unit = data.get("unit", "")
    
    return {
        "firm": highest_firm,
        "entity": highest_entity,
        "value": highest,
        "unit": highest_unit,
    } if highest_firm else None


def find_lowest_metric(metric_type: str) -> dict:
    """Find firm with lowest value for a metric type."""
    lowest = None
    lowest_firm = None
    lowest_entity = None
    lowest_unit = None
    
    metrics = get_all_metrics_of_type(metric_type)
    
    for firm, firm_metrics in metrics.items():
        for entity, data in firm_metrics.items():
            value = data.get("value", float('inf'))
            if lowest is None or (value < lowest and value > 0):
                lowest = value
                lowest_firm = firm
                lowest_entity = entity
                lowest_unit = data.get("unit", "")
    
    return {
        "firm": lowest_firm,
        "entity": lowest_entity,
        "value": lowest,
        "unit": lowest_unit,
    } if lowest_firm else None


def compute_average_metric(metric_type: str) -> dict:
    """Compute average value for a metric across all firms."""
    metrics = get_all_metrics_of_type(metric_type)
    
    values = []
    for firm, firm_metrics in metrics.items():
        for entity, data in firm_metrics.items():
            value = data.get("value")
            if value is not None:
                values.append(value)
    
    if not values:
        return None
    
    average = sum(values) / len(values)
    unit = list(metrics.values())[0]
    unit = list(unit.values())[0].get("unit", "") if metrics else ""
    
    return {
        "metric_type": metric_type,
        "average": average,
        "unit": unit,
        "count": len(values),
    }


# ─────────────────────────────────────────────
# Aggregation Response Builder
# ─────────────────────────────────────────────

def build_aggregation_response(query: str) -> dict:
    """
    Process aggregation query and return structured data.
    
    Returns:
        {
          "type": "aggregation",
          "query_type": "firms_list" | "metrics_comparison" | "ranking" | "stats",
          "data": [...],
          "description": str,
        }
    """
    query_lower = query.lower()
    
    # PATTERN 1: "Show all firms"
    if any(p in query_lower for p in ["show all firms", "list all firms", "list firms"]):
        firms = get_all_firms()
        return {
            "type": "aggregation",
            "query_type": "firms_list",
            "data": firms,
            "description": f"All {len(firms)} firms in the knowledge graph",
            "columns": ["Firm"],
        }
    
    # PATTERN 2: "Show firms and revenue/profit/etc"
    metric_match = None
    for metric in ["revenue", "profit", "assets", "margin", "employees"]:
        if metric in query_lower:
            metric_match = metric.capitalize()
            break
    
    if metric_match and ("show" in query_lower or "list" in query_lower or "compare" in query_lower):
        firms = get_all_firms()
        metrics = get_all_metrics_of_type(metric_match)
        
        data = []
        for firm in firms:
            firm_data = {"Firm": firm}
            if firm in metrics:
                for entity, values in metrics[firm].items():
                    firm_data[entity] = f"{values['value']} {values['unit']}".strip()
            data.append(firm_data)
        
        return {
            "type": "aggregation",
            "query_type": "metrics_comparison",
            "data": data,
            "description": f"Comparison of {metric_match} across firms",
            "columns": ["Firm"] + list(data[0].keys())[1:] if data else ["Firm"],
        }
    
    # PATTERN 3: "Which firm has highest/lowest revenue/profit"
    if "highest" in query_lower or "lowest" in query_lower:
        metric_match = None
        for metric in ["revenue", "profit", "assets", "margin", "employees"]:
            if metric in query_lower:
                metric_match = metric.capitalize()
                break
        
        if metric_match:
            if "highest" in query_lower:
                result = find_highest_metric(metric_match)
                action = "highest"
            else:
                result = find_lowest_metric(metric_match)
                action = "lowest"
            
            if result:
                return {
                    "type": "aggregation",
                    "query_type": "ranking",
                    "data": [result],
                    "description": f"{result['firm']} has {action} {metric_match}",
                    "columns": ["Firm", "Value", "Unit"],
                }
    
    # Default: Return all firms
    firms = get_all_firms()
    return {
        "type": "aggregation",
        "query_type": "firms_list",
        "data": firms,
        "description": f"All {len(firms)} firms in the knowledge graph",
        "columns": ["Firm"],
    }


# ─────────────────────────────────────────────
# Query Handler
# ─────────────────────────────────────────────

def handle_aggregation_query(query: str) -> dict:
    """
    Wrapper for aggregation queries.
    Returns structured response (no KG needed).
    """
    response = build_aggregation_response(query)
    
    # Convert data to proper format
    if isinstance(response.get("data"), list):
        if response.get("query_type") == "firms_list":
            # Format for display
            formatted_data = [{"Firm": firm} for firm in response["data"]]
        else:
            formatted_data = response["data"]
    else:
        formatted_data = []
    
    return {
        "answer": response.get("description", ""),
        "data": formatted_data,
        "metadata": {
            "query_type": response.get("query_type"),
            "columns": response.get("columns", []),
            "total_records": len(response.get("data", [])),
        }
    }
