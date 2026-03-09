import logging
from typing import List, Any, Optional
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from config import VECTORSTORE_DIR, OPENAI_API_KEY

logger = logging.getLogger(__name__)

def get_retriever() -> Optional[Any]:
    """
    Returns the configured retriever for the vector store.
    
    Returns:
        Optional[Any]: A LangChain retriever instance, or None if configuration fails.
    """
    if not OPENAI_API_KEY:
        logger.critical("OPENAI_API_KEY is not set. Cannot configure retriever.")
        return None

    try:
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=OPENAI_API_KEY
        )
        vectorstore = Chroma(
            persist_directory=VECTORSTORE_DIR, 
            embedding_function=embeddings
        )
        
        # Configure retriever for top 4 similarity search matches
        return vectorstore.as_retriever(search_kwargs={"k": 4})
    except Exception as e:
        logger.error("Error configuring retriever: %s", e)
        return None

def retrieve_code(query: str) -> List[Document]:
    """
    Retrieves the most relevant code chunks for a given query.
    
    Args:
        query (str): The search query.
        
    Returns:
        List[Document]: Associated retrieved documents.
    """
    retriever = get_retriever()
    if not retriever:
        logger.warning("Retriever unavailable for query: %s", query)
        return []
        
    try:
        results = retriever.invoke(query)
        logger.info("Retrieved %d document chunks for query.", len(results))
        return results
    except Exception as e:
        logger.error("Error retrieving code chunks: %s", e)
        return []
