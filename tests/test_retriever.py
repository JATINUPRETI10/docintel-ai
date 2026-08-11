from app.retrieval.retriever import (
    Retriever,
)


def test_retriever():

    retriever = Retriever()

    docs = retriever.retrieve(
        "Explain Model Context Protocol"
    )

    assert docs is not None
    assert isinstance(
        docs,
        list,
    )

    assert len(docs) > 0

    for doc in docs:

        assert doc.page_content

        assert isinstance(
            doc.page_content,
            str,
        )

        assert isinstance(
            doc.metadata,
            dict,
        )

        assert "score" in doc.metadata

    print(
        f"\nRetrieved documents: {len(docs)}"
    )