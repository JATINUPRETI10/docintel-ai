import asyncio
import json
from pathlib import Path

import pandas as pd

from openai import AsyncOpenAI

from ragas.llms import llm_factory
from ragas.embeddings import HuggingFaceEmbeddings

from ragas.metrics.collections import (
    Faithfulness,
    AnswerRelevancy,
    ContextPrecision,
    ContextRecall,
)


# =====================================================
# Paths
# =====================================================

RESULTS_DIR = Path("evaluation/results")

RAW_RESULTS_FILE = (
    RESULTS_DIR / "rag_results.json"
)

FINAL_RESULTS_FILE = (
    RESULTS_DIR / "ragas_results.csv"
)


# =====================================================
# Load RAG Results
# =====================================================

def load_results():

    if not RAW_RESULTS_FILE.exists():

        raise FileNotFoundError(
            f"Evaluation data not found: {RAW_RESULTS_FILE}"
        )

    with open(
        RAW_RESULTS_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)


# =====================================================
# Create Evaluator Models
# =====================================================

def create_evaluators():

    print("\nInitializing evaluator LLM...")

    # Ollama local OpenAI-compatible API
    client = AsyncOpenAI(
        api_key="ollama",
        base_url="http://localhost:11434/v1",
    )

    evaluator_llm = llm_factory(
        "llama3:latest",
        provider="openai",
        client=client,
    )

    print("Evaluator LLM ready.")

    print("Loading evaluation embeddings...")

    evaluator_embeddings = HuggingFaceEmbeddings(
        model="BAAI/bge-small-en-v1.5"
    )

    print("Evaluation embeddings ready.")

    return (
        evaluator_llm,
        evaluator_embeddings,
    )

# =====================================================
# Create Metrics
# =====================================================

def create_metrics(
    evaluator_llm,
    evaluator_embeddings,
):

    return [

        Faithfulness(
            llm=evaluator_llm
        ),

        AnswerRelevancy(
            llm=evaluator_llm,
            embeddings=evaluator_embeddings,
        ),

        ContextPrecision(
            llm=evaluator_llm
        ),

        ContextRecall(
            llm=evaluator_llm
        ),
    ]


# =====================================================
# Evaluate One Sample
# =====================================================

async def evaluate_sample(
    sample,
    metrics,
):

    print("\n" + "-" * 80)

    print(
        f"QUESTION: {sample['question']}"
    )

    print(
        f"ANSWER: {sample['answer']}"
    )

    scores = {}

    # -------------------------------------------------
    # Faithfulness
    # -------------------------------------------------

    try:

        result = await metrics[0].ascore(
            user_input=sample["question"],
            response=sample["answer"],
            retrieved_contexts=sample["contexts"],
        )

        scores["faithfulness"] = float(
            result.value
        )

        print(
            f"Faithfulness: {result.value:.4f}"
        )

        if result.reason:
            print(
                f"Reason: {result.reason}"
            )

    except Exception as e:

        print(
            f"Faithfulness ERROR: {e}"
        )

        scores["faithfulness"] = None

    # -------------------------------------------------
    # Answer Relevancy
    # -------------------------------------------------

    try:

        result = await metrics[1].ascore(
            user_input=sample["question"],
            response=sample["answer"],
        )

        scores["answer_relevancy"] = float(
            result.value
        )

        print(
            f"Answer Relevancy: {result.value:.4f}"
        )

        if result.reason:
            print(
                f"Reason: {result.reason}"
            )

    except Exception as e:

        print(
            f"Answer Relevancy ERROR: {e}"
        )

        scores["answer_relevancy"] = None

    # -------------------------------------------------
    # Context Precision
    # -------------------------------------------------

    try:

        result = await metrics[2].ascore(
            user_input=sample["question"],
            retrieved_contexts=sample["contexts"],
            reference=sample["reference"],
        )

        scores["context_precision"] = float(
            result.value
        )

        print(
            f"Context Precision: {result.value:.4f}"
        )

        if result.reason:
            print(
                f"Reason: {result.reason}"
            )

    except Exception as e:

        print(
            f"Context Precision ERROR: {e}"
        )

        scores["context_precision"] = None

    # -------------------------------------------------
    # Context Recall
    # -------------------------------------------------

    try:

        result = await metrics[3].ascore(
            user_input=sample["question"],
            retrieved_contexts=sample["contexts"],
            reference=sample["reference"],
        )

        scores["context_recall"] = float(
            result.value
        )

        print(
            f"Context Recall: {result.value:.4f}"
        )

        if result.reason:
            print(
                f"Reason: {result.reason}"
            )

    except Exception as e:

        print(
            f"Context Recall ERROR: {e}"
        )

        scores["context_recall"] = None

    return scores


# =====================================================
# Main Evaluation
# =====================================================

async def run_evaluation():

    print("=" * 80)
    print("DOCINTEL AI - RAGAS EVALUATION")
    print("=" * 80)

    # -------------------------------------------------
    # Load existing RAG results
    # -------------------------------------------------

    results = load_results()

    print(
        f"\nLoaded {len(results)} evaluation samples."
    )

    # -------------------------------------------------
    # Create evaluator
    # -------------------------------------------------

    (
        evaluator_llm,
        evaluator_embeddings,
    ) = create_evaluators()

    # -------------------------------------------------
    # Create metrics
    # -------------------------------------------------

    metrics = create_metrics(
        evaluator_llm,
        evaluator_embeddings,
    )

    print("\nMetrics:")

    print("  - Faithfulness")
    print("  - Answer Relevancy")
    print("  - Context Precision")
    print("  - Context Recall")

    print("\nStarting evaluation...")
    print(
        "Ollama will evaluate each sample locally."
    )

    # -------------------------------------------------
    # Evaluate samples
    # -------------------------------------------------

    final_results = []

    for index, sample in enumerate(
        results,
        start=1,
    ):

        print("\n")
        print("=" * 80)
        print(
            f"EVALUATING SAMPLE {index}/{len(results)}"
        )
        print("=" * 80)

        if sample.get("error"):

            print(
                "Skipping sample because "
                "the RAG run failed."
            )

            continue

        scores = await evaluate_sample(
            sample,
            metrics,
        )

        final_results.append(
            {
                "question": sample["question"],
                "reference": sample["reference"],
                "answer": sample["answer"],
                **scores,
            }
        )

    # -------------------------------------------------
    # Create DataFrame
    # -------------------------------------------------

    dataframe = pd.DataFrame(
        final_results
    )

    # -------------------------------------------------
    # Calculate averages
    # -------------------------------------------------

    metric_columns = [
        "faithfulness",
        "answer_relevancy",
        "context_precision",
        "context_recall",
    ]

    print("\n")
    print("=" * 80)
    print("FINAL RESULTS")
    print("=" * 80)

    for metric in metric_columns:

        if metric in dataframe:

            score = dataframe[
                metric
            ].mean()

            print(
                f"{metric}: {score:.4f}"
            )

    # -------------------------------------------------
    # Save CSV
    # -------------------------------------------------

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataframe.to_csv(
        FINAL_RESULTS_FILE,
        index=False,
        encoding="utf-8",
    )

    print("\n")
    print("=" * 80)
    print("RESULTS SAVED")
    print("=" * 80)

    print(
        f"File: {FINAL_RESULTS_FILE}"
    )


# =====================================================
# Entry Point
# =====================================================

if __name__ == "__main__":

    asyncio.run(
        run_evaluation()
    )