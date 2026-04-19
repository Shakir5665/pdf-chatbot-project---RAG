import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    

    # PDF Processing
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    RETRIEVAL_K = 4
    
    # Gemini Model Settings
    CHAT_MODEL = "gemini-2.0-flash"  # For chat/QA
    
    # ← FIXED: Correct embedding model names
    # Option 1: Use the latest embedding model (RECOMMENDED)
    EMBEDDING_MODEL = "models/gemini-embedding-001"  # ← Updated
    
    # Option 2: Alternative if above doesn't work
    # EMBEDDING_MODEL = "models/embedding-gecko-001"  # Older model
    
    # Option 3: Latest model with better performance
    # EMBEDDING_MODEL = "models/text-embedding-005"  # Latest as of 2025
    
    TEMPERATURE = 0.3
    MAX_OUTPUT_TOKENS = 500
    
    # File Paths
    VECTOR_STORE_PATH = "./vector_store"
    UPLOAD_PATH = "./uploads"
    
    # Performance
    BATCH_SIZE = 50