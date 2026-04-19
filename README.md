# 📚 PDF Chatbot - RAG Architecture

An intelligent, Retrieval-Augmented Generation (RAG) powered Chatbot that allows users to seamlessly converse with their PDF documents. The application is built using Python, Streamlit, LangChain, FAISS, and Google Gemini models.

## ✨ Features
- **PDF Ingestion & Processing**: Easily upload your PDF documents through a clean Streamlit interface.
- **Smart Chunking**: Automatically processes and splits documents into optimized text chunks using `RecursiveCharacterTextSplitter`.
- **Local Vector Search (FAISS)**: Uses FAISS to index and rapidly retrieve relevant document chunks based on semantic similarity without relying on external cloud vector databases.
- **Google Gemini Integration**: 
  - Embeddings generated using Google's `gemini-embedding-001`.
  - Accurate, context-aware conversational answers powered by `gemini-2.0-flash`.
- **Source Citation**: Transparently displays exact snippets and pages where the answers were derived from to ensure hallucination-free interactions.

## 🛠️ Tech Stack
- **User Interface**: [Streamlit](https://streamlit.io/)
- **LLM Orchestration**: [LangChain](https://www.langchain.com/)
- **LLM & Embeddings Provider**: [Google Gemini](https://ai.google.dev/)
- **Vector Store**: [FAISS CPU](https://github.com/facebookresearch/faiss)
- **PDF Parser**: `pypdf`

## 📂 Project Structure
```text
├── .env                   # Environment variables (requires GOOGLE_API_KEY)
├── app.py                 # Streamlit UI layout and main application logic
├── chatbot.py             # Chatbot module defining the Retrieval QA chain
├── config.py              # Application settings, LLM mapping, and constants
├── ingestion.py           # Document loader, text chunking logic, and indexing
├── requirements.txt       # Project Python dependencies
└── test_local.py          # Scripts for testing functionality locally without UI
```

## 🚀 Getting Started

### Prerequisites
- **Python 3.8+**
- **Google API Key**: Needed for embeddings and LLM generation. Get yours from [Google AI Studio](https://aistudio.google.com/app/apikey).

### Installation
1. **Navigate to the project directory**:
   ```bash
   cd path/to/your/project
   ```

2. **Create a virtual environment (Recommended)**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the root directory (if not already existing) and add your API key:
   ```env
   GOOGLE_API_KEY=your_api_key_here
   ```

### Usage
Start the Streamlit application by running:
```bash
streamlit run app.py
```
This command will open the interactive UI in your default web browser (usually at `http://localhost:8501`). Just upload your target PDF, click `Process PDF`, and start querying!

## ⚙️ Configuration & Customization
System behaviors, hyperparameters, and models can be easily tweaked inside `config.py`:
- **CHUNK_SIZE**: `1000` (Size of the parsed text splits)
- **CHUNK_OVERLAP**: `200` (Sliding overlap to prevent losing sentence contexts)
- **RETRIEVAL_K**: `4` (Number of document matches fetched to frame the answer)
- **CHAT_MODEL**: Switch the core reasoning engine (`gemini-2.0-flash` by default).

*Note: The application automatically creates `./uploads` and `./vector_store` fallback directories contextually to process data streams.*

## 🌐 Deployment

The easiest way to showcase and deploy this application is using **Streamlit Community Cloud**, which is free and tightly integrated with GitHub.

### Step-by-step Deployment Guide:
1. **Push your code to GitHub**:
   Upload this project folder to a new public or private GitHub repository. 
   *(Note: A `.gitignore` file has been added to the project. It safely hides your `.env` file and local data vectors so your API key is never exposed publicly!)*

2. **Log into Streamlit Community Cloud**:
   Navigate to [share.streamlit.io](https://share.streamlit.io/) and authorize it with your GitHub account.

3. **Configure the App**:
   - Click on the "**New app**" button.
   - Select your **Repository** and **Branch** (usually `main` or `master`).
   - For the **Main file path**, enter: `app.py`

4. **Add your API Key Securely**:
   - **Crucial step**: Before hitting deploy, click on "**Advanced settings...**".
   - Look for the **Secrets** section. Add your `GOOGLE_API_KEY` here (similar to the `.env` format):
     ```toml
     GOOGLE_API_KEY="your_actual_api_key_here"
     ```
   - Click "**Save**".

5. **Launch!**
   Click "**Deploy!**". Streamlit will automatically read your `requirements.txt`, install dependencies, and start the app. You'll shortly receive a public URL to share your showcase!
