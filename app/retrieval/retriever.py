from app.embeddings.embedding_model import get_embedding_model
from app.factories.components import get_vector_store
from config import TOP_K


class Retriever:

    def __init__(self):

        self.vector_store = get_vector_store()

        self.retriever = self.vector_store.as_retriever(
            search_kwargs={"k": TOP_K}
        )

    def retrieve(self, query):
        return self.retriever.invoke(query)