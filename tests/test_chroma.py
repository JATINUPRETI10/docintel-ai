from app.embeddings.embedding_model import get_embedding_model
from app.vectorstore.chroma_store import ChromaStore

embedding_model = get_embedding_model()

db = ChromaStore(embedding_model)

print("Database Created Successfully!")

print("Current Documents:", db.count())