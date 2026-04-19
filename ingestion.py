import os
from typing import List, Tuple
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
import streamlit as st
from config import Config

class PDFIngestor:
    def __init__(self):
        """Initialize the PDF ingestor to prepare files for the AI"""
        try:
            # Create the embedding tracker to turn words into numbers (vectors)
            self.embeddings = OpenAIEmbeddings(
                model=Config.EMBEDDING_MODEL,
                api_key=Config.OPENAI_API_KEY,
            )
            st.success(f"✅ Using embedding model: {Config.EMBEDDING_MODEL}")
        except Exception as e:
            # Let the user know if the API Key or model is broken
            st.error(f"Failed to initialize embeddings: {str(e)}")
            raise
            
        # Tool to slice big pages into smaller paragraphs so the AI can read them easily
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Create storage folders on the computer if they don't exist yet
        os.makedirs(Config.VECTOR_STORE_PATH, exist_ok=True)
        os.makedirs(Config.UPLOAD_PATH, exist_ok=True)
        
    def load_pdf(self, pdf_path: str) -> List[Document]:
        """Reads the PDF file and turns it into readable text pages"""
        try:
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            st.info(f"📄 Loaded {len(documents)} pages")
            return documents
        except Exception as e:
            st.error(f"Error loading PDF: {str(e)}")
            return []
            
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """Cuts the big pile of pages into smaller piece-sized chunks"""
        chunks = self.text_splitter.split_documents(documents)
        st.info(f"✂️ Created {len(chunks)} chunks")
        return chunks
        
    def create_vector_store(self, chunks: List[Document], filename: str) -> FAISS:
        """Converts the text chunks into math vectors and saves them to a local database"""
        try:
            # This takes time, so show a loading spinner
            with st.spinner("Generating embeddings (this may take a moment)..."):
                vector_store = FAISS.from_documents(chunks, self.embeddings)
                
            # Figure out where to save the database on the hard drive
            store_path = os.path.join(Config.VECTOR_STORE_PATH, filename.replace('.pdf', ''))
            vector_store.save_local(store_path)
            st.success(f"💾 Vector store saved to {store_path}")
            return vector_store
        except Exception as e:
            st.error(f"Error creating vector store: {str(e)}")
            st.error("Try using a different embedding model in config.py")
            return None
            
    def load_vector_store(self, filename: str) -> FAISS:
        """Tries to load an old database if we already processed this PDF before"""
        try:
            store_path = os.path.join(Config.VECTOR_STORE_PATH, filename.replace('.pdf', ''))
            vector_store = FAISS.load_local(
                store_path, 
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            return vector_store
        except:
            return None
            
    def process_pdf(self, pdf_path: str) -> Tuple[FAISS, List[Document]]:
        """The main boss function that runs all the steps automatically: Load -> Cut -> Save"""
        with st.spinner("📖 Loading PDF..."):
            documents = self.load_pdf(pdf_path)
            if not documents:
                return None, None
                
        with st.spinner("✂️  Splitting into chunks..."):
            chunks = self.chunk_documents(documents)
            
        with st.spinner("🔢 Creating vector database with OpenAI embeddings..."):
            vector_store = self.create_vector_store(chunks, os.path.basename(pdf_path))
            
        return vector_store, chunks