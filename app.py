import streamlit as st
import os
import tempfile
from datetime import datetime
from ingestion import PDFIngestor
from chatbot import PDFChatbot
from config import Config

# Page configuration
st.set_page_config(
    page_title="PDF Chatbot - RAG with LangChain",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .css-1d391kg {
        background-color: #f0f2f6;
    }
    .source-text {
        font-size: 0.8rem;
        color: #666;
        background-color: #f9f9f9;
        padding: 0.5rem;
        border-radius: 0.3rem;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "chatbot" not in st.session_state:
    st.session_state.chatbot = None
if "current_pdf" not in st.session_state:
    st.session_state.current_pdf = None
if "processing_complete" not in st.session_state:
    st.session_state.processing_complete = False

# Title
st.title("📚 PDF Chatbot with RAG Architecture")
st.caption("Powered by LangChain, FAISS, and GPT-3.5 Turbo")

# Sidebar for PDF upload
with st.sidebar:
    st.header("📄 Document Management")
    
    # PDF Upload
    uploaded_file = st.file_uploader(
        "Upload PDF Document",
        type=["pdf"],
        help="Upload a PDF to start asking questions about its content"
    )
    
    if uploaded_file and (st.session_state.current_pdf != uploaded_file.name):
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        
        # Process PDF
        if st.button("🔄 Process PDF", type="primary"):
            ingestor = PDFIngestor()
            vector_store, chunks = ingestor.process_pdf(tmp_path)
            
            if vector_store:
                st.session_state.vector_store = vector_store
                st.session_state.chatbot = PDFChatbot(vector_store)
                st.session_state.current_pdf = uploaded_file.name
                st.session_state.processing_complete = True
                st.session_state.messages = []  # Clear chat history
                
                st.success(f"✅ Successfully processed PDF!")
                st.info(f"📊 Created {len(chunks)} text chunks for retrieval")
                
                # Clean up temp file
                os.unlink(tmp_path)
            else:
                st.error("❌ Failed to process PDF. Please try again.")
    
    # Display current PDF status
    if st.session_state.processing_complete:
        st.success(f"📄 Active PDF: {st.session_state.current_pdf}")
        
        # Option to clear
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
    
    # Info section
    st.divider()
    with st.expander("ℹ️ How it works"):
        st.markdown("""
        1. **Upload PDF** - Your document is split into chunks
        2. **Create Embeddings** - Each chunk is converted to vectors
        3. **Store in FAISS** - Vectors are indexed for fast search
        4. **Ask Questions** - We find relevant chunks
        5. **Generate Answer** - GPT answers based on those chunks
        """)
    
    st.caption(f"🟢 System Ready | Model: {Config.CHAT_MODEL} (OpenAI)")

# Main chat interface
if not st.session_state.processing_complete:
    # Welcome screen
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://img.icons8.com/color/240/000000/pdf.png", width=150)
        st.markdown("## 👋 Welcome to PDF Chatbot!")
        st.markdown("""
        ### Get started:
        1. **Upload a PDF** using the sidebar on the left
        2. **Wait for processing** (takes ~30 seconds for 50 pages)
        3. **Start asking questions** about your document
        
        ### Example questions:
        - *What are the main topics discussed?*
        - *Summarize chapter 3*
        - *Find information about [specific concept]*
        """)
else:
    # Chat interface
    chat_container = st.container()
    
    with chat_container:
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Show sources for assistant messages
                if message["role"] == "assistant" and "sources" in message:
                    with st.expander("📖 View Sources"):
                        for i, source in enumerate(message["sources"], 1):
                            st.markdown(f"**Source {i}:**")
                            st.markdown(f"```\n{source['content']}\n```")
                            if 'page' in source['metadata']:
                                st.caption(f"📍 Page {source['metadata']['page']}")
                            st.divider()
    
    # Input for new question
    if prompt := st.chat_input("Ask a question about your PDF..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get response
        with st.chat_message("assistant"):
            with st.spinner("🔍 Searching PDF and generating answer..."):
                response = st.session_state.chatbot.ask(prompt)
                
                if response["success"]:
                    st.markdown(response["answer"])
                    
                    # Show sources
                    if response["sources"]:
                        with st.expander("📖 View Sources"):
                            for i, source in enumerate(response["sources"], 1):
                                st.markdown(f"**Source {i}:**")
                                st.markdown(f"```\n{source['content']}\n```")
                                st.caption(f"📍 Page {source['metadata'].get('page', 'N/A')}")
                                st.divider()
                    
                    # Save to history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response["answer"],
                        "sources": response["sources"]
                    })
                else:
                    st.error(response["answer"])

# Footer
st.divider()
st.caption("🚀 Built with LangChain | FAISS | OpenAI GPT-3.5 Turbo | Streamlit")