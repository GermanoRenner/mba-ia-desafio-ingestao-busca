import os
import logging
from dotenv import load_dotenv


from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_postgres import PGVector

from utils import embedding_factory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")

def ingest_pdf(pdf_path: str = PDF_PATH):
    document = PyPDFLoader(pdf_path).load()
    splits = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150).split_documents(document)
    enriched_splits = [
        Document(page_content=split.page_content, 
                metadata={k:v for k,v in split.metadata.items() if v not in ("", None)}
            ) 
        for split in splits
    ]
    ids = [f"doc{i}" for i in range(len(enriched_splits))]
    embeddings = embedding_factory()
    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
    )
    store.add_documents(documents=enriched_splits, ids=ids)

if __name__ == "__main__":
    logger.info("Starting PDF ingestion...")
    ingest_pdf()
    logger.info("PDF ingestion completed.")