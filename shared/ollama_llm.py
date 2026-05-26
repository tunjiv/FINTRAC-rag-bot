from langchain_community.llms import Ollama
from dotenv import load_dotenv
import os

load_dotenv()

def get_llm(model="llama3", temperature=0):
    return Ollama(
        model=model,
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        temperature=temperature,
    )

llm_fast    = get_llm(model="llama3", temperature=0.1)
llm_careful = get_llm(model="llama3", temperature=0)