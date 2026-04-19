import streamlit as st
import os
import tempfile
from datetime import datetime
from ingestion import PDFIngestor
from chatbot import PDFChatbot
from config import Config

# --- Application Startup ---
# Set up the title and layout for the browser tab
st.set_page_config(
    page_title="PDF Chatbot - RAG with LangChain",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Cosmetic Design ---
# Inject tiny bits of CSS code to make the text bubbles look nice and modern
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

# --- Memory Setup ---
# Initialize the app's brain / memory so it doesn't forget things when you click a button
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
    
# --- Main Screen Design ---
# Create the big title on the main page
st.title("📚 PDF Chatbot with RAG Architecture")
st.caption("Powered by LangChain, FAISS, and GPT-3.5 Turbo")

# --- Left Sidebar Menu ---
with st.sidebar:
    st.header("📄 Document Management")
    
    # Create the drag-and-drop file uploader box
    uploaded_file = st.file_uploader(
        "Upload PDF Document",
        type=["pdf"],
        help="Upload a PDF to start asking questions about its content"
    )
    
    # If the user uploads a new PDF that we haven't seen yet
    if uploaded_file and (st.session_state.current_pdf != uploaded_file.name):
        
        # Save the uploaded file temporarily on the computer so we can read it
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
            
        # Draw the "Process PDF" button. When clicked, do the logic inside
        if st.button("🔄 Process PDF", type="primary"):
            
            # Start the ingestion pipeline (Loading and slicing the PDF text)
            ingestor = PDFIngestor()
            vector_store, chunks = ingestor.process_pdf(tmp_path)
            
            # If everything worked successfully, update our memory state
            if vector_store:
                st.session_state.vector_store = vector_store
                st.session_state.chatbot = PDFChatbot(vector_store)
                st.session_state.current_pdf = uploaded_file.name
                st.session_state.processing_complete = True
                
                # Delete old chat history since this is a brand new PDF
                st.session_state.messages = []  
                
                st.success(f"✅ Successfully processed PDF!")
                st.info(f"📊 Created {len(chunks)} text chunks for retrieval")
                
                # Throw away the temporary file to keep the computer clean
                os.unlink(tmp_path)
            else:
                st.error("❌ Failed to process PDF. Please try again.")
                
    # If the app successfully loaded a PDF, show a button to clear chat history
    if st.session_state.processing_complete:
        st.success(f"📄 Active PDF: {st.session_state.current_pdf}")
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
            
    st.divider()
    
    # An expandable section to teach the user how it works
    with st.expander("ℹ️ How it works"):
        st.markdown("""
        1. **Upload PDF** - Your document is split into chunks
        2. **Create Embeddings** - Each chunk is converted to vectors
        3. **Store in FAISS** - Vectors are indexed for fast search
        4. **Ask Questions** - We find relevant chunks
        5. **Generate Answer** - GPT answers based on those chunks
        """)
        
    st.caption(f"🟢 System Ready | Model: {Config.CHAT_MODEL} (OpenAI)")

# --- Chat Interface area ---
# If no PDF is loaded yet, tell the user to upload one
if not st.session_state.processing_complete:
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
# If the PDF is loaded, we can show the chat boxes
else:
    chat_container = st.container()
    
    with chat_container:
        # Loop over our memory to redraw all previous messages in the chat
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Only if the assistant sent the message, show the sources they used
                if message["role"] == "assistant" and "sources" in message:
                    with st.expander("📖 View Sources"):
                        for i, source in enumerate(message["sources"], 1):
                            st.markdown(f"**Source {i}:**")
                            st.markdown(f"```\n{source['content']}\n```")
                            if 'page' in source['metadata']:
                                st.caption(f"📍 Page {source['metadata']['page']}")
                            st.divider()
                            
    # Look for a typed chat message box appearing on the bottom
    if prompt := st.chat_input("Ask a question about your PDF..."):
        
        # Add the human's message to the memory
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Add the AI's response message logic
        with st.chat_message("assistant"):
            with st.spinner("🔍 Searching PDF and generating answer..."):
                
                # Ask the chatbot the user's question
                response = st.session_state.chatbot.ask(prompt)
                
                if response["success"]:
                    # Print out the text answer
                    st.markdown(response["answer"])
                    
                    # Print out the sources section
                    if response["sources"]:
                        with st.expander("📖 View Sources"):
                            for i, source in enumerate(response["sources"], 1):
                                st.markdown(f"**Source {i}:**")
                                st.markdown(f"```\n{source['content']}\n```")
                                st.caption(f"📍 Page {source['metadata'].get('page', 'N/A')}")
                                st.divider()
                                
                    # Remember the answer so we don't forget it the next time the screen updates
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response["answer"],
                        "sources": response["sources"]
                    })
                else:
                    # Inform the user if the AI couldn't answer
                    st.error(response["answer"])

st.divider()
st.caption("🚀 Built with LangChain | FAISS | OpenAI GPT-3.5 Turbo | Streamlit")