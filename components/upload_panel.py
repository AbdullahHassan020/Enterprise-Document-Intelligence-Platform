import os
import streamlit as st

from utils.loader import load_document
from utils.chunker import create_chunks
from utils.embeddings import generate_embeddings
from utils.vectordb import (
    store_embeddings,
    total_documents
)

UPLOAD_FOLDER = "data/uploads"


def upload_panel():

    st.sidebar.markdown("---")
    st.sidebar.subheader("📂 Upload Documents")

    os.makedirs(
        UPLOAD_FOLDER,
        exist_ok=True
    )

    uploaded_files = st.sidebar.file_uploader(
        "Upload PDF, TXT or Markdown",
        type=["pdf", "txt", "md"],
        accept_multiple_files=True
    )

    if uploaded_files:

        progress = st.sidebar.progress(0)

        total = len(uploaded_files)

        for index, uploaded_file in enumerate(uploaded_files):

            save_path = os.path.join(
                UPLOAD_FOLDER,
                uploaded_file.name
            )

            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # --------------------------
            # Load document
            # --------------------------

            document = load_document(
                save_path
            )

            # --------------------------
            # Chunk text
            # --------------------------

            chunks = create_chunks(
                document["text"]
            )

            # --------------------------
            # Embeddings
            # --------------------------

            embeddings = generate_embeddings(
                chunks
            )

            # --------------------------
            # Store
            # --------------------------

            store_embeddings(
                document["filename"],
                chunks,
                embeddings
            )

            progress.progress(
                (index + 1) / total
            )

            st.sidebar.success(
                f"✅ {document['filename']} indexed"
            )

        st.sidebar.success(
            "🎉 Documents indexed successfully."
        )

    st.sidebar.markdown("---")

    st.sidebar.metric(
        "Stored Chunks",
        total_documents()
    )