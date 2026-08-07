from langchain_core.prompts import ChatPromptTemplate

from app.llm.ollama_model import get_llm
from app.retrieval.retriever import Retriever
from app.factories.components import get_llm_instance

class RAGChain:

    def __init__(self):

        self.llm = get_llm_instance()

        self.retriever = Retriever()

        self.prompt = ChatPromptTemplate.from_template(
            """
You are a helpful AI assistant.

Answer ONLY using the context below.

If the answer is not present in the context, reply:

"I couldn't find this information in the uploaded document."

Context:
{context}

Question:
{question}

Answer:
"""
        )

    def ask(self, question):

        # Retrieve relevant chunks
        docs = self.retriever.retrieve(question)

        # Build context
        context = "\n\n".join(
            doc.page_content for doc in docs
        )

        # Create chain
        chain = self.prompt | self.llm

        # Generate answer
        response = chain.invoke(
            {
                "context": context,
                "question": question,
            }
        )

        # Collect source pages
        sources = []

        for doc in docs:
            page = doc.metadata.get("page", "Unknown")

            if page != "Unknown":
                sources.append(f"Page {page + 1}")
            else:
                sources.append("Unknown")

        # Remove duplicate pages
        sources = list(dict.fromkeys(sources))

        return {
            "answer": response.content,
            "sources": sources,
        }