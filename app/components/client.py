# client.py
import os
from langchain_community.chat_models import ChatOpenAI
from dotenv import load_dotenv

def llm():
    # Load LLM API Key
    load_dotenv()
    api_key = os.getenv("LLM_API_KEY")

    # Return LLM Model
    return ChatOpenAI(
        model="deepseek/deepseek-r1:free",
        # model="openai/gpt-4o-mini",
        openai_api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )