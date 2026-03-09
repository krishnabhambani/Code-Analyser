# auto-code (AI Codebase Analyzer)

An AI-powered codebase analyzer using Retrieval Augmented Generation (RAG).
This enables users to input a GitHub repository URL and interactively ask questions about the codebase.

## Prerequisites
- Python 3.8+
- OpenAI API Key

## Installation

1. Clone or download this directory.
2. Create and activate a Python virtual environment:
   ```bash
   # Create the virtual environment
   python -m venv venv
   
   # Activate on Windows:
   .\venv\Scripts\activate
   
   # Activate on macOS/Linux:
   source venv/bin/activate
   ```
3. Install dependencies inside the virtual environment:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your OpenAI API Key:
   Rename `.env.example` to `.env` (or create a new `.env` file in the root directory) and add:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

### Run the UI (Recommended)
You can run the web interface using Streamlit:
```bash
streamlit run app.py
```

### Run the CLI
Alternatively, run the main terminal application:
```bash
python main.py
```

You will be prompted to either:
1. **Ingest a new repository**: Provide a GitHub URL to clone, process, and store its codebase into the local Chroma vector database.
2. **Chat**: Ask questions about the currently ingested codebase.
