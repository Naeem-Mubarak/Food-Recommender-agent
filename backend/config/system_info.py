from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from groq import AsyncGroq
import os

load_dotenv()

def Gemini_model_provider():

    try:

        model=ChatGoogleGenerativeAI(
            model='gemini-3.5-flash',
            thinking_level="low",
            temperature=0.2
            )
        return model
    
    except Exception as e:
        
        print(f"Failed to load the model check your API key quota limit or there might be some other issue \n Error Details : {e}")


# DB path information so always use same DB
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PROJECT_ROOT, "database", "food_agent.db")


# Groq model provider
def Groq_client_provider():

    try:

        groq_client = AsyncGroq(
            api_key=os.getenv('GROQ_API_KEY')
            )
        return groq_client

    except Exception as e:

        print(f"Some Unexpected Error occur. \n Error Details: {e}")
        return None


# DB connection
def DB_connection_provider():

    try:

        DB_URL=os.getenv('DATABASE_URL')
        return DB_URL
    
    except Exception as e:

        print(f"Some unexpected Error occured during making DB connection \n Error Details : {e}")
        return None