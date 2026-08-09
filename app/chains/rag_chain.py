from langchain_core.prompts import ChatPromptTemplate
from langsmith import traceable

from app.factories.components import get_llm_instance
from app.retrieval.retriever import Retriever


class RAGChain:

    def __init__(self):

        self.llm = get_llm_instance()

        self.retriever = Retriever()

        self.prompt = ChatPromptTemplate.from_template(
            """
You are a Question Answering AI.

Rules:

1. Answer ONLY using the provided context.
2. Never use outside knowledge.
3. Never guess.
4. If the answer is not in the context, reply exactly:

"I couldn't find this information in the uploaded document."

Context:
{context}

Question:
{question}

Answer:
"""
        )

    @traceable(name="RAG QA")
    def ask(self, question):

        # Retrieve relevant chunks
        docs = self.retriever.retrieve(question)

        # No relevant chunks found
        if not docs:
            return {
                "answer": "I couldn't find any relevant information in the uploaded document.",
                "documents": [],
            }

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

        # Collect retrieval metadata
        retrieved_docs = []

        for doc in docs:

            retrieved_docs.append(
                {
                    "document": doc.metadata.get("source", "Unknown"),
                    "page": doc.metadata.get("page", 0) + 1,
                    "score": doc.metadata.get("score"),
                    "length": len(doc.page_content),
                    "content": doc.page_content,
                }
            )

        return {
            "answer": response.content,
            "documents": retrieved_docs,
        }