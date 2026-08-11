import hashlib
from pathlib import Path

from langsmith import traceable

from app.loaders.document_loader import DocumentLoader
from app.services.text_splitter import TextSplitter
from app.factories.components import get_vector_store


class IndexManager:

    def __init__(self):

        self.loader = DocumentLoader()
        self.splitter = TextSplitter()
        self.vector_store = get_vector_store()

    # -------------------------------------------------
    # Generate SHA-256 document hash
    # -------------------------------------------------

    def _get_document_hash(self, pdf_path):

        sha256 = hashlib.sha256()

        with open(
            pdf_path,
            "rb",
        ) as file:

            for chunk in iter(
                lambda: file.read(1024 * 1024),
                b"",
            ):

                sha256.update(chunk)

        return sha256.hexdigest()

    # -------------------------------------------------
    # Index document
    # -------------------------------------------------

    @traceable(name="Document Indexing")
    def index_document(self, pdf_path):

        pdf_path = str(
            Path(pdf_path).resolve()
        )

        # ---------------------------------------------
        # Validate file
        # ---------------------------------------------

        if not Path(pdf_path).exists():

            raise FileNotFoundError(
                f"Document not found: {pdf_path}"
            )

        print(
            "Calculating document hash..."
        )

        document_hash = self._get_document_hash(
            pdf_path
        )

        print(
            f"Document Hash: {document_hash[:16]}..."
        )

        # ---------------------------------------------
        # Duplicate check
        # ---------------------------------------------

        if self.vector_store.document_exists(
            document_hash
        ):

            print(
                "Document already indexed."
            )

            print(
                "Skipping duplicate indexing."
            )

            print(
                f"Current Documents in DB : "
                f"{self.vector_store.count()}"
            )

            return {
                "status": "already_indexed",
                "document_hash": document_hash,
                "count": self.vector_store.count(),
            }

        # ---------------------------------------------
        # Load document
        # ---------------------------------------------

        print(
            "Loading document..."
        )

        documents = self.loader.load(
            pdf_path
        )

        print(
            f"Loaded {len(documents)} pages"
        )

        # ---------------------------------------------
        # Add document metadata
        # ---------------------------------------------

        for document in documents:

            document.metadata[
                "document_hash"
            ] = document_hash

            document.metadata[
                "source"
            ] = pdf_path

        # ---------------------------------------------
        # Split document
        # ---------------------------------------------

        print(
            "Splitting document..."
        )

        chunks = self.splitter.split_documents(
            documents
        )

        print(
            f"Created {len(chunks)} chunks"
        )

        # ---------------------------------------------
        # Make sure every chunk has the hash
        # ---------------------------------------------

        for chunk in chunks:

            chunk.metadata[
                "document_hash"
            ] = document_hash

            chunk.metadata[
                "source"
            ] = pdf_path

        # ---------------------------------------------
        # Save to ChromaDB
        # ---------------------------------------------

        print(
            "Saving into ChromaDB..."
        )

        self.vector_store.add_documents(
            chunks
        )

        print(
            "Indexing Complete!"
        )

        current_count = (
            self.vector_store.count()
        )

        print(
            f"Current Documents in DB : "
            f"{current_count}"
        )

        return {
            "status": "indexed",
            "document_hash": document_hash,
            "chunks": len(chunks),
            "count": current_count,
        }