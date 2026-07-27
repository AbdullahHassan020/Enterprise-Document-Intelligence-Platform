import time
import streamlit as st

from utils.vectordb import total_documents
from utils.openrouter import ask_ai
from utils.retriever import retrieve_chunks
from components.templates import TEMPLATES


def chat_interface(messages, system_prompt, model, template):

    # ----------------------------------------
    # Display Previous Messages
    # ----------------------------------------

    for msg in messages:

        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ----------------------------------------
    # Chat Input
    # ----------------------------------------

    prompt = st.chat_input(
        "Ask anything about your uploaded documents..."
    )

    if not prompt:
        return

    prompt = prompt.strip()

    if len(prompt) == 0:
        return

    if template != "None":

        prompt = (
            TEMPLATES[template]
            + prompt
        )

    # ----------------------------------------
    # Show User Message
    # ----------------------------------------

    with st.chat_message("user"):

        st.markdown(prompt)

    messages.append(

        {
            "role": "user",
            "content": prompt
        }

    )

    # ----------------------------------------
    # Retrieve Relevant Chunks
    # ----------------------------------------

    retrieved_chunks = retrieve_chunks(
        prompt,
        top_k=10
    )

    # -----------------------------
    # DEBUG
    # -----------------------------

    st.sidebar.markdown("---")
    st.sidebar.subheader("🔎 Retrieval Debug")

    st.sidebar.write(
    f"Retrieved Chunks: {len(retrieved_chunks)}"
    )

    if retrieved_chunks:

     for i, chunk in enumerate(retrieved_chunks, start=1):

        st.sidebar.write(f"Chunk {i}")

        st.sidebar.caption(
            chunk["source"]
        )

        st.sidebar.code(
            chunk["text"][:250]
        )

    # ----------------------------------------
    # Build Context
    # ----------------------------------------

    context = ""

    for chunk in retrieved_chunks:

        context += f"""

Document:
{chunk["source"]}

Content:
{chunk["text"]}

"""

    # ----------------------------------------
    # Enterprise RAG Prompt
    # ----------------------------------------

    rag_prompt = f"""
You are an Enterprise Document Intelligence Assistant.

Your job is to answer ONLY using the uploaded document context.

Rules:

1. If the answer exists in the document,
answer naturally.

2. Never invent information.

3. If the answer is missing from the uploaded documents,
reply ONLY:

I couldn't find that information in the uploaded documents.

4. Do NOT use your own knowledge unless the user explicitly asks for an explanation beyond the document.

5. Keep answers clean and professional.

==============================
DOCUMENT CONTEXT
==============================

{context}

==============================
QUESTION
==============================

{prompt}
"""

    # ----------------------------------------
    # Build Messages
    # ----------------------------------------

    llm_messages = [

        {
            "role": "system",
            "content": system_prompt
        }

    ]

    llm_messages.extend(

        st.session_state.memory.get()

    )

    llm_messages.append(

        {
            "role": "user",
            "content": rag_prompt
        }

    )

    # ----------------------------------------
    # Assistant Response
    # ----------------------------------------

    with st.chat_message("assistant"):

        placeholder = st.empty()

        placeholder.markdown(
            "🤖 *Thinking...*"
        )

        start = time.time()

        try:

            answer = ask_ai(
                llm_messages,
                model
            )

        except Exception:

            answer = """
❌ Unable to contact the AI model.

Possible reasons:

- Daily OpenRouter free limit reached.
- Internet connection issue.
- OpenRouter server unavailable.

Please try again later.
"""

        elapsed = time.time() - start

        placeholder.markdown(answer)

        st.caption(
            f"Response Time: {elapsed:.2f} sec"
        )

    # ----------------------------------------
    # Save Memory
    # ----------------------------------------

    st.session_state.memory.add(
        "user",
        prompt
    )

    st.session_state.memory.add(
        "assistant",
        answer
    )

    # ----------------------------------------
    # Save Chat
    # ----------------------------------------

    messages.append(

        {
            "role": "assistant",
            "content": answer
        }

    )