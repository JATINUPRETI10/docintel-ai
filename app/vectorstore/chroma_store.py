from langchain_chroma import Chroma

from config import CHROMA_PATH


class ChromaStore:

    def __init__(self, embedding_model):

        self.embedding_model = embedding_model

        self.db = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=self.embedding_model,
        )

    # -------------------------------------------------
    # Add documents
    # -------------------------------------------------

    def add_documents(self, documents):

        return self.db.add_documents(
            documents
        )

    # -------------------------------------------------
    # Check whether a document is already indexed
    # -------------------------------------------------

    def document_exists(self, document_hash):

        results = self.db.get(
            where={
                "document_hash": document_hash
            },
            limit=1,
        )

        ids = results.get(
            "ids",
            []
        )

        return len(ids) > 0

    # -------------------------------------------------
    # Similarity search
    # -------------------------------------------------

    def similarity_search_with_score(
        self,
        query,
        k=5,
    ):

        return self.db.similarity_search_with_score(
            query=query,
            k=k,
        )

    # -------------------------------------------------
    # Retriever
    # -------------------------------------------------

    def as_retriever(self, **kwargs):

        return self.db.as_retriever(
            **kwargs
        )

    # -------------------------------------------------
    # Count
    # -------------------------------------------------

    def count(self):

        return self.db._collection.count()