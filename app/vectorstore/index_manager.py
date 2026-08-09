from langsmith import traceable

from app.loaders.document_loader import DocumentLoader
from app.services.text_splitter import TextSplitter
from app.factories.components import get_vector_store


class IndexManager:

    def __init__(self):
        self.loader = DocumentLoader()
        self.splitter = TextSplitter()
        self.vector_store = get_vector_store()

    @traceable(name="Document Indexing")
    def index_document(self, pdf_path):

        print("Loading document...")
        documents = self.loader.load(pdf_path)

        print(f"Loaded {len(documents)} pages")

        print("Splitting document...")
        chunks = self.splitter.split_documents(documents)

        print(f"Created {len(chunks)} chunks")

        print("Saving into ChromaDB...")
        self.vector_store.add_documents(chunks)

        print("Indexing Complete!")

        print(
            f"Current Documents in DB : {self.vector_store.count()}"
        )