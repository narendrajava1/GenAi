# Import dependencies
from langchain_ollama import ChatOllama

MODEL_NAME="mistral:7b"
QUESTION="Act as a IAS officer Who is the Chief Minister of AP?"

def get_chat_response(question:str)->str:
    """Send question the LLM and get return the response."""
    try:
        chat=ChatOllama(
            model=MODEL_NAME,
            temperature=0 # 0 = focused, deterministic responses, 1 = creative, random responses
        )
        response=chat.invoke(question)
        return response.content # Extract just the text content from the response
    except ConnectionError:
        print("Connection error")
        return "Error: Unable to connect to the Ollama server. Please ensure it is running and accessible."
    except TimeoutError:
        print("Timeout error")
        return "Error: The request to the Ollama server timed out. Please try again later."
    except Exception as e:
        print(e)
        return f"An unexpected error occurred: {str(e)}"

if __name__=="__main__":
    response=get_chat_response(QUESTION)
    print(response)