"""Quick endpoint smoke-test for the Finance KG-RAG backend."""
import urllib.request
import urllib.parse
import json

BASE = "http://localhost:5000"

def test_graph():
    r = urllib.request.urlopen(BASE + "/graph", timeout=5)
    d = json.loads(r.read())
    print(f"/graph  => Nodes: {len(d['nodes'])}, Links: {len(d['links'])}")
    for n in d['nodes'][:6]:
        print(f"   {n['id']:22s}  type={n['entity_type']}")

def test_query(q):
    body = json.dumps({"query": q}).encode()
    req  = urllib.request.Request(
        BASE + "/query",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    r = urllib.request.urlopen(req, timeout=30)
    d = json.loads(r.read())
    print(f"\n/query => '{q}'")
    print(f"  entities : {d.get('entities_found')}")
    print(f"  answer   : {d.get('answer', '')[:200]}")

if __name__ == "__main__":
    test_graph()
    test_query("What is Firm_A revenue?")
    test_query("What does PE_Ratio indicate?")
    test_query("Which firm was acquired by Firm_A?")
    print("\nAll tests done.")
