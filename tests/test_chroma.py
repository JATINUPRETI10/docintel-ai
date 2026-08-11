from app.embeddings.embedding_model import (
    get_embedding_model,
)

from app.vectorstore.chroma_store import (
    ChromaStore,
)


def test_chroma_store():

    embedding_model = get_embedding_model()

    db = ChromaStore(
        embedding_model
    )

    assert db is not None

    count = db.count()

    assert isinstance(
        count,
        int,
    )

    assert count >= 0

    print(
        f"\nChromaDB document count: {count}"
    )