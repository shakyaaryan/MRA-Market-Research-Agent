from langchain_openrouter import ChatOpenRouter
import os

def get_llm() -> ChatOpenRouter:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is missing. Add it to your .env file.")

    model_name = os.getenv("OPENROUTER_MODEL", "deepseek/deepseek-v4.1-flash")
    return ChatOpenRouter(
        model=model_name,
        temperature=0.2,
        api_key=api_key,
    )