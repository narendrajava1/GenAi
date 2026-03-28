No worries! I'll provide a sample PDF. Let's begin! 💪

---

# 🎯 Week 4 — RAG Mastery Plan

```
Day 1: Understand RAG theory deeply
Day 2: Build RAG with single PDF
Day 3: Build RAG with multiple PDFs
Day 4: Build RAG with a website
Day 5: Build a Company Knowledge Base
Day 6: Add Streamlit UI
Day 7: Polish + Deploy
```

---

# 📅 Day 1 — RAG Theory (Deep Dive)

## 🧠 What exactly is RAG?

As your **Senior Tech Lead**, let me explain it with a real world analogy:

```
❌ LLM WITHOUT RAG:
   Imagine a brilliant doctor who studied
   medicine 2 years ago and has NO access
   to your medical reports.

   You: "What's wrong with me based on my reports?"
   Doctor: "I don't have your reports, I can only
            guess based on general knowledge."

✅ LLM WITH RAG:
   Same doctor BUT now has your medical reports
   on the table in front of him.

   You: "What's wrong with me based on my reports?"
   Doctor: "Based on your report page 3,
            your cholesterol is high because..."
```

> **RAG = Giving the LLM YOUR documents as context before answering**

---

## 🔬 RAG Architecture (Full Picture)

```
┌─────────────────────────────────────────────┐
│           INDEXING PIPELINE                  │
│  (runs once when you upload documents)       │
│                                             │
│  📄 Documents                               │
│      ↓                                      │
│  ✂️  Chunking (split into small pieces)     │
│      ↓                                      │
│  🔢 Embeddings (convert text → numbers)     │
│      ↓                                      │
│  🗄️  Vector Store (store the numbers)       │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│           RETRIEVAL PIPELINE                 │
│  (runs every time user asks a question)      │
│                                             │
│  ❓ User Question                           │
│      ↓                                      │
│  🔢 Convert question → Embedding            │
│      ↓                                      │
│  🔍 Search Vector Store                     │
│  (find most similar chunks)                 │
│      ↓                                      │
│  📋 Retrieved Chunks                        │
│      ↓                                      │
│  🤖 LLM (question + chunks → answer)        │
│      ↓                                      │
│  ✅ Final Answer                            │
└─────────────────────────────────────────────┘
```

---

## 🔑 5 Core Concepts You MUST Understand

### 1️⃣ Document Loaders
> Reads your files and converts them into text

```python
# PDF Loader
from langchain_community.document_loaders import PyPDFLoader
loader = PyPDFLoader("your_file.pdf")
documents = loader.load()

# Each document has:
print(documents[0].page_content)  # The text
print(documents[0].metadata)      # {'page': 0, 'source': 'file.pdf'}
```

---

### 2️⃣ Text Splitter — Why split?

```
❌ Problem: PDF has 100 pages = 50,000 tokens
   LLM context window = 8,000 tokens
   You CANNOT send the whole PDF!

✅ Solution: Split into small chunks of ~500 tokens
   Then only send the RELEVANT chunks
```

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,      # each chunk = 500 characters
    chunk_overlap=50     # overlap to avoid losing context
)
chunks = splitter.split_documents(documents)
```

**chunk_overlap explained:**
```
Chunk 1: "Chandrababu Naidu was born in 1950. He studied"
Chunk 2: "He studied Economics at SVU. He joined politics"
          ↑↑↑↑↑↑↑↑↑↑↑
          overlapping part keeps context connected!
```

---

### 3️⃣ Embeddings — The Magic! 🪄

> Converts text into numbers (vectors) that capture **meaning**

```
"King"   → [0.2, 0.8, 0.1, 0.9, ...]
"Queen"  → [0.2, 0.8, 0.1, 0.8, ...]  ← similar to King!
"Pizza"  → [0.9, 0.1, 0.7, 0.2, ...]  ← very different!
```

Similar meaning = similar numbers = close in vector space!

```python
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="nomic-embed-text")
vector = embeddings.embed_query("Who is Chandrababu Naidu?")
print(vector[:5])  # [0.123, 0.456, 0.789, ...]
```

---

### 4️⃣ Vector Store — The Database

> Stores all embeddings and lets you search by similarity

```python
from langchain_community.vectorstores import FAISS

# Store chunks as vectors
vectorstore = FAISS.from_documents(chunks, embeddings)

# Search for relevant chunks
results = vectorstore.similarity_search("Who is CM of AP?", k=3)
# Returns top 3 most relevant chunks!
```

---

### 5️⃣ Retriever + LLM = RAG Chain

```python
retriever = vectorstore.as_retriever()

# User asks → retriever finds chunks → LLM answers
chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever
)
response = chain.invoke("Who is CM of AP?")
```

---

## 🔧 Setup for Day 2

### Update your `Pipfile`:
```toml
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
langchain = "*"
langchain-ollama = "*"
langchain-core = "*"
langchain-community = "*"
streamlit = "*"
pypdf = "*"
faiss-cpu = "*"

[dev-packages]

[requires]
python_version = "3.12"
```

Install:
```bash
pipenv install
```

### Pull embedding model:
```bash
ollama pull nomic-embed-text
ollama pull mistral:7b
```

---

## 📄 Sample PDF for Testing

Since you don't have a PDF, create `sample.txt` and we'll treat it as our document:

```python
# run this once to create a sample PDF
from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

content = """
Nara Chandrababu Naidu Profile

Nara Chandrababu Naidu, commonly known as CBN, was born on 20 April 1950.
He is currently serving as the Chief Minister of Andhra Pradesh since 2024.
He holds the record of longest-serving Chief Minister in the political history of Telugu states.
He is the national president of the Telugu Desam Party (TDP).

Education:
He obtained his B.A. degree in 1972 from Sri Venkateswara Arts College, Tirupati.
He earned a master degree in Economics from Sri Venkateswara University.

Political Career:
Naidu began his political journey as a confidant of Sanjay Gandhi.
He was elected to the Andhra Pradesh state legislative assembly in 1978.
He later joined the TDP, founded by his father-in-law N. T. Rama Rao (NTR).
He served as Chief Minister from 1995 to 2004.
In the 2024 elections, TDP made a comeback securing 164 seats.

Technology Vision:
During his tenure he was hailed as the Hi-tech Chief Minister.
He plans to launch India first drone taxis.
He aims to build 5.5 GW of data centers in Andhra Pradesh.
He partnered with IBM to skill 1 lakh youngsters in AI and cybersecurity.
"""

for line in content.split("\n"):
    pdf.cell(200, 10, txt=line, ln=True)

pdf.output("sample.pdf")
print("✅ sample.pdf created!")
```

Add `fpdf` to Pipfile and run this once to generate your test PDF.

---

## ✅ Day 1 Homework

Answer these questions **without looking**:

| Question | Answer |
|---|---|
| What does RAG stand for? | ? |
| Why do we split documents into chunks? | ? |
| What are embeddings? | ? |
| What does a vector store do? | ? |
| What is chunk_overlap and why is it needed? | ? |

---

## 🗓️ What's Coming Tomorrow

**Day 2** — We write the full code for:
```
📄 Single PDF → Chunks → Embeddings
→ FAISS Vector Store → Retriever
→ LLM → Answer
```

