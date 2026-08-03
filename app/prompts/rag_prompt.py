from langchain_core.prompts import ChatPromptTemplate

RAG_PROMPT = ChatPromptTemplate.from_template(
    """
You are a helpful AI assistant.

Answer ONLY using the provided context.

If the answer is not available in the context, reply:

"I couldn't find this information in the uploaded documents."

Context:
{context}

Question:
{question}

Answer:
"""
)