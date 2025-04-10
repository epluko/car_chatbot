"""
utils/llm.py

Provides defined LLM as a global variable LLM.
"""


from langchain_openai import ChatOpenAI
from .env import ENV

MODEL = "gpt-4o-mini"
# MODEL = "gpt-3.5-turbo"
# MODEL = "gpt-4o"

LLM = ChatOpenAI(model=MODEL, temperature=0, api_key=ENV['OPENAI_API_KEY'])
