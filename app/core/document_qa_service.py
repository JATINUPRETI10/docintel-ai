from pathlib import Path

from app.vectorstore.index_manager import IndexManager
from app.chains.rag_chain import RAGChain


class DocumentQAService:

    def __init__(self):

        self.index_manager = IndexManager()
        self.rag = RAGChain()

    # -------------------------------------------------
    # Index document
    # -------------------------------------------------

    def index_document(self, pdf_path):

        if not pdf_path:
            raise ValueError(
                "Document path cannot be empty."
            )

        path = Path(pdf_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Document not found: {pdf_path}"
            )

        if not path.is_file():
            raise ValueError(
                f"Invalid document path: {pdf_path}"
            )

        return self.index_manager.index_document(
            str(path)
        )

    # -------------------------------------------------
    # Ask question
    # -------------------------------------------------

    def ask(self, question):

        if question is None:
            raise ValueError(
                "Question cannot be empty."
            )

        if not isinstance(question, str):
            raise TypeError(
                "Question must be a string."
            )

        question = question.strip()

        if not question:
            raise ValueError(
                "Question cannot be empty."
            )

        return self.rag.ask(
            question
        )