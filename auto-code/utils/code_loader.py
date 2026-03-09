import logging
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)

def load_code_files(repo_path: str) -> List[Document]:
    """
    Loads Python source code files from a repository directory.
    Uses LangChain GenericLoader and LanguageParser to recursively
    load all .py files and convert them into LangChain Documents
    with metadata including the file path.
    
    Args:
        repo_path (str): The local path to the repository.
        
    Returns:
        List[Document]: A list of LangChain Document objects containing the code.
    """
    try:
        logger.info("Initializing document loader for path: %s", repo_path)
        loader = GenericLoader.from_filesystem(
            repo_path,
            glob="**/*",
            suffixes=[".py"],
            parser=LanguageParser(language=Language.PYTHON, parser_threshold=500)
        )
        
        documents = loader.load()
        logger.info("Successfully loaded %d Python documents.", len(documents))
        return documents
    except Exception as e:
        logger.error("Error loading code files from %s: %s", repo_path, e)
        return []

def chunk_code_documents(documents: List[Document]) -> List[Document]:
    """
    Splits loaded code documents into chunks using RecursiveCharacterTextSplitter.
    Ensures code structure is preserved and chunks remain readable.
    
    Args:
        documents (List[Document]): The loaded code documents.
        
    Returns:
        List[Document]: A list of smaller, chunked documents.
    """
    try:
        logger.info("Chunking %d documents...", len(documents))
        python_splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.PYTHON,
            chunk_size=1000,
            chunk_overlap=200
        )
        
        chunks = python_splitter.split_documents(documents)
        logger.info("Successfully split into %d chunks.", len(chunks))
        return chunks
    except Exception as e:
        logger.error("Error chunking documents: %s", e)
        return []
