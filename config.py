import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    

    # PDF Processing
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    RETRIEVAL_K = 4
    
    # OpenAI Model Settings
    CHAT_MODEL = "gpt-3.5-turbo"  # For chat/QA
    
    # Embedding model
    EMBEDDING_MODEL = "text-embedding-3-small"
    
    TEMPERATURE = 0.3
    MAX_OUTPUT_TOKENS = 500
    
    # API Keys
    # Try to load from Streamlit Secrets first (for deployment), then fallback to local .env
    try:
        import streamlit as st
        OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
    except Exception:
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # File Paths
    VECTOR_STORE_PATH = "./vector_store"
    UPLOAD_PATH = "./uploads"
    
    # Performance
    BATCH_SIZE = 50