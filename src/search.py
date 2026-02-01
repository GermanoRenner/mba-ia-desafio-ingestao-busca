import os

from utils import embedding_factory, llm_factory
from langchain_postgres import PGVector

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def search_vector_db(query: str):
    embeddings = embedding_factory()
    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
    )

    result = store.similarity_search_with_score(query, k=10)
    concat_result = [f"{doc.page_content}\n" for doc, score in result]
    return "\n".join(concat_result)

def build_prompt(question: str):
    context = search_vector_db(question)
    return PROMPT_TEMPLATE.format(contexto=context, pergunta=question)
    

def search_prompt(question=None):
    llm = llm_factory()
    prompt = build_prompt(question)
    result = llm.invoke(prompt) 

    return result