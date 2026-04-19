import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    RETRIEVAL_K = 4
    CHAT_MODEL = "gpt-3.5-turbo"  
    EMBEDDING_MODEL = "text-embedding-3-small"
    TEMPERATURE = 0.3
    MAX_OUTPUT_TOKENS = 500
    try:
        import streamlit as st
        _api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
    except Exception:
        _api_key = os.getenv("OPENAI_API_KEY")
    OPENAI_API_KEY = _api_key
    if OPENAI_API_KEY:
        os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    VECTOR_STORE_PATH = "./vector_store"
    UPLOAD_PATH = "./uploads"
    BATCH_SIZE = 50