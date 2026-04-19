from langchain_openai import ChatOpenAI  
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from typing import Dict, Any
from config import Config

class PDFChatbot:
    def __init__(self, vector_store: FAISS):
        """Initialize the chatbot by giving it the stored PDF data"""
        self.vector_store = vector_store
        
        # Set up our AI "brain" using the OpenAI details from config.py
        self.llm = ChatOpenAI(
            model=Config.CHAT_MODEL,
            api_key=Config.OPENAI_API_KEY,
            temperature=Config.TEMPERATURE,
            max_tokens=Config.MAX_OUTPUT_TOKENS
        )
        
        # This is the "prompt" (the secret instructions) we give to the AI
        # so it knows exactly how to answer the user's questions
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
        
        # Combine everything together into a chain: the retriever + the AI + the prompt
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
        """Takes a user question, searches the PDF, and generated an answer"""
        try:
            # Tell the AI chain to process the user's question
            response = self.qa_chain.invoke({"query": question})
            
            # Here we capture exactly where the AI found the information
            sources = []
            for doc in response.get("source_documents", []):
                sources.append({
                    "content": doc.page_content[:200] + "...",
                    "metadata": doc.metadata
                })
                
            # Return the answer and the sources nicely packaged
            return {
                "answer": response["result"],
                "sources": sources,
                "success": True
            }
        except Exception as e:
            # If something crashes, catch the error and tell the user
            return {
                "answer": f"Error: {str(e)}",
                "sources": [],
                "success": False
            }