# DocIntel AI

DocIntel AI is a document question-answering system built using Retrieval-Augmented Generation (RAG).

It allows users to upload a document, index its content into a vector database, and ask questions about the document through a Streamlit-based interface.

## Features

- PDF, DOCX, and TXT document loading
- Text splitting and chunking
- HuggingFace-based embeddings
- ChromaDB vector storage
- Semantic document retrieval
- Ollama + Llama 3 for local LLM inference
- Retrieval-Augmented Generation (RAG)
- Streamlit chat interface
- Developer Mode for viewing retrieved chunks
- Duplicate document indexing protection
- Input validation
- LangSmith tracing
- RAGAS-based evaluation
- Automated test suite using pytest

## Architecture

```text
                    DOCINTEL AI
                         |
                  Document Upload
                         |
                         v
                  Document Loader
                         |
                         v
                  Text Splitter
                         |
                         v
               HuggingFace Embeddings
                         |
                         v
                     ChromaDB
                         |
                    Retrieval
                         |
                         v
                    RAG Chain
                         |
                         v
                   Ollama / Llama 3
                         |
                         v
                    Final Answer
                         |
                         v
                  Streamlit Interface


```

## Installation

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd docintel-ai
```
2. Create a Virtual Environment
```bash
python -m venv venv
```
4. Activate the Virtual Environment
```bash
Windows PowerShell:
venv\Scripts\Activate.ps1
```
4. Install Dependencies
```bash
pip install -r requirements.txt
```
Ollama Setup

DocIntel AI uses Ollama with Llama 3 for local LLM inference.

Install the Llama 3 Model
ollama pull llama3
Verify the Model
```bash
ollama list
```
From the project root, run:
```bash
python -m streamlit run app/ui/streamlit_app.py
```
After starting the application, use the Streamlit interface to:

Upload a PDF document.
Click Index Document.
Ask questions about the uploaded document.
Enable Developer Mode to inspect retrieved chunks and retrieval distances.
Evaluation

DocIntel AI uses RAGAS to evaluate the RAG pipeline.

Run the evaluation with:
```bash

python -m evaluation.evaluation
```
The evaluation uses the following metrics:

Faithfulness
Answer Relevancy
Context Precision
Context Recall

Evaluation results are stored in:

evaluation/results/ragas_results.csv
Testing

The project uses pytest for automated testing.

Run the complete test suite:
```bash
python -m pytest tests -v
```

The tests cover:

Document loading
Text splitting
Embeddings
ChromaDB
Document indexing
Duplicate document protection
Retriever
LLM
RAG chain
Document QA service
Input validation
Technologies Used
Python
LangChain
Ollama
Llama 3
HuggingFace
BGE Embeddings
ChromaDB
Streamlit
RAGAS
LangSmith
Pytest
Current Status

The project currently includes:

Working RAG pipeline
Local LLM inference
Streamlit interface
Document indexing
Retrieval inspection
RAGAS evaluation
Automated testing
Input validation
Duplicate indexing protection
Future Improvements

Possible future improvements include:

Better answer grounding and refusal handling
Support for additional document formats
Improved retrieval/reranking
Streaming LLM responses
Conversation memory
Authentication
More extensive evaluation datasets
