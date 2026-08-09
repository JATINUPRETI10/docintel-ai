from app.utils.langsmith_config import *

import os
import streamlit as st

from app.core.document_qa_service import DocumentQAService


# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="DocIntel AI",
    page_icon="📄",
    layout="wide",
)


# =====================================================
# Backend
# =====================================================

@st.cache_resource
def get_service():
    return DocumentQAService()


service = get_service()


# =====================================================
# Session State
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "document_indexed" not in st.session_state:
    st.session_state.document_indexed = False


# =====================================================
# Header
# =====================================================

st.title("📄 DocIntel AI")

st.write(
    "Chat with your PDF documents using Retrieval-Augmented Generation (RAG)."
)


# =====================================================
# Sidebar
# =====================================================

st.sidebar.header("📂 Document Upload")

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

pdf_path = None

if uploaded_file:

    os.makedirs("documents", exist_ok=True)

    pdf_path = os.path.join(
        "documents",
        uploaded_file.name
    )

    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.sidebar.success(f"Uploaded: {uploaded_file.name}")

    if st.sidebar.button("📥 Index Document"):

        with st.spinner("Indexing document..."):

            service.index_document(pdf_path)

        st.session_state.document_indexed = True

        st.sidebar.success("✅ Document indexed successfully!")

        st.toast("Document indexed successfully!")


if st.sidebar.button("🗑 Clear Chat"):

    st.session_state.messages = []

    st.rerun()

# =====================================================
# Developer Mode
# =====================================================

developer_mode = st.sidebar.toggle(
    "🛠 Developer Mode",
    value=False
)


# =====================================================
# Display Previous Chat
# =====================================================

# =====================================================
# Display Previous Chat
# =====================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if (
            developer_mode
            and message["role"] == "assistant"
            and "documents" in message
        ):

            with st.expander("📚 Retrieval Details"):

                for i, doc in enumerate(
                    message["documents"],
                    start=1
                ):

                    score = doc.get("score")

                    if score is None:
                        icon = "⚪"
                        label = "N/A"

                    elif score < 0.30:
                        icon = "🟢"
                        label = "Excellent"

                    elif score < 0.60:
                        icon = "🟡"
                        label = "Good"

                    else:
                        icon = "🔴"
                        label = "Weak"

                    st.markdown(f"### Chunk {i}")

                    st.markdown(f"**📄 Page:** {doc['page']}")

                    st.markdown(
                        f"**Retrieval Distance:** {icon} {score} ({label})"
                    )

                    st.code(doc["content"])

                    st.divider()
# =====================================================
# Chat
# =====================================================

question = st.chat_input(
    "Ask something about your document..."
)

if question:

    if not st.session_state.document_indexed:

        st.warning(
            "⚠ Please upload and index a document first."
        )

        st.stop()

    # ---------------- User ----------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

     with st.spinner("Thinking..."):

        try:

            result = service.ask(question)

            answer = result["answer"]

            documents = result["documents"]

            st.markdown(answer)

            if developer_mode:

                with st.expander("📚 Retrieval Details"):

                    st.info(
                        f"Retrieved {len(documents)} chunks"
                    )

                    for i, doc in enumerate(
                        documents,
                        start=1
                    ):

                        score = doc.get("score")

                        if score is None:
                            icon = "⚪"
                            label = "N/A"

                        elif score < 0.30:
                            icon = "🟢"
                            label = "Excellent"

                        elif score < 0.60:
                            icon = "🟡"
                            label = "Good"

                        else:
                            icon = "🔴"
                            label = "Weak"

                        st.markdown(f"### Chunk {i}")

                        st.markdown(
                            f"**📄 Page:** {doc['page']}"
                        )

                        st.markdown(
                            f"**Retrieval Distance:** {icon} {score} ({label})"
                        )

                        st.code(doc["content"])

                        st.divider()

        except Exception as e:

            answer = f"Error: {e}"

            documents = []

            st.error(answer)