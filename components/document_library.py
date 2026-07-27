import streamlit as st

from utils.document_manager import (
    get_documents,
    delete_document
)


def document_library():

    st.sidebar.markdown("---")
    st.sidebar.subheader("📚 Document Library")

    documents = get_documents()

    if len(documents) == 0:

        st.sidebar.info(
            "No uploaded documents."
        )

        return

    for doc in documents:

        with st.sidebar.container():

            st.markdown(
                f"**📄 {doc['name']}**"
            )

            col1, col2 = st.columns([3, 1])

            with col1:

                st.caption(
                    f"{doc['chunks']} Chunks"
                )

                st.success("Indexed")

            with col2:

                if st.button(
                    "🗑",
                    key=doc["name"],
                    help="Delete document"
                ):

                    delete_document(
                        doc["name"]
                    )

                    st.rerun()

            st.markdown("---")