from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_ollama import ChatOllama

# ─────────────────────────────────────────
# 1. Few-shot examples
# ─────────────────────────────────────────
examples = [
    {
        "context": "Sachin Tendulkar was born on 24 April 1973 in Mumbai. He is a former Indian cricketer and is widely regarded as one of the greatest batsmen of all time. He retired from all forms of cricket in 2013.",
        "question": "When did Sachin Tendulkar retire?",
        "answer": (
            "Sachin Tendulkar retired from all forms of cricket in 2013.\n\n"
            "Sources: '...retired from all forms of cricket in 2013.'"
        )
    },
    {
        "context": "The Eiffel Tower is located in Paris, France. It was constructed between 1887 and 1889 as the entrance arch for the 1889 World's Fair. It stands 330 metres tall.",
        "question": "How tall is the Eiffel Tower?",
        "answer": (
            "The Eiffel Tower stands 330 metres tall.\n\n"
            "Sources: '...stands 330 metres tall.'"
        )
    },
    {
        "context": "The Amazon River is located in South America. It is the largest river by discharge volume of water in the world.",
        "question": "Where is the Amazon River located?",
        "answer": (
            "The Amazon River is located in South America.\n\n"
            "Sources: '...located in South America.'"
        )
    },
]

# ─────────────────────────────────────────
# 2. Example prompt template (single example format)
# ─────────────────────────────────────────
example_prompt = PromptTemplate(
    input_variables=["context", "question", "answer"],
    template=(
        "Context: {context}\n"
        "Question: {question}\n"
        "Answer: {answer}\n"
    )
)

# ─────────────────────────────────────────
# 3. Few-shot prompt template
# ─────────────────────────────────────────
few_shot_template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix=(
        "You are an expert AI assistant.\n"
        "Use ONLY the provided context to answer the question.\n"
        "If the context is insufficient, reply exactly: 'Not enough information.'\n\n"
        "Answering Rules:\n"
        "1) Be concise and precise (3–6 sentences).\n"
        "2) Use bullet points for lists.\n"
        "3) End with a 'Sources:' section with short snippets from the context.\n\n"
        "Here are some examples:\n"
    ),
    suffix=(
        "Now answer the following:\n\n"
        "Context: {context_str}\n"
        "Question: {query_str}\n"
        "Answer:"
    ),
    input_variables=["context_str", "query_str"]
)

# ─────────────────────────────────────────
# 4. Sample context and query
# ─────────────────────────────────────────
sample_context: str = (
    "Nara Chandrababu Naidu, commonly known as CBN, was born on 20 April 1950.\n"
    "He is currently serving as the Chief Minister of Andhra Pradesh since 2024 "
    "and holds the record of longest-serving Chief Minister in the political history of Telugu states.\n"
    "He is the national president of the Telugu Desam Party (TDP).\n"
    "He obtained his B.A. degree in 1972 from Sri Venkateswara Arts College, Tirupati, "
    "then earned a master's degree in Economics from Sri Venkateswara University.\n"
    "Naidu began his political journey as a confidant of Sanjay Gandhi and was elected "
    "to the Andhra Pradesh state legislative assembly in 1978.\n"
    "He later joined the TDP, founded by his father-in-law N. T. Rama Rao (NTR)."
)

sample_user_query: str = "Who is the Chief Minister of AP?"

# ─────────────────────────────────────────
# 5. Format the prompt and invoke LLM
# ─────────────────────────────────────────
formatted_prompt = few_shot_template.format(
    context_str=sample_context,
    query_str=sample_user_query
)

MODEL_NAME = "mistral:7b"
llm = ChatOllama(
    model=MODEL_NAME,
    temperature=0  # 0 = focused, deterministic responses
)

response = llm.invoke(formatted_prompt)
print(response.content)
