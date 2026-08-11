from app.core.document_qa_service import DocumentQAService


# =====================================================
# Initialize Service
# =====================================================

service = DocumentQAService()


# =====================================================
# Ask Question
# =====================================================

result = service.ask(
    "Explain Model Context Protocol"
)


# =====================================================
# Display Answer
# =====================================================

print("=" * 80)

print("ANSWER")
print("=" * 80)

print(result["answer"])


# =====================================================
# Display Retrieved Documents
# =====================================================

print("\n")
print("=" * 80)

print("RETRIEVED DOCUMENTS")
print("=" * 80)


documents = result.get(
    "documents",
    []
)


print(
    f"Retrieved {len(documents)} chunks"
)


for index, document in enumerate(
    documents,
    start=1
):

    print("\n" + "-" * 80)

    print(
        f"Chunk {index}"
    )

    print(
        f"Document: "
        f"{document.get('document', 'Unknown')}"
    )

    print(
        f"Page: "
        f"{document.get('page', 'Unknown')}"
    )

    print(
        f"Score: "
        f"{document.get('score', 'N/A')}"
    )

    print(
        f"Length: "
        f"{document.get('length', 0)} characters"
    )

    print("\nContent:")

    print(
        document.get(
            "content",
            ""
        )
    )

print("\n")
print("=" * 80)

print("TEST COMPLETED")

print("=" * 80)