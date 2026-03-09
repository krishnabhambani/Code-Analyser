import os
import logging
from typing import List, Optional
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from config import VECTORSTORE_DIR, OPENAI_API_KEY

logger = logging.getLogger(__name__)

def ingest_documents(chunked_documents: List[Document]) -> Optional[Chroma]:
    """
    Accepts chunked documents and stores them in Chroma.
    Generates embeddings using text-embedding-3-small and persists locally.
    
    Args:
        chunked_documents (List[Document]): Processed and chunked documents.
        
    Returns:
        Optional[Chroma]: The instantiated vector store or None if ingestion fails.
    """
    logger.info("Starting ingestion of %d chunked documents...", len(chunked_documents))
    
    if not OPENAI_API_KEY:
        logger.critical("OPENAI_API_KEY is not set. Cannot ingest documents.")
        return None

    try:
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=OPENAI_API_KEY
        )
        
        if not os.path.exists(VECTORSTORE_DIR):
            os.makedirs(VECTORSTORE_DIR)
            logger.info("Created vectorstore directory at %s", VECTORSTORE_DIR)
            
        vectorstore = Chroma.from_documents(
            documents=chunked_documents, 
            embedding=embeddings, 
            persist_directory=VECTORSTORE_DIR
        )
        logger.info("Ingestion complete. Vector database populated and persisted locally.")
        return vectorstore
    except Exception as e:
        logger.error("An error occurred during document ingestion: %s", e)
        return None
