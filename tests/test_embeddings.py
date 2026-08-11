from app.embeddings.embedding_model import (
    get_embedding_model,
)


def test_embedding_model():

    embeddings = get_embedding_model()

    vector = embeddings.embed_query(
        "Hello World"
    )

    assert vector is not None
    assert len(vector) > 0

    assert all(
        isinstance(value, (int, float))
        for value in vector
    )

    print(
        f"\nEmbedding dimension: {len(vector)}"
    )