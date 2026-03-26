from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

template_str: str = (
    "You are an expert AI assistant.\n"
    "Use ONLY the use provided context to answer the user's question. "
    "If the context is insufficient or does not mention the answer, reply exactly: "
    "'Not enough information.'\n\n"
    "Context:\n{context_str}\n\n"
    "User Question: {query_str}\n\n"
    "Answering Rules:\n"
    "1) Be concise and precise (3–6 sentences, unless the question requires more).\n"
    "2) Use bullet points for lists.\n"
    "3) At the end, include a 'Sources:' section with short snippets or filenames from the context you used.\n\n"
    "Final Answer:"
)
# sample usage

sample_context = (
    "Transformers use a self-attention mechanism that lets each token attend "
    "to every other token in the sequence. This enables modeling of long-range "
    "dependencies without recurrence. Positional encodings inject order "
    "information, and multi-head attention captures diverse relations.\n\n"
    "The encoder stacks layers of self-attention and feed-forward networks to "
    "build contextual representations. The decoder uses masked self-attention "
    "to maintain causality and cross-attention to consult encoder outputs."
)

sample_user_query = "what is used by the decoder?"
template = PromptTemplate.from_template(template_str)
template_value = template.format(context_str=sample_context, query_str=sample_user_query)
MODEL_NAME="mistral:7b"
llm=ChatOllama(
        model=MODEL_NAME,
        temperature=0  # 0 = focused, deterministic responses, 1 = creative, random responses
)
response = llm.invoke(template_value)
print(response.content)