import json
from pathlib import Path

from app.core.document_qa_service import DocumentQAService


# =====================================================
# Paths
# =====================================================

RESULTS_DIR = Path("evaluation/results")

OUTPUT_FILE = RESULTS_DIR / "rag_results.json"


# =====================================================
# Expanded Evaluation Dataset
# =====================================================
#
# Questions are based on information present in the
# documents already used by the original evaluation.
#
# =====================================================

EVALUATION_DATASET = [

    # -------------------------------------------------
    # Transformer
    # -------------------------------------------------

    {
        "question": "What is a Transformer?",
        "reference": (
            "The Transformer is a model architecture based entirely "
            "on attention mechanisms, dispensing with recurrence and "
            "convolutions."
        ),
    },

    {
        "question": "What mechanism does the Transformer rely on?",
        "reference": (
            "The Transformer relies entirely on self-attention and "
            "uses attention mechanisms to draw global dependencies "
            "between input and output."
        ),
    },

    {
        "question": "What is the overall architecture of the Transformer?",
        "reference": (
            "The Transformer uses stacked self-attention and "
            "point-wise fully connected layers for both the encoder "
            "and decoder."
        ),
    },

    {
        "question": "How many identical layers are in the Transformer encoder?",
        "reference": (
            "The Transformer encoder is composed of a stack of "
            "N = 6 identical layers."
        ),
    },

    {
        "question": "What are the two sub-layers in each Transformer encoder layer?",
        "reference": (
            "Each encoder layer has a multi-head self-attention "
            "mechanism followed by a simple position-wise layer."
        ),
    },

    {
        "question": "What advantage does the Transformer provide in terms of computation?",
        "reference": (
            "The Transformer reduces sequential computation and "
            "allows significantly more parallelization."
        ),
    },

    # -------------------------------------------------
    # MCP
    # -------------------------------------------------

    {
        "question": "What is the Model Context Protocol (MCP)?",
        "reference": (
            "The Model Context Protocol provides a structural link "
            "that enables interaction between a large language model "
            "and plugins through a standard format."
        ),
    },

    {
        "question": "How does MCP allow plugins to communicate with a large language model?",
        "reference": (
            "MCP allows various plugins to interface through a "
            "standard format, ensuring consistent communication "
            "with a large language model."
        ),
    },

    {
        "question": "What problem does MCP address?",
        "reference": (
            "MCP addresses the complexity of integrating multiple "
            "data sources and tools by providing structured interaction "
            "through a unified and standardized framework."
        ),
    },

    {
        "question": "How does MCP improve scalability and flexibility?",
        "reference": (
            "MCP separates data collection, processing, and content "
            "generation and uses independent connectors operating "
            "through the same protocol, improving scalability and flexibility."
        ),
    },
]


# =====================================================
# Generate RAG Results
# =====================================================

def collect_results():

    print("=" * 80)
    print("DOCINTEL AI - EXPANDED RAG RESULT COLLECTION")
    print("=" * 80)

    print(
        f"\nEvaluation samples: "
        f"{len(EVALUATION_DATASET)}"
    )

    service = DocumentQAService()

    results = []

    for index, item in enumerate(
        EVALUATION_DATASET,
        start=1,
    ):

        question = item["question"]
        reference = item["reference"]

        print("\n" + "-" * 80)
        print(
            f"QUESTION {index}/{len(EVALUATION_DATASET)}"
        )
        print("-" * 80)

        print(
            f"Question: {question}"
        )

        try:

            result = service.ask(question)

            answer = result.get(
                "answer",
                ""
            )

            documents = result.get(
                "documents",
                []
            )

            contexts = []

            for document in documents:

                content = document.get(
                    "content",
                    ""
                )

                if content:

                    contexts.append(
                        content
                    )

            print("\nANSWER:")
            print(answer)

            print(
                f"\nRetrieved chunks: "
                f"{len(contexts)}"
            )

            results.append(
                {
                    "question": question,
                    "reference": reference,
                    "answer": answer,
                    "contexts": contexts,
                }
            )

        except Exception as e:

            print(
                f"\nERROR: {e}"
            )

            results.append(
                {
                    "question": question,
                    "reference": reference,
                    "answer": "",
                    "contexts": [],
                    "error": str(e),
                }
            )

    # =================================================
    # Save results
    # =================================================

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            results,
            file,
            indent=4,
            ensure_ascii=False,
        )

    print("\n")
    print("=" * 80)
    print("RAG RESULTS SAVED")
    print("=" * 80)

    print(
        f"File: {OUTPUT_FILE}"
    )

    print(
        f"Samples: {len(results)}"
    )


# =====================================================
# Main
# =====================================================

if __name__ == "__main__":

    collect_results()