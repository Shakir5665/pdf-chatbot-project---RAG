# Quick test to verify everything works with Gemini
import os
from dotenv import load_dotenv

load_dotenv()

# Test 1: Check API key
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    print("✅ Google Gemini API key found")
else:
    print("❌ API key missing - check .env file")

# Test 2: Try importing Gemini libraries
try:
    from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
    print("✅ LangChain Google GenAI package installed")
except ImportError as e:
    print(f"❌ LangChain Google package missing: {e}")

try:
    import streamlit
    print("✅ Streamlit installed")
except:
    print("❌ Streamlit missing")

print("\n🎯 Ready to run! Use: streamlit run app.py")