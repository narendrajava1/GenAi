from langchain_chroma import Chroma
from langchain_classic.chains.retrieval_qa.base import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_text_splitters import RecursiveCharacterTextSplitter

#Load LLM
llm = ChatOllama(model="mistral:7b", temperature=0.1)

# ── Prompt Template ───────────────────────────
RAG_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=(
        "You are an expert AI assistant.\n"
        "Use ONLY the context below to answer the question.\n"
        "If the answer is not in the context, say exactly: "
        "'Not enough information.'\n\n"
        "Context:\n{context}\n\n"
        "Question: {question}\n\n"
        "Answering Rules:\n"
        "1) Be concise and precise.\n"
        "2) Use bullet points for lists.\n"
        "3) End with Sources: section.\n\n"
        "Answer:"
    )
)
#Step:1
# LoadPDF
def load_docs(path:str):
    loader=PyPDFLoader(path)
    return loader.load()

#Step:2 Split
def split_docs(docs:list):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200 )
    return splitter.split_documents(docs)

#Step:3 create vector DB
def create_vectorstore(chunks:list):
    embeddings=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    #For Chroma Vector store
    # return Chroma.from_documents(
    #     documents=chunks,
    #     embedding=embeddings,
    #     persist_directory="./db"
    # )
    #Fast similarity search engine for embeddings
    return FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

def get_k(question:str):
    if len(question.split()) <5:
        return 2
    elif len(question.split()) <10:
        return 4
    else:
        return 6

#Step:4 create retriever RAG Query
def ask_question(vectorstore,question:str):
    retriever = vectorstore.as_retriever(search_kwargs={"k": get_k(question)})
    docs = retriever.invoke(question)

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = RAG_PROMPT.format(
        context=context,
        question=question
    )

    response = llm.invoke(prompt)

    return response.content, docs

