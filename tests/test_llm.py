from app.llm.ollama_model import get_llm


llm = get_llm()

response = llm.invoke("Introduce yourself in one sentence.")

print(response.content)