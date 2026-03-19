"""
llm_handler.py
--------------
Groq API-based LLM answer generator for the Finance KG-RAG system.

Rules:
  - Answer ONLY using the provided context.
  - If context is missing or irrelevant → return "Insufficient data in provided context."
  - Maintain formal financial reasoning tone.
"""

import os
from groq import Groq

# ─────────────────────────────────────────────
# Groq client — key from env or hardcoded fallback
# ─────────────────────────────────────────────
_GROQ_API_KEY = os.environ.get(
    "GROQ_API_KEY",
    "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",
)
_client = Groq(api_key=_GROQ_API_KEY)

# LLM model — Updated to use supported Groq model
# mixtral-8x7b-32768 is a powerful, fast, and free model on Groq
LLM_MODEL = "mixtral-8x7b-32768"

SYSTEM_PROMPT = """You are a financial analysis assistant operating on a synthetic knowledge graph for academic research.

CONTEXT PRIORITY:
- PRIMARY: Knowledge Graph Facts (marked "PRIMARY SOURCE: KNOWLEDGE GRAPH FACTS") — Use FIRST
- SECONDARY: Retrieved Documents (marked "SUPPLEMENTARY CONTEXT") — Use only to add details

RESPONSE FORMAT RULES:
- For "show/list/compare/all" queries: ALWAYS list EACH item with its specific metric value from KG
- For financial metrics: Show exact values with units (e.g., "Firm_A Revenue_A_Y1: 120 M USD")
- For firm lists: Show firm name + relationship + description
- Format lists clearly with bullet points or numbered items

Rules you MUST follow:
1. ALWAYS prioritize Knowledge Graph facts over retrieved documents.
2. When listing firms/metrics, cite EVERY one found in KG context with exact values.
3. Answer ONLY from the context provided. Do not use external knowledge.
4. If the PRIMARY KG section lacks needed information, you may reference documents.
5. If no relevant data exists in either section, respond: "Insufficient data in provided context."
6. Maintain formal, precise financial reasoning tone.
7. For "show/list/compare/all" queries: Provide COMPLETE lists, not summaries.
8. Include specific numeric values with units (e.g., "120 M USD").
9. NEVER fabricate data, metrics, or relationships not explicitly stated.
10. NEVER infer or add units, values, or entities not in the context.
11. Do NOT rephrase entity identifiers (Firm_A stays Firm_A, not "the firm").
12. If context shows multiple metrics, list them ALL in your response."""


def generate_answer(query: str, merged_context: str) -> str:
    """
    Generate an answer from Groq LLM using merged KG + RAG context.

    Args:
        query:          User's natural language question.
        merged_context: Combined KG facts + retrieved documents.

    Returns:
        Answer string from the LLM.
    """
    if not merged_context.strip():
        return "Insufficient data in provided context."

    user_message = f"""Context:
{merged_context}

Question: {query}

Answer:"""

    try:
        response = _client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_message},
            ],
            temperature=0.1,   # Low temperature for factual, deterministic answers
            max_tokens=512,
        )
        return response.choices[0].message.content.strip()

    except Exception as exc:
        # Graceful degradation: return a simple extractive answer
        print(f"[LLM] Groq API error: {exc}")
        return _extractive_fallback(query, merged_context)


def _extractive_fallback(query: str, context: str) -> str:
    """
    Lightweight fallback when the API is unavailable.
    Intelligently extracts answer from context by prioritizing direct matches.
    
    Priority order:
    1. Values in PRIMARY QUERY ENTITIES section
    2. Values matching the queried firm
    3. Last resort: first VALUE: found
    """
    import re
    
    query_lower = query.lower()
    
    # Extract firm letter from query (e.g., "Firm_B" or "firm b")
    firm_match = re.search(r'\bfirm\s+([a-j])\b|\bfirm_?([a-j])\b', query_lower)
    queried_firm_letter = None
    if firm_match:
        queried_firm_letter = (firm_match.group(1) or firm_match.group(2)).upper()
    
    # Priority 1: Look in PRIMARY QUERY ENTITIES section first
    lines = context.split("\n")
    in_primary_section = False
    best_value = None
    
    for i, line in enumerate(lines):
        if "PRIMARY QUERY ENTITIES" in line:
            in_primary_section = True
        elif "RELATED ENTITIES" in line:
            in_primary_section = False
        
        # In primary section, look for VALUE: lines
        if in_primary_section and "VALUE:" in line:
            # Check if this value matches the queried firm
            if queried_firm_letter:
                # Look for Revenue_X pattern where X matches the queried firm
                if f"Revenue_{queried_firm_letter}" in context[max(0, i-5):i+1]:
                    value_match = re.search(r'VALUE:\s*([\d.,]+)\s*([A-Za-z]+(?:\s?[A-Za-z]+)*)', line)
                    if value_match:
                        return f"{value_match.group(1)} {value_match.group(2)}".strip()
                    best_value = line
    
    # Priority 2: If not found in primary section, look for firm-specific value
    if queried_firm_letter:
        for line in lines:
            if "PRIMARY QUERY" in line:
                # Still in context, look for firm-letter values
                if f"Revenue_{queried_firm_letter}" in line or f"_{queried_firm_letter}" in line:
                    if "VALUE:" in line:
                        value_match = re.search(r'VALUE:\s*([\d.,]+)\s*([A-Za-z]+(?:\s?[A-Za-z]+)*)', line)
                        if value_match:
                            return f"{value_match.group(1)} {value_match.group(2)}".strip()
    
    # Priority 3: Last resort - find PRIMARY entity VALUE
    if not best_value:
        for line in lines:
            if "[DIRECT]" in line and "VALUE:" in lines[lines.index(line)+1] if lines.index(line)+1 < len(lines) else False:
                value_line = lines[lines.index(line)+1]
                if "VALUE:" in value_line:
                    value_match = re.search(r'VALUE:\s*([\d.,]+)\s*([A-Za-z]+(?:\s?[A-Za-z]+)*)', value_line)
                    if value_match:
                        return f"{value_match.group(1)} {value_match.group(2)}".strip()
    
    # Fallback: Search with improved regex
    query_words = set(query_lower.split())
    best_line, best_score = "", 0
    
    for line in lines:
        if not line.strip() or "════" in line or "ENTITIES" in line:
            continue
        
        # Score based on query word matches
        score = sum(1 for w in query_words if w in line.lower())
        
        # Heavy boost for PRIMARY section
        if "[DIRECT]" in line:
            score += 20
        # Boost for lines with VALUE
        if "VALUE:" in line:
            score += 10
        # Boost for relationship lines showing main metrics
        if "--[reported]-->" in line or "--[has_metric]-->" in line:
            score += 5
        
        if score > best_score and score > 0:
            best_score = score
            best_line = line.strip()
    
    if best_line:
        # Extract VALUE if present (with unit)
        value_match = re.search(r'VALUE:\s*([\d.,]+)\s*([A-Za-z]+(?:\s?[A-Za-z]+)*)', best_line)
        if value_match:
            return f"{value_match.group(1)} {value_match.group(2)}".strip()
        
        # Clean up the line for display  
        best_line = best_line.replace("  →", "").replace("└─", "").strip()
        if best_line and best_line != "":
            return best_line
    
    return "Insufficient data in provided context."
