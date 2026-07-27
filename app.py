import json
import streamlit as st

from components.document_filter import document_filter
from components.chat import chat_interface
from components.upload_panel import upload_panel
from components.document_library import document_library
from utils.memory import ConversationMemory
from utils.vectordb import total_documents

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Enterprise Document Intelligence Platform",
    page_icon="📚",
    layout="wide"
)

# --------------------------------------------------
# Session State
# --------------------------------------------------

if "all_chats" not in st.session_state:

    st.session_state.all_chats = {
        "Chat 1": []
    }

if "current_chat" not in st.session_state:

    st.session_state.current_chat = "Chat 1"

if "memory" not in st.session_state:

    st.session_state.memory = ConversationMemory(
        max_messages=10
    )

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("📚 Enterprise Document Intelligence Platform")

st.caption(
    "AI-powered Enterprise Retrieval-Augmented Generation (RAG) Workspace"
)

st.markdown(
    """
Ask questions over your uploaded documents using semantic search,
retrieval-augmented generation (RAG), and conversational AI.
"""
)

# --------------------------------------------------
# Dashboard Metrics
# --------------------------------------------------

messages = st.session_state.all_chats[
    st.session_state.current_chat
]

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "📄 Documents",
        len(__import__("os").listdir("data/uploads"))
        if __import__("os").path.exists("data/uploads")
        else 0
    )

with col2:

    st.metric(
        "🧩 Chunks",
        total_documents()
    )

with col3:

    st.metric(
        "💬 Messages",
        len(messages)
    )

with col4:

    st.metric(
        "🗂 Chats",
        len(st.session_state.all_chats)
    )

st.divider()

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.title("⚙️ AI Workspace")

st.sidebar.caption(
    "Enterprise Document Intelligence"
)

chat_names = list(
    st.session_state.all_chats.keys()
)

selected = st.sidebar.selectbox(
    "💬 Active Chat",
    chat_names,
    index=chat_names.index(
        st.session_state.current_chat
    )
)

st.session_state.current_chat = selected

if st.sidebar.button(
    "➕ New Chat",
    use_container_width=True
):

    new_chat = f"Chat {len(chat_names)+1}"

    st.session_state.all_chats[
        new_chat
    ] = []

    st.session_state.current_chat = new_chat

    st.session_state.memory.clear()

    st.rerun()

messages = st.session_state.all_chats[
    st.session_state.current_chat
]

# --------------------------------------------------
# AI Settings
# --------------------------------------------------

st.sidebar.markdown("---")

st.sidebar.subheader("🤖 AI Settings")

system_prompt = st.sidebar.text_area(
    "System Prompt",
    "You are a professional Enterprise Document Intelligence Assistant."
)

model = st.sidebar.selectbox(
    "LLM Model",
    [
        "openai/gpt-oss-20b:free"
    ]
)

template = st.sidebar.selectbox(
    "Prompt Template",
    [
        "None",
        "📝 Summarize Text",
        "💻 Explain Code",
        "💡 Generate Ideas",
        "✍ Rewrite Content",
        "🌍 Translate",
        "📧 Create Email",
        "🧠 Brainstorm"
    ]
)

# --------------------------------------------------
# Upload Documents
# --------------------------------------------------

upload_panel()

# --------------------------------------------------
# Document Library
# --------------------------------------------------

document_library()

# --------------------------------------------------
# Document Filter
# --------------------------------------------------

document_filter()

# --------------------------------------------------
# Chat Interface
# --------------------------------------------------

chat_interface(
    messages,
    system_prompt,
    model,
    template
)

# --------------------------------------------------
# Sidebar Actions
# --------------------------------------------------

st.sidebar.markdown("---")

st.sidebar.subheader("🛠 Workspace")

if st.sidebar.button(
    "🗑 Clear Current Chat",
    use_container_width=True
):

    st.session_state.all_chats[
        st.session_state.current_chat
    ] = []

    st.session_state.memory.clear()

    st.rerun()

if messages:

    st.sidebar.download_button(
        "📥 Export Chat",
        json.dumps(
            messages,
            indent=4
        ),
        file_name=f"{st.session_state.current_chat}.json",
        mime="application/json",
        use_container_width=True
    )

# --------------------------------------------------
# Workspace Statistics
# --------------------------------------------------

st.sidebar.markdown("---")

st.sidebar.subheader("📊 Workspace Statistics")

st.sidebar.write(
    f"📄 Documents : {len(__import__('os').listdir('data/uploads')) if __import__('os').path.exists('data/uploads') else 0}"
)

st.sidebar.write(
    f"🧩 Chunks : {total_documents()}"
)

st.sidebar.write(
    f"💬 Messages : {len(messages)}"
)

st.sidebar.write(
    f"🗂 Chats : {len(st.session_state.all_chats)}"
)

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown("---")

st.caption(
    """
Enterprise Document Intelligence Platform

Built with Streamlit • ChromaDB • Sentence Transformers • OpenRouter
"""
)