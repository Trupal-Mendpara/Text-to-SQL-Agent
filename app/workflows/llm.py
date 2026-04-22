import os
from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

llm_sql_generator = ChatGroq(
     model="openai/gpt-oss-120b"
)

llm_sql_planner = ChatGroq(
     model="openai/gpt-oss-120b"
)