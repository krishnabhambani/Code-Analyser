import sys
import logging
from utils.repo_loader import clone_repo
from utils.code_loader import load_code_files, chunk_code_documents
from ingest import ingest_documents
from chat import chat_loop

logger = logging.getLogger(__name__)

def main() -> None:
    """
    Main entry point for the auto-code AI Codebase Analyzer.
    Coordinates repository ingestion and the interactive chat loop.
    """
    print("Welcome to auto-code (AI Codebase Analyzer)!")
    
    try:
        # 1. Ask the user for a GitHub repository URL
        repo_url = input("\nEnter GitHub repo:\n").strip()
        if not repo_url:
            print("No URL provided. Exiting.")
            return

        # 2. Clone the repository
        print("\nCloning repository...")
        logger.info("User requested to clone repo: %s", repo_url)
        repo_path = clone_repo(repo_url)
        if not repo_path:
            logger.error("Failed to clone repository. Exiting.")
            print("Failed to clone repository.")
            return
        
        # 3. Load source code
        print("Loading files...")
        documents = load_code_files(repo_path)
        
        if not documents:
            logger.warning("No processable text files found in the repository %s.", repo_path)
            print("No processable text files found in the repository.")
            return
            
        # 4. Split into chunks
        print("Chunking documents...")
        chunked_docs = chunk_code_documents(documents)
            
        # 5. Generate embeddings and store them
        print("Ingesting into vector database...")
        vectorstore = ingest_documents(chunked_docs)
        if not vectorstore:
            logger.error("Failed to create the vector database.")
            print("Failed to store embeddings. Please check your API keys or logs.")
            return
        
        # 6. Start a chat interface
        logger.info("Entering chat interface.")
        chat_loop()

    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
    except Exception as e:
        logger.exception("A critical error occurred in main program flow: %s", e)
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()
