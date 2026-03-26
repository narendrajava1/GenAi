from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

MODEL_NAME = "mistral:7b"
llm=ChatOllama(
    model=MODEL_NAME,
    temperature=0.1
)

chat_history=[]

def chat_bot(user_input:str)->str:
    prompt=ChatPromptTemplate.from_messages([
        ("system", "You are an expert AI assistant."),
        *[(chat_msg["role"],chat_msg["content"]) for chat_msg in chat_history],
        ("human","{input}")
    ])

    chain=prompt | llm
    response = chain.invoke({"input": user_input})
    return response.content

def main ():
    print("*"*20)

    while True:
        user_input=input("Enter your input: ").strip()
        if not user_input:
            continue
        elif user_input.lower()=="exit":
            print("👋 Goodbye!")
            break
        elif user_input.lower()=="clear":
            chat_history.clear()
            print("Chat history cleared.")
            continue

        bot_response = chat_bot(user_input)
        print(bot_response)
        chat_history.append({"role": "human", "content": user_input})
        chat_history.append({"role": "assistant", "content": bot_response})
        print("*"*20)

if __name__ == "__main__":
    main()

# Step 2: Without *
# [
#     ("system", "You are helpful"),
#     [("human", "Hi"), ("ai", "Hello")],  # ❌ nested list
#     ("human", "{input}")
# ]
#
# 👉 ❌ WRONG structure
#
# Step 3: With *
# [
#     ("system", "You are helpful"),
#     ("human", "Hi"),
#     ("ai", "Hello"),
#     ("human", "{input}")
# ]