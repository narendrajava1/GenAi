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
# sample usage

sample_context = (
    "NASA’s Artemis program aims to return humans to the Moon by the mid-2020s. "
    "Artemis I was an uncrewed test flight in 2022, successfully orbiting the Moon. "
    "Artemis II, scheduled for 2025, will carry astronauts on a lunar flyby. "
    "Artemis III, planned for 2026, aims to land the first woman and next man on the lunar surface. "
    "The program also intends to establish a sustainable presence by building a lunar Gateway space station "
    "and using the Moon as a stepping stone to Mars."
)

sample_user_query = "What are the main goals of the Artemis program?"
template = PromptTemplate.from_template(template_str)
template_value = template.format(context_str=sample_context, query_str=sample_user_query)
MODEL_NAME="mistral:7b"
llm=ChatOllama(
        model=MODEL_NAME,
        temperature=0  # 0 = focused, deterministic responses, 1 = creative, random responses
)
response = llm.invoke(template_value)
print(response.content)


def zero_shot_prompt(question):
    # Directly send the question without examples
    # You can wrap the question in a template if you want
    llm.invoke(question)
    return response.content


def few_shot_prompt(question):
    # Provide 2–3 examples before the actual question
    # You can also use a prompt template here
    return response


question = "Explain what a Large Language Model is in simple terms."
examples= "ChatGPT (OpenAI)"
print("Zero-shot:", zero_shot_prompt(question))
print("Few-shot:", few_shot_prompt(question))