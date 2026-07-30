from langchain_ollama import ChatOllama


def get_llm():
    """
    Returns the local Ollama LLM instance.
    """
    return ChatOllama(
        model="llama3:latest",
        temperature=0
    )