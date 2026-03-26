# Layer 1 — Just connect to the model
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate

MODEL_NAME = "mistral:7b"

llm = ChatOllama(
    model=MODEL_NAME,
    temperature=0  # 0 = focused, deterministic responses, 1 = creative, random responses
)
chat_history=[]
def chat_bot(user_input: str)->str:
    prompt=ChatPromptTemplate.from_messages([
        ("system", "You are an expert AI assistant."),
        *[(chat_msg["role"], chat_msg["content"]) for chat_msg in chat_history],
        ("human","{input}")

    ])
    chain=prompt | llm
    response = chain.invoke({"input": user_input})
    #save to history
    chat_history.append({"role":"human", "content": user_input}),
    chat_history.append({"role":"assistant", "content": response.content})
    return response.content
print("*"*20)
print(chat_bot("My name is Narendra."))
print("*"*20)
print(chat_bot("What is my name ?"))
