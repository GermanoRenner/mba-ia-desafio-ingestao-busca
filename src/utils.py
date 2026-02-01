import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_openai import OpenAIEmbeddings, ChatOpenAI


def embedding_factory(kind: str = "gemini"):
    if kind == "gemini":
        return GoogleGenerativeAIEmbeddings(model=os.getenv("GOOGLE_EMBEDDING_MODEL"), 
                                        google_api_key=os.getenv("GOOGLE_API_KEY"))
    elif kind == "openai":
        return OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL"))
    else:
        raise ValueError(f"Embedding kind {kind} not supported")


def llm_factory(kind: str = "gemini"):
    if kind == "gemini":
        return ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
    elif kind == "openai":
        return ChatOpenAI(model="gpt-5-nano")
    else:
        raise ValueError(f"LLM kind {kind} not supported")