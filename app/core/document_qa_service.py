from app.vectorstore.index_manager import IndexManager
from app.chains.rag_chain import RAGChain


class DocumentQAService:

    def __init__(self):
        self.index_manager = IndexManager()
        self.rag = RAGChain()

    def index_document(self, pdf_path):
        self.index_manager.index_document(pdf_path)

    def ask(self, question):
        return self.rag.ask(question)