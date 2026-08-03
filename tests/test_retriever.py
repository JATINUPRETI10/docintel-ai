from app.retrieval.retriever import Retriever

retriever = Retriever()

docs = retriever.retrieve(
    "Explain Model Context Protocol"
)

print(f"Retrieved {len(docs)} documents\n")

for i, doc in enumerate(docs, start=1):

    print("=" * 80)
    print(f"Chunk {i}")
    print("=" * 80)

    print(doc.page_content[:500])

    print("\nMetadata:")
    print(doc.metadata)