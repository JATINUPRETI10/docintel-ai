from app.core.document_qa_service import DocumentQAService

service = DocumentQAService()

# Uncomment this only if you need to index a new PDF
# service.index_document("documents/An AI Newsletter Generation System using MCP and 1.pdf")

result = service.ask("Explain Model Context Protocol")

print("=" * 80)
print(result["answer"])

print("\nSources:")

for source in result["sources"]:
    print(source)