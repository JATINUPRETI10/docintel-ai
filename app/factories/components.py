from functools import lru_cache

from app.llm.ollama_model import get_llm
from app.embeddings.embedding_model import get_embedding_model
from app.vectorstore.chroma_store import ChromaStore


@lru_cache(maxsize=1)
def get_llm_instance():
    return get_llm()


@lru_cache(maxsize=1)
def get_embedding_instance():
    return get_embedding_model()


@lru_cache(maxsize=1)
def get_vector_store():

    embedding = get_embedding_instance()

    return ChromaStore(embedding)