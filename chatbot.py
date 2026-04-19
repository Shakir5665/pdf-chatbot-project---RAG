from langchain_openai import ChatOpenAI  # ← CHANGED
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from typing import Dict, Any
from config import Config

class PDFChatbot:
    def __init__(self, vector_store: FAISS):
        """Initialize chatbot with OpenAI LLM"""
        self.vector_store = vector_store
        
        # ← CHANGED: Initialize OpenAI instead of Gemini
        self.llm = ChatOpenAI(
            model=Config.CHAT_MODEL,
            api_key=Config.OPENAI_API_KEY,
            temperature=Config.TEMPERATURE,
            max_tokens=Config.MAX_OUTPUT_TOKENS
        )
        
        # Custom prompt template (same as before)
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""
You are an expert assistant that answers questions based ONLY on the provided PDF document.

CONTEXT FROM PDF:
{context}

USER QUESTION: {question}

INSTRUCTIONS:
1. Answer based SOLELY on the context above
2. If the answer isn't in the context, say "I cannot find this information in the uploaded PDF"
3. Be specific and quote relevant sections when helpful
4. Keep answers concise but complete (2-4 sentences typically)
5. If mentioning page numbers, use the metadata from context

YOUR ANSWER:
"""
        )
        
        # Create retrieval QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(
                search_kwargs={"k": Config.RETRIEVAL_K}
            ),
            chain_type_kwargs={"prompt": self.prompt_template},
            return_source_documents=True
        )
    
    def ask(self, question: str) -> Dict[str, Any]:
        """Ask a question and get answer with sources"""
        try:
            response = self.qa_chain.invoke({"query": question})
            
            # Extract source information
            sources = []
            for doc in response.get("source_documents", []):
                sources.append({
                    "content": doc.page_content[:200] + "...",
                    "metadata": doc.metadata
                })
            
            return {
                "answer": response["result"],
                "sources": sources,
                "success": True
            }
        except Exception as e:
            return {
                "answer": f"Error: {str(e)}",
                "sources": [],
                "success": False
            }