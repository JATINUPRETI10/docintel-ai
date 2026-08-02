from langchain_text_splitters import RecursiveCharacterTextSplitter


class TextSplitter:

    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 150,
    ):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def split_documents(self, documents):
        return self.splitter.split_documents(documents)