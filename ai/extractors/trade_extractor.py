from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

from config.settings import USE_OLLAMA, OLLAMA_MODEL

# LLM setup
if USE_OLLAMA:
    from langchain_community.chat_models import ChatOllama
    llm = ChatOllama(model=OLLAMA_MODEL, temperature=0)
else:
    raise ValueError("Only Ollama supported in this setup")


class TradeInput(BaseModel):
    symbol: str
    lots: int = Field(gt=0)
    buy_price: float = Field(gt=0)
    sell_price: float = Field(gt=0)
    stop_loss: float = Field(gt=0)


parser = JsonOutputParser(pydantic_object=TradeInput)

# ✅ FIXED PROMPT (escaped JSON)
prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a strict financial data extractor.

Convert user query into JSON ONLY.

Format:
{{
  "symbol": "NIFTY 18000 CE",
  "lots": 2,
  "buy_price": 120,
  "sell_price": 150,
  "stop_loss": 100
}}

Rules:
- Do NOT explain anything
- Do NOT add extra text
- Only return valid JSON
- If missing values → estimate reasonably
"""),
    ("human", "{query}")
])


def extract_trade_data(query: str):
    try:
        chain = prompt | llm | parser
        return chain.invoke({"query": query})
    except Exception as e:
        raise ValueError(f"Extraction failed: {str(e)}")