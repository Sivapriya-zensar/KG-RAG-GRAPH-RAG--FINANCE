# Synthetic Finance KG-RAG System
### Academic Research Demo · Anonymized Entities · Knowledge Graph + Retrieval-Augmented Generation

---

## 📁 Project Structure

```
finance_kg_rag/
├── backend/
│   ├── synthetic_data.py   # 10 synthetic docs + KG triples + entity attributes
│   ├── kg_builder.py       # NetworkX DiGraph — build, query, serialize
│   ├── rag_engine.py       # all-MiniLM-L6-v2 embeddings + FAISS index
│   ├── fusion.py           # Entity extraction + KG/RAG context merger
│   ├── llm_handler.py      # Groq API (llama3-8b-8192) with fallback
│   └── app.py              # Flask server — /query, /graph, /
├── frontend/
│   └── index.html          # D3.js force-directed graph + query UI
└── requirements.txt
```

---

## ⚡ Quick Start (VS Code)

### 1. Open Terminal in VS Code
`Ctrl + backtick`  →  `View > Terminal`

### 2. Install Dependencies
```bash
cd "c:\Users\sivap\Desktop\KG RAG implementation paperwork\finance_kg_rag"
pip install -r requirements.txt
```

### 3. Run the Backend
```bash
cd backend
python app.py
```
You should see:
```
═══════════════════════════════════════════════════════
  Synthetic Finance KG-RAG System
  Backend: http://localhost:5000
═══════════════════════════════════════════════════════
[RAG] Indexed 10 documents | dim=384
 * Running on http://0.0.0.0:5000
```

### 4. Open the Frontend
Open your browser and go to: **http://localhost:5000**

---

## 🧪 Example Queries

| Query | Expected Behaviour |
|---|---|
| `What is Firm_A's revenue?` | Cites Revenue_Y1 = 120M USD |
| `What does PE_Ratio indicate?` | Points to Growth_Expectation |
| `Which firm was acquired by Firm_A?` | Returns Firm_B, Acquisition_E1 |
| `How does diversification affect risk?` | Links Diversification → Risk_Level |
| `What instruments does Firm_A hold?` | Cites Equity_X (500M USD) |
| `Tell me about Bond_Y` | Coupon 6%, issued by Firm_C |
| `What is the weather today?` | "Insufficient data in provided context." |

---

## 🕸️ D3.js Graph Features

| Feature | Description |
|---|---|
| **Colour coding** | Firms = green · Metrics = blue · Instruments = amber · Events = pink |
| **Hover tooltip** | Shows entity type, value, unit, year, description |
| **Click to highlight** | Dims all non-adjacent nodes; highlights connected edges |
| **Drag nodes** | Reposition any entity freely |
| **Zoom / Pan** | Scroll to zoom, drag canvas to pan; `+`/`−`/`⟳` buttons |
| **Quick chips** | Click an example chip to auto-submit a query |

---

## 🏗️ Architecture

```
User Query
    │
    ▼
[Fusion] ── regex entity extraction
    ├── [KG] NetworkX graph facts
    └── [RAG] FAISS similarity search (all-MiniLM-L6-v2)
           │
           ▼
    Merged Context
           │
           ▼
    [Groq LLM] llama3-8b-8192
    (context-only · "Insufficient data" fallback)
           │
           ▼
    JSON Answer → D3.js Frontend
```

---

## 🚀 API Reference

### `POST /query`
```json
// Request
{ "query": "What is Firm_A's revenue?" }

// Response
{
  "answer": "Firm_A reported Revenue_Y1 of 120M USD in 2023...",
  "entities_found": ["Firm_A", "Revenue_Y1"],
  "kg_context": "...",
  "doc_context": "..."
}
```

### `GET /graph`
```json
{
  "nodes": [{"id": "Firm_A", "entity_type": "Firm", "value": null, ...}],
  "links": [{"source": "Firm_A", "target": "Revenue_Y1", "relation": "reported"}]
}
```

---

## ⚠️ Constraints

- **No real company names** — all entities are synthetic identifiers
- **Context-only answers** — LLM cannot access information outside the provided KG + documents
- **Academic use only** — dataset is intentionally synthetic and simplified

---

## 🔧 Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: faiss` | Run `pip install faiss-cpu` |
| `ModuleNotFoundError: groq` | Run `pip install groq` |
| `OSError: [WinError 10061] Connection refused` | Ensure `python app.py` is running |
| Graph not loading | Check browser console; verify Flask is on port 5000 |
| Groq API error | Check API key or internet connection; fallback answer is returned |
