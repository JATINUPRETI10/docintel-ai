from app.loaders.document_loader import DocumentLoader

loader = DocumentLoader()

docs = loader.load("documents/An AI Newsletter Generation System using MCP and 1.pdf")

print(f"Total pages loaded: {len(docs)}")
print("-" * 50)
print(docs[0].page_content[:500])
print("-" * 50)
print(docs[0].metadata)