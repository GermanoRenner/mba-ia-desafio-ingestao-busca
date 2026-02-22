import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_openai import OpenAIEmbeddings, ChatOpenAI


def embedding_factory():
    provider = os.getenv("MODEL_PROVIDER", "gemini")
    if provider == "gemini":
        return GoogleGenerativeAIEmbeddings(model=os.getenv("GOOGLE_EMBEDDING_MODEL"), 
                                        google_api_key=os.getenv("GOOGLE_API_KEY"))
    elif provider == "openai":
        return OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL"))
    else:
        raise ValueError(f"Embedding provider {provider} not supported")


def llm_factory():
    provider = os.getenv("MODEL_PROVIDER", "gemini")
    if provider == "gemini":
        return ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
    elif provider == "openai":
        return ChatOpenAI(model="gpt-5-nano")
    else:
        raise ValueError(f"LLM provider {provider} not supported")