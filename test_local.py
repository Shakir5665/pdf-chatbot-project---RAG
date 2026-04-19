import os
from dotenv import load_dotenv

# Grab the secret keys from the .env file
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

# Check if the API key is correctly spotted by the code
if api_key:
    print("✅ OpenAI API key found")
else:
    print("❌ API key missing - check .env file")
    
# Check if the LangChain library for OpenAI was installed successfully
try:
    from langchain_openai import ChatOpenAI, OpenAIEmbeddings
    print("✅ LangChain OpenAI package installed")
except ImportError as e:
    print(f"❌ LangChain OpenAI package missing: {e}")
    
# Check if the web server module (Streamlit) was installed successfully
try:
    import streamlit
    print("✅ Streamlit installed")
except:
    print("❌ Streamlit missing")

# Tell the user they can start the app now
print("\n🎯 Ready to run! Use: streamlit run app.py")