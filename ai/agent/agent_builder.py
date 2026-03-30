from langchain_classic import hub
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_classic.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOllama, ChatOpenAI

from ai.tools.trade_tool import trade_calculator
from ai.tools.position_tool import position_size
from config.settings import USE_OLLAMA, OLLAMA_MODEL, OPENAI_MODEL


def build_agent():
    # ✅ Select model dynamically
    if USE_OLLAMA:
        llm = ChatOllama(
            model=OLLAMA_MODEL,
            temperature=0
        )
    else:
        llm = ChatOpenAI(
            model=OPENAI_MODEL,
            temperature=0
        )

    # ✅ Tools
    tools = [trade_calculator, position_size]

    # ✅ Standard ReAct prompt
    prompt = hub.pull("hwchase17/react")

    # ✅ Create agent
    agent = create_react_agent(llm, tools, prompt)

    # ✅ Executor

    memory = ConversationBufferMemory(return_messages=True)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True, # shows tool calls in terminal
        handle_parsing_errors=True
    )

    return agent_executor
# from langchain_classic.agents import create_openai_tools_agent, AgentExecutor
# from langchain_classic.memory import ConversationBufferMemory
# from langchain_openai import ChatOpenAI
#
# from ai.tools.trade_tool import trade_calculator
# from ai.tools.position_tool import position_size
#
# def build_agent():
#     llm = ChatOpenAI(
#         model="gpt-4o-mini",
#         temperature=0
#     )
#
#     tools = [trade_calculator, position_size]
#
#     memory = ConversationBufferMemory(return_messages=True)
#
#     agent = create_openai_tools_agent(llm, tools)
#
#     agent_executor = AgentExecutor(
#         agent=agent,
#         tools=tools,
#         memory=memory,
#         verbose=True
#     )
#
#     return agent_executor