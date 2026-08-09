from langchain_chroma import Chroma
from config import CHROMA_PATH


class ChromaStore:

    def __init__(self, embedding_model):

        self.embedding_model = embedding_model

        self.db = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=self.embedding_model,
        )

    def add_documents(self, documents):
        self.db.add_documents(documents)

    def similarity_search_with_score(self, query, k=5):
        return self.db.similarity_search_with_score(
            query=query,
            k=k
        )

    def as_retriever(self, **kwargs):
        return self.db.as_retriever(**kwargs)

    def count(self):
        return self.db._collection.count()