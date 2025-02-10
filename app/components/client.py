# client.py
import os
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv

def llm():
    # Load LLM API Key
    load_dotenv()
    api_key = os.getenv("LLM_API_KEY")

    # Return LLM Model
    return ChatOpenAI(
        model="deepseek/deepseek-r1:free",
        openai_api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )