import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

# ── Config ──────────────────────────────────────
MODEL_NAME = "mistral:7b"
SYSTEM_PROMPT = (
    "You are a helpful, friendly AI assistant. "
    "Answer questions clearly and concisely. "
    "If you don't know something, say 'I don't know' honestly."
)

# ── Load LLM (cached so it loads only once) ─────
@st.cache_resource
def load_llm() -> ChatOllama:
    return ChatOllama(model=MODEL_NAME, temperature=0.7)

# ── Get response from LLM ────────────────────────
def get_response(llm: ChatOllama, history: list, user_input: str) -> str:
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        *[(msg["role"], msg["content"]) for msg in history],
        ("human", "{input}")
    ])
    chain = prompt | llm
    try:
        response = chain.invoke({"input": user_input})
        return response.content
    except Exception as e:
        return f"❌ Error: {e}"

# ── Page Config ──────────────────────────────────
st.set_page_config(
    page_title="Q&A Chatbot",
    page_icon="🤖",
    layout="centered"
)

# ── Header ───────────────────────────────────────
st.title("🤖 Q&A Chatbot")
st.caption(f"Powered by Ollama · Model: `{MODEL_NAME}`")

# ── Sidebar ──────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")
    st.write(f"**Model:** {MODEL_NAME}")
    st.write("**Status:** 🟢 Running")

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("**How to use:**")
    st.markdown("- Type your question below")
    st.markdown("- Bot remembers the conversation")
    st.markdown("- Click 'Clear Chat' to reset")

# ── Initialize chat history ──────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Display chat history ─────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ── Handle user input ────────────────────────────
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Show user message
    with st.chat_message("human"):
        st.write(user_input)

    # Save user message
    st.session_state.messages.append({
        "role": "human",
        "content": user_input
    })

    # Get and show bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            llm = load_llm()
            response = get_response(llm, st.session_state.messages, user_input)
        st.write(response)

    # Save bot response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })