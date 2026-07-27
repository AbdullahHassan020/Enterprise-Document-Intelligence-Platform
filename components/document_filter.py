import streamlit as st
from utils.document_manager import list_documents


def document_filter():

    st.sidebar.markdown("---")
    st.sidebar.subheader("🔍 Search Scope")

    docs = list_documents()

    if len(docs) == 0:

        st.session_state.selected_document = None

        st.sidebar.info(
            "Upload documents to enable search."
        )

        return

    options = ["🌍 All Documents"]

    options.extend(
        [f"📄 {doc}" for doc in docs]
    )

    selected = st.sidebar.selectbox(
        "Search In",
        options
    )

    if selected == "🌍 All Documents":

        st.session_state.selected_document = None

    else:

        st.session_state.selected_document = selected.replace(
            "📄 ",
            ""
        )