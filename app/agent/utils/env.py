"""
utils/env.py

Provides basic tools to load and verify required env variables.

Functions and global dict:
- ENV: global dict with env variables to be used by other modules
- 
"""
 

from dotenv import load_dotenv
import os
from .logger import logger
from .exceptions import MissingEnvVariable

# Specify in this list all env variables that should be placed in .env file
REQUIRED_ENV = [
    "OPENAI_API_KEY",
    "LANGSMITH_API_KEY",
    "LANGSMITH_ENDPOINT",
    "LANGSMITH_TRACING",
    "LANGSMITH_PROJECT",
]

# Global dict for env variables (API keys and other important env variables)
ENV = {}

# loading and checking env variables

load_dotenv()
for env in REQUIRED_ENV:
    logger.debug(f"checking key {env} ...")
    env_value = os.getenv(env)
    if not env_value:
        raise MissingEnvVariable(F"Missing required Env variable {env}.")
    logger.debug(f"{env} loaded.")
    ENV[env] = env_value
