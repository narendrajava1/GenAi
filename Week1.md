Perfect! Here's your **personalized Gen AI roadmap** 🎯

---

## 🗺️ Your Learning Roadmap

```
Module 1: How LLMs Work (Theory)
         ↓
Module 2: Prompt Engineering
         ↓
Module 3: Build Chatbots with LangChain
         ↓
Module 4: RAG (Chat with Documents)
```

---

# 🧠 Module 1 — How LLMs Work

## What is an LLM?

**LLM = Large Language Model**

> A neural network trained on **billions of text documents** that learns to predict the next word — and becomes so good at it that it can answer questions, write code, summarize documents, and more.

---

## 🔑 3 Core Concepts

### 1️⃣ Tokens — How LLMs read text

LLMs don't read **words**, they read **tokens**.

```
"I love Python programming"
       ↓
["I", "love", "Python", "program", "ming"]
         5 tokens
```

> 1 token ≈ 0.75 words
> "ChatGPT" = 3 tokens: ["Chat", "G", "PT"]

**Why it matters:**
- Models have a **context window** (max tokens they can process)
- `mistral:7b` → ~8,000 tokens
- `GPT-4` → ~128,000 tokens

---

### 2️⃣ Temperature — How creative is the model?

```python
# Temperature = 0 → focused, deterministic
# "What is 2+2?" → "4" (always)
llm = ChatOllama(model="mistral:7b", temperature=0)

# Temperature = 1 → creative, random
# "What is 2+2?" → "4, but in another universe maybe 5!" 😄
llm = ChatOllama(model="mistral:7b", temperature=1)
```

| Temperature | Best for |
|---|---|
| 0 | Factual Q&A, code generation |
| 0.5 | Balanced responses |
| 0.7–1.0 | Creative writing, brainstorming |

---

### 3️⃣ Context Window — LLM's short term memory

```
┌─────────────────────────────┐
│       Context Window        │
│                             │
│  System Prompt              │
│  + Chat History             │
│  + Your Question            │
│  + Answer                   │
│                             │
│  Max: ~8000 tokens          │
└─────────────────────────────┘
```

> ⚠️ LLMs have **NO memory** between sessions.
> Every time you call the API, you must send the **full history** again.

---

# ✍️ Module 2 — Prompt Engineering

## What is a Prompt?

> A prompt is the **instruction you give to the LLM**. Better prompts = better answers.

---

## 4 Types of Prompting

### 1️⃣ Zero-Shot — Just ask directly
```python
prompt = "What is the capital of India?"
# No examples given
# Output: "New Delhi"
```

---

### 2️⃣ Few-Shot — Give examples first
```python
prompt = """
Q: Capital of France? A: Paris
Q: Capital of Japan?  A: Tokyo
Q: Capital of India?  A:
"""
# LLM learns the pattern from examples
# Output: "New Delhi"
```

---

### 3️⃣ System Prompt — Give the LLM a role
```python
system = "You are a doctor. Answer only health-related questions."
user   = "What is diabetes?"
# LLM stays in doctor role
```

---

### 4️⃣ Chain of Thought — Ask it to think step by step
```python
prompt = "Solve this step by step: If I have 10 apples and give 3 to Ram and 2 to Sita, how many are left?"
# Output:
# Step 1: Start with 10
# Step 2: Give 3 to Ram → 10-3 = 7
# Step 3: Give 2 to Sita → 7-2 = 5
# Answer: 5
```

---

# 🤖 Module 3 — Build Chatbots with LangChain

## What is LangChain?

```
Without LangChain:
  You → Raw API calls → LLM
  (handle prompts, memory, errors yourself)

With LangChain:
  You → LangChain → LLM
  (prompts, memory, chains all handled!)
```

## 3 Key Building Blocks

### 1️⃣ LLM — The brain
```python
from langchain_ollama import ChatOllama

llm = ChatOllama(model="mistral:7b", temperature=0.7)
response = llm.invoke("What is Python?")
print(response.content)
```

---

### 2️⃣ Prompt Template — The structure
```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{input}")
])
```

---

### 3️⃣ Chain — Connect them together
```python
# The | symbol connects prompt → llm
chain = prompt | llm
response = chain.invoke({"input": "What is Python?"})
print(response.content)
```

Think of it like a **pipe**:
```
Your Input → Prompt Template → LLM → Response
```

---

# 📄 Module 4 — RAG (Chat with Documents)

## What is RAG?

**RAG = Retrieval Augmented Generation**

> Instead of relying on the LLM's training data, you **give it your own documents** to answer from.

---

## Why RAG?

```
❌ Without RAG:
   "What does our company policy say about leave?"
   LLM: "I don't know your company policy."

✅ With RAG:
   Your PDF → RAG System → LLM reads it → Correct Answer!
```

---

## How RAG Works

```
Step 1: Load your documents (PDF, TXT, etc.)
         ↓
Step 2: Split into chunks
         ↓
Step 3: Convert to Embeddings (numbers)
         ↓
Step 4: Store in Vector Database
         ↓
Step 5: User asks a question
         ↓
Step 6: Find relevant chunks
         ↓
Step 7: Send chunks + question to LLM
         ↓
Step 8: LLM answers from YOUR document!
```

---

## 📅 Your Weekly Study Plan

| Week | Topic | Goal |
|---|---|---|
| **Week 1** | LLMs + Tokens + Temperature | Understand how LLMs think |
| **Week 2** | Prompt Engineering | Write better prompts |
| **Week 3** | LangChain Chatbot | Build terminal + Streamlit chatbot |
| **Week 4** | RAG | Chat with your own PDF |

---

## ✅ Your Homework for Week 1

Try this code and experiment with temperature:

```python
from langchain_ollama import ChatOllama

question = "Tell me a joke about Python programming"

# Try temperature 0
llm_focused = ChatOllama(model="mistral:7b", temperature=0)
print("Temperature 0:")
print(llm_focused.invoke(question).content)

print("\n" + "="*40 + "\n")

# Try temperature 1
llm_creative = ChatOllama(model="mistral:7b", temperature=1)
print("Temperature 1:")
print(llm_creative.invoke(question).content)
```

**Observe:** How different are the two answers? Run it 3 times and see!

---

# 🎉 Congratulations on completing Week 1!