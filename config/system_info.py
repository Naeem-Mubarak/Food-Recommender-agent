from langchain_google_genai import ChatGoogleGenerativeAI
from groq import Groq
import os



model=ChatGoogleGenerativeAI(model='gemini-3.5-flash')
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PROJECT_ROOT, "Database", "food_agent.db")

STT_model=Groq(api_key=os.getenv('GROQ_API_KEY'))

DB_URL=os.getenv('DATABASE_URL')