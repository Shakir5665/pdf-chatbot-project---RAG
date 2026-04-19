# Quick test to verify everything works with OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Test 1: Check API key
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print("✅ OpenAI API key found")
else:
    print("❌ API key missing - check .env file")

# Test 2: Try importing OpenAI libraries
try:
    from langchain_openai import ChatOpenAI, OpenAIEmbeddings
    print("✅ LangChain OpenAI package installed")
except ImportError as e:
    print(f"❌ LangChain OpenAI package missing: {e}")

try:
    import streamlit
    print("✅ Streamlit installed")
except:
    print("❌ Streamlit missing")

print("\n🎯 Ready to run! Use: streamlit run app.py")