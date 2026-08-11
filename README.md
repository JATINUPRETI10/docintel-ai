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
RAG Workflow
1. Document Loading

The uploaded document is processed using LangChain document loaders.

Supported formats:

PDF
DOCX
TXT
2. Text Splitting

Documents are divided into smaller chunks before embedding.

Current configuration:

Chunk Size: 500
Chunk Overlap: 100
3. Embedding

The project uses:

BAAI/bge-small-en-v1.5

to convert document chunks into vector representations.

4. Vector Storage

The embeddings are stored in ChromaDB.

The retriever uses semantic similarity to find relevant chunks for a user's question.

5. Retrieval-Augmented Generation

The retrieved chunks are passed to the RAG chain along with the user's question.

The LLM then generates the final response using the retrieved document context.

6. LLM

The project currently uses:

Ollama
└── llama3:latest

This allows the application to run LLM inference locally.

Evaluation

The project uses RAGAS to evaluate the quality of the RAG pipeline.

The following metrics are used:

Faithfulness
Answer Relevancy
Context Precision
Context Recall
Latest Evaluation Results
Metric	Score
Faithfulness	1.0000
Answer Relevancy	0.8817
Context Precision	0.9707
Context Recall	0.8971

These results were obtained from a 10-question evaluation dataset.

Testing

The project includes automated tests using pytest.

Latest test result:

14 passed

The test suite covers:

ChromaDB
Embeddings
Document indexing
LLM
Document loading
RAG chain
Retriever
Document QA service
Input validation
Text splitting
Duplicate document indexing

Run the tests with:

python -m pytest tests -v
Project Structure
docintel-ai/
│
├── app/
│   ├── chains/
│   ├── core/
│   ├── embeddings/
│   ├── factories/
│   ├── llm/
│   ├── loaders/
│   ├── prompts/
│   ├── retrieval/
│   ├── services/
│   ├── ui/
│   ├── utils/
│   └── vectorstore/
│
├── documents/
│
├── evaluation/
│   ├── evaluation.py
│   ├── collect_results.py
│   └── results/
│
├── tests/
│
├── chroma_db/
├── config.py
├── main.py
├── requirements.txt
└── README.md
Installation

Clone the repository:

git clone <YOUR_GITHUB_REPOSITORY_URL>
cd docintel-ai

Create a virtual environment:

python -m venv venv

Activate it on Windows:

venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt
Ollama Setup

Install Ollama and make sure the required model is available:

ollama pull llama3

Verify:

ollama list

The application is configured to use:

llama3:latest
Running the Application

From the project root:

python -m streamlit run app/ui/streamlit_app.py

The application will be available at:

http://localhost:8501
Using the Application
Open the Streamlit application.
Upload a PDF document.
Click Index Document.
Ask questions about the document.
Enable Developer Mode to inspect retrieved chunks and retrieval distances.
Evaluation

Run the RAGAS evaluation with:

python -m evaluation.evaluation

The evaluation results are stored in:

evaluation/results/ragas_results.csv
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

The project currently has:

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
Cloud deployment
More extensive evaluation datasets
