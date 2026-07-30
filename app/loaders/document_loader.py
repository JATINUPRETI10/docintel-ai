from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
)


class DocumentLoader:
    def load(self, file_path: str):
        """
        Load a PDF, DOCX, or TXT file and return
        a list of LangChain Document objects.
        """

        extension = Path(file_path).suffix.lower()

        if extension == ".pdf":
            loader = PyPDFLoader(file_path)

        elif extension == ".docx":
            loader = Docx2txtLoader(file_path)

        elif extension == ".txt":
            loader = TextLoader(file_path, encoding="utf-8")

        else:
            raise ValueError(f"Unsupported file type: {extension}")

        return loader.load()