import streamlit as st
import logging
from typing import Optional
from utils.repo_loader import clone_repo
from utils.code_loader import load_code_files, chunk_code_documents
from ingest import ingest_documents
from chat import get_chat_chain, ask_question

# Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="AutoCode", page_icon="🤖", layout="wide")

st.title("AutoCode - AI Codebase Analyzer")
st.markdown("Analyze GitHub repositories and ask questions using an AI-powered RAG pipeline.")

# Session state initialization
if "vectorstore_ready" not in st.session_state:
    st.session_state.vectorstore_ready = False
if "chat_chain" not in st.session_state:
    st.session_state.chat_chain = None

# --- Section 1: Repository Ingestion ---
st.header("1. Ingest Repository")
repo_url = st.text_input("GitHub Repository URL", placeholder="https://github.com/username/repo")

if st.button("Analyze Repository"):
    if not repo_url:
        st.warning("Please enter a valid GitHub repository URL.")
    else:
        with st.spinner(f"Cloning and analyzing {repo_url} (this might take a few minutes)..."):
            try:
                # 1. Clone
                st.info("Cloning repository...")
                repo_path = clone_repo(repo_url)
                if not repo_path:
                    st.error("Failed to clone repository. Check URL or available space.")
                else:
                    # 2. Load
                    st.info("Loading source files...")
                    documents = load_code_files(repo_path)
                    
                    if not documents:
                        st.warning("No processable target files found in repository.")
                    else:
                        # 3. Chunk
                        st.info(f"Chunking {len(documents)} logic documents...")
                        chunked_docs = chunk_code_documents(documents)
                        
                        # 4. Ingest
                        st.info("Generating embeddings and writing to ChromaDB...")
                        vectorstore = ingest_documents(chunked_docs)
                        
                        if vectorstore:
                            st.success(f"Successfully processed repository! {len(chunked_docs)} chunks embedded.")
                            st.session_state.vectorstore_ready = True
                            
                            # 5. Initialize Chat Chain
                            chain = get_chat_chain()
                            if chain:
                                st.session_state.chat_chain = chain
                            else:
                                st.error("Failed to initialize conversational chain.")
                        else:
                            st.error("Failed to store vector embeddings. Check API keys.")
            except Exception as e:
                logger.error("Error during ingestion pipeline.", exc_info=True)
                st.error(f"An error occurred: {str(e)}")


# --- Section 2: Chat ---
st.header("2. Ask Questions")

# Disable chat if vectorstore isn't ready
disabled = not st.session_state.vectorstore_ready
question = st.text_input("Ask a question about the codebase", disabled=disabled, placeholder="e.g. 'Where is the login functionality implemented?'")

if st.button("Ask Question", disabled=disabled):
    if not question:
        st.warning("Please ask a valid question.")
    elif not st.session_state.chat_chain:
         st.error("Chat engine is not initialized. Please re-analyze the repository.")
    else:
        with st.spinner("Thinking..."):
            answer = ask_question(question, chain=st.session_state.chat_chain)
            st.markdown("### Answer")
            st.info(answer)

st.divider()
st.caption("AutoCode: Built with LangChain, Chroma DB, and OpenAI `gpt-4o-mini`")
