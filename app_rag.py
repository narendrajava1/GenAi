from langchain_community.document_loaders import PyPDFLoader
import streamlit as st

from rag_pipeline import split_docs, create_vectorstore, ask_question, load_docs

# ── Page Config ───────────────────────────────
st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="📄",
    layout="wide"
)

#Load & Process PDF(run once)
@st.cache_resource
def setup():
    try:
        with st.spinner("📄 Loading PDF..."):
            documents = load_docs("./pdfs")

        with st.spinner(f"✂️ Splitting {len(documents)} page(s) into chunks..."):
            chunks = split_docs(documents)

        with st.spinner(f"🔢 Creating embeddings for {len(chunks)} chunks..."):
            vectorstore = create_vectorstore(chunks)

        return vectorstore, len(documents), len(chunks)

    except Exception as e:
        st.error(f"❌ Error loading PDF: {e}")
        st.stop()

# ── Header ────────────────────────────────────
st.title("📄 Chat with your PDF")
st.caption("Powered by LangChain + Ollama + FAISS")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])



#Chat UI
user_input=st.chat_input("Ask a question about the PDF:" )
if user_input:
    #show user input message
    with st.chat_message("human"):
        st.write(user_input)
    #save user messages
    st.session_state.messages.append({
        "role": "human",
        "content": user_input
    })

    #Got bot response
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):

            vectorstore, doc_count, chunk_count  = setup()
            response, docs = ask_question(vectorstore,user_input)
            st.chat_message("user").write(user_input)
            st.chat_message("assistant").write(response)
            if docs:
                with st.expander("📚 Source Documents"):
                    for doc in docs:
                        page = doc_count
                        source = doc.metadata.get("source", "Unknown")
                        st.markdown(
                            f"**Source:** {source} | **Page:** {page}  \n"
                            f"{doc.page_content[:200]}..."
                        )
            #save assistant response
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "sources": docs
            })
            # st.success(f"Loaded {doc_count} {'pages' if doc_count > 1 else 'page'}, {chunk_count} chunks")