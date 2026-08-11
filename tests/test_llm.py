from app.llm.ollama_model import (
    get_llm,
)


def test_llm():

    llm = get_llm()

    response = llm.invoke(
        "Introduce yourself in one sentence."
    )

    assert response is not None

    assert hasattr(
        response,
        "content",
    )

    assert isinstance(
        response.content,
        str,
    )

    assert len(
        response.content.strip()
    ) > 0

    print(
        f"\nLLM response: "
        f"{response.content}"
    )