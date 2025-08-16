from dotenv import load_dotenv
from config import GEMINI_API_KEY
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

llm_gemini_flash = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    api_key=GEMINI_API_KEY,
    temperature=0.6,
)

llm_gemini_pro = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    api_key=GEMINI_API_KEY,
    temperature=1,
)

google_embedding = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=GEMINI_API_KEY
)
