from app.loaders.document_loader import DocumentLoader
from app.services.text_splitter import TextSplitter

loader = DocumentLoader()
documents = loader.load("documents/An AI Newsletter Generation System using MCP and 1.pdf")

splitter = TextSplitter()

chunks = splitter.split_documents(documents)

print(f"Pages Loaded : {len(documents)}")
print(f"Chunks Created : {len(chunks)}")

print("-" * 80)

print(chunks[0].page_content)

print("-" * 80)

print(chunks[0].metadata)