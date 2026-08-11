from pathlib import Path

from app.loaders.document_loader import DocumentLoader


PDF_PATH = "documents/An AI Newsletter Generation System using MCP and 1.pdf"


def test_document_loader():

    assert Path(PDF_PATH).exists(), (
        f"Test PDF not found: {PDF_PATH}"
    )

    loader = DocumentLoader()

    docs = loader.load(PDF_PATH)

    assert docs is not None
    assert len(docs) > 0

    assert docs[0].page_content
    assert isinstance(
        docs[0].page_content,
        str,
    )

    assert isinstance(
        docs[0].metadata,
        dict,
    )

    print(
        f"\nTotal pages loaded: {len(docs)}"
    )

    print(
        f"First page characters: "
        f"{len(docs[0].page_content)}"
    )