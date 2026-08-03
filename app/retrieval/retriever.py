from app.embeddings.embedding_model import get_embedding_model
from app.vectorstore.chroma_store import ChromaStore
from config import TOP_K

class Retriever:

    def __init__(self):

        embedding_model = get_embedding_model()

        self.vector_store = ChromaStore(embedding_model)

        self.retriever = self.vector_store.as_retriever(
            search_kwargs={"k": TOP_K}
        )

    def retrieve(self, query):

        return self.retriever.invoke(query)