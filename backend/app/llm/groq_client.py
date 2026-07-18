import os
import httpx
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

client = httpx.Client(verify=False)

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    temperature=0,
    http_client=client,
)