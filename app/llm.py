import os
from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq

load_dotenv()
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")
os.environ["OLLAMA_API_KEY"] = os.getenv("OLLAMA_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

llm_sql_generator = ChatGroq(
     model="llama-3.3-70b-versatile"
 )

#llm_sql_planner = ChatGroq(
#     model="llama-3.3-70b-versatile"
# )

llm_sql_planner = HuggingFaceEndpoint(
    model="openai/gpt-oss-120b",
    task="text-generation"
)

llm_sql_planner = ChatHuggingFace(llm=llm_sql_planner)

#llm_sql_generator = HuggingFaceEndpoint(
#    model="Qwen/Qwen3-Coder-Next",
#    task="text-generation"
#)

#llm_sql_generator = ChatHuggingFace(llm=llm_sql_generator)

