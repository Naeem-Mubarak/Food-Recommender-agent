from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()



model=ChatGoogleGenerativeAI(model='gemini-3.5-flash')
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PROJECT_ROOT, "Database", "food_agent.db")

groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))

DB_URL=os.getenv('DATABASE_URL')