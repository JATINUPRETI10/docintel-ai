from app.chains.rag_chain import RAGChain

rag = RAGChain()

result = rag.ask(
    "Explain Model Context Protocol"
)

print("=" * 80)
print("ANSWER")
print("=" * 80)

print(result["answer"])

print()

print("=" * 80)
print("SOURCES")
print("=" * 80)

for source in result["sources"]:
    print(source)