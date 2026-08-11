from pathlib import Path

from app.loaders.document_loader import DocumentLoader
from app.services.text_splitter import TextSplitter


PDF_PATH = "documents/An AI Newsletter Generation System using MCP and 1.pdf"


def test_text_splitter():

    assert Path(PDF_PATH).exists(), (
        f"Test PDF not found: {PDF_PATH}"
    )

    loader = DocumentLoader()

    documents = loader.load(PDF_PATH)

    assert len(documents) > 0

    splitter = TextSplitter()

    chunks = splitter.split_documents(
        documents
    )

    assert chunks is not None
    assert len(chunks) > 0

    for chunk in chunks:

        assert chunk.page_content
        assert isinstance(
            chunk.page_content,
            str,
        )

        assert isinstance(
            chunk.metadata,
            dict,
        )

    print(
        f"\nPages loaded: {len(documents)}"
    )

    print(
        f"Chunks created: {len(chunks)}"
    )