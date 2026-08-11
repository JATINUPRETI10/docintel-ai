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
You are a precise document question-answering assistant.

Answer the user's question using ONLY information explicitly
supported by the provided document context.

RULES:

1. Use only the provided context.
2. Do not use outside knowledge.
3. Do not guess, infer, or introduce conclusions that are not
   directly supported by the context.
4. Combine information from multiple context chunks when they
   are relevant to the question.
5. Answer the question directly and completely.
6. Include the important details needed to answer the question,
   but do not add unnecessary information.
7. Prefer factual statements that can be directly traced to the
   provided context.
8. Do not repeat large portions of the context verbatim.
9. Do not mention "Context Chunk", retrieval scores, or internal
   processing in the answer.
10. If the context does not contain enough information to answer
    the question, reply exactly:

"I couldn't find this information in the uploaded document."

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}

ANSWER:
"""
        )

    @traceable(name="RAG QA")
    def ask(self, question):

        # -------------------------------------------------
        # Retrieve relevant documents
        # -------------------------------------------------

        docs = self.retriever.retrieve(question)

        # -------------------------------------------------
        # No relevant documents
        # -------------------------------------------------

        if not docs:

            return {
                "answer": (
                    "I couldn't find this information "
                    "in the uploaded document."
                ),
                "documents": [],
            }

        # -------------------------------------------------
        # Build context
        # -------------------------------------------------

        context_parts = []

        for index, doc in enumerate(
            docs,
            start=1
        ):

            page = doc.metadata.get(
                "page",
                0
            )

            source = doc.metadata.get(
                "source",
                "Unknown"
            )

            score = doc.metadata.get(
                "score"
            )

            context_parts.append(
                f"""
--- CONTEXT CHUNK {index} ---
Source: {source}
Page: {page + 1}
Retrieval Score: {score}

{doc.page_content}
"""
            )

        context = "\n".join(
            context_parts
        )

        # -------------------------------------------------
        # Generate answer
        # -------------------------------------------------

        chain = self.prompt | self.llm

        response = chain.invoke(
            {
                "context": context,
                "question": question,
            }
        )

        # -------------------------------------------------
        # Retrieved document metadata
        # -------------------------------------------------

        retrieved_docs = []

        for doc in docs:

            page = doc.metadata.get(
                "page",
                0
            )

            retrieved_docs.append(
                {
                    "document": doc.metadata.get(
                        "source",
                        "Unknown"
                    ),
                    "page": page + 1,
                    "score": doc.metadata.get(
                        "score"
                    ),
                    "length": len(
                        doc.page_content
                    ),
                    "content": doc.page_content,
                }
            )

        # -------------------------------------------------
        # Return
        # -------------------------------------------------

        return {
            "answer": response.content.strip(),
            "documents": retrieved_docs,
        }