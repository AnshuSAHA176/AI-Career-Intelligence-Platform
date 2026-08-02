
from groq import Groq
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from apps.resumes.analyze import get_api


def get_groq_model(model="llama-3.3-70b-versatile"):
    return ChatGroq(
        model=model,
        temperature=0,
        max_retries=2,
        api_key=get_api(),
    ).bind(parallel_tool_calls=False)
