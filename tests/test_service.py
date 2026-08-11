from app.core.document_qa_service import (
    DocumentQAService,
)


def test_document_qa_service():

    service = DocumentQAService()

    result = service.ask(
        "Explain Model Context Protocol"
    )

    # -----------------------------
    # Validate result
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

        assert isinstance(
            document,
            dict,
        )

        assert "document" in document
        assert "page" in document
        assert "score" in document
        assert "length" in document
        assert "content" in document

        assert document["content"]

    print(
        f"\nAnswer: {answer}"
    )

    print(
        f"Retrieved chunks: "
        f"{len(documents)}"
    )