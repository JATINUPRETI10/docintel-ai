from pathlib import Path

from app.vectorstore.index_manager import IndexManager


PDF_PATH = (
    "documents/"
    "An AI Newsletter Generation System using MCP and 1.pdf"
)


def test_duplicate_document_is_not_indexed_twice():

    assert Path(PDF_PATH).exists(), (
        f"Test PDF not found: {PDF_PATH}"
    )

    manager = IndexManager()

    # First indexing attempt
    first_result = manager.index_document(
        PDF_PATH
    )

    count_after_first = (
        manager.vector_store.count()
    )

    assert first_result is not None

    assert first_result["status"] in (
        "indexed",
        "already_indexed",
    )

    # Second indexing attempt
    second_result = manager.index_document(
        PDF_PATH
    )

    count_after_second = (
        manager.vector_store.count()
    )

    # ---------------------------------------------
    # The second indexing must not add chunks
    # ---------------------------------------------

    assert (
        count_after_second
        == count_after_first
    )

    assert (
        second_result["status"]
        == "already_indexed"
    )