import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REPOS_DIR = os.path.join(os.path.dirname(__file__), "repos")
VECTORSTORE_DIR = os.path.join(os.path.dirname(__file__), "vectorstore")
