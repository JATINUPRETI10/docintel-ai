from app.vectorstore.index_manager import IndexManager

manager = IndexManager()

manager.index_document(
    "documents/An AI Newsletter Generation System using MCP and 1.pdf"
)