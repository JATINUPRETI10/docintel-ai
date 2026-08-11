from app.chains.rag_chain import (
    RAGChain,
)


def test_rag_chain():

    rag = RAGChain()

    question = (
        "What is the Model Context Protocol?"
    )

    result = rag.ask(
        question
    )

    # -----------------------------
    # Validate result structure
    # -----------------------------

    assert isinstance(
        result,
        dict,
    )

    assert "answer" in result
    assert "documents" in result

    # -----------------------------
    # Validate answer
    # -----------------------------

    answer = result["answer"]

    assert isinstance(
        answer,
        str,
    )

    assert len(
        answer.strip()
    ) > 0

    # -----------------------------
    # Validate documents
    # -----------------------------

    documents = result["documents"]

    assert isinstance(
        documents,
        list,
    )

    assert len(documents) > 0

    for document in documents:

        assert "document" in document
        assert "page" in document
        assert "score" in document
        assert "content" in document

        assert document["content"]

    print(
        f"\nQuestion: {question}"
    )

    print(
        f"Answer: {answer}"
    )

    print(
        f"Retrieved chunks: "
        f"{len(documents)}"
    )