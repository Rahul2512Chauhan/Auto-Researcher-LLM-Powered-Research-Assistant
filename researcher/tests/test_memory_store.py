# researcher/tests/test_memory_store.py
import pprint
from researcher.memory.memory_store import MemoryStore

print("\n=== TEST MEMORY STORE ===")
ms = MemoryStore(persist_directory="./.local_memory_test")

# add a summary
sid = ms.add("summaries", "This paper proposes a novel RAG method that reduces hallucinations.", metadata={"title": "Paper A", "id": "paper-a"})
print("Added summary id:", sid)

# add an insight
iid = ms.add("insights", "Using debate-augmented retrieval increases factuality in RAG.", metadata={"source": "paper-a", "topic": "RAG-hallucinations"})
print("Added insight id:", iid)

# query by semantic text
res = ms.query("insights", "how to reduce hallucinations in RAG", top_k=3)
print("\nQuery results (insights):")
pprint.pprint(res)

# get by id
g = ms.get("insights", iid)
print("\nGet by id result:")
pprint.pprint(g)

# cleanup: delete the insight
ok = ms.delete("insights", iid)
print("\nDeleted insight:", ok)

print("\nCollections available:", ms.list_collections())

print("\n✅ Memory store test complete.")
