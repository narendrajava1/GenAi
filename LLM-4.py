from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

template_str: str = (
    "You are an expert AI assistant.\n"
    "Use ONLY the user provided context to answer the user's question. "
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
# sample context
sample_context: str = (
    "Nara Chandrababu Naidu, commonly known as CBN, was born on 20 April 1950.\n"
    "He is currently serving as the Chief Minister of Andhra Pradesh since 2024 and holds the record of longest-serving Chief Minister in the political history of Telugu states.\n"
    "He is the national president of the Telugu Desam Party (TDP)\n"
    "He obtained his B.A. degree in 1972 from Sri Venkateswara Arts College, Tirupati, then earned a master's degree in Economics from Sri Venkateswara University. "
    "Although he aspired to complete a Ph.D., it remained unfulfilled as he moved into politics."
    "Naidu began his political journey as a confidant of Sanjay Gandhi and was elected to the Andhra Pradesh state legislative assembly in 1978."
    "He later joined the TDP, founded by his father-in-law N. T. Rama Rao (NTR). ")

sample_user_query: str = "Who is the Chief Minister of AP?"
template = PromptTemplate.from_template(template_str)
template_value = template.format(context_str=sample_context, query_str=sample_user_query)
MODEL_NAME="mistral:7b"
llm=ChatOllama(
        model=MODEL_NAME,
        temperature=0  # 0 = focused, deterministic responses, 1 = creative, random responses
)
response = llm.invoke(template_value)
print(response.content)
