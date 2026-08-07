import os
import streamlit as st

from app.core.document_qa_service import DocumentQAService


# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="DocIntel AI",
    page_icon="📄",
    layout="wide"
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
# Display Previous Messages
# =====================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant":

            if "sources" in message:

                with st.expander("📚 Sources"):

                    for source in message["sources"]:
                        st.write(f"📄 {source}")


# =====================================================
# Chat Input
# =====================================================

question = st.chat_input(
    "Ask something about your document..."
)


if question:

    if not st.session_state.document_indexed:

        st.warning("⚠ Please upload and index a document first.")

        st.stop()

    # ---------------- User Message ----------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    # ---------------- Assistant ----------------

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                result = service.ask(question)

                answer = result["answer"]

                sources = result["sources"]

                st.markdown(answer)

                with st.expander("📚 Sources"):

                    for source in sources:
                        st.write(f"📄 {source}")

            except Exception as e:

                answer = f"Error: {e}"

                sources = []

                st.error(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": sources
        }
    )