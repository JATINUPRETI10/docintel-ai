from pathlib import Path

from app.vectorstore.index_manager import (
    IndexManager,
)


PDF_PATH = "documents/An AI Newsletter Generation System using MCP and 1.pdf"


def test_index_manager():

    assert Path(PDF_PATH).exists(), (
        f"Test PDF not found: {PDF_PATH}"
    )

    manager = IndexManager()

    assert manager is not None

    manager.index_document(
        PDF_PATH
    )

    count = manager.vector_store.count()

    assert count > 0

    print(
        f"\nIndexed chunks: {count}"
    )