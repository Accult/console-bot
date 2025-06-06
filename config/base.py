import os
from dotenv import load_dotenv


load_dotenv()

# Function to get the OpenAI API key from environment variables
def get_openai_api_key():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY not found in environment variables.")
    return key

# OpenAI model configuration
OPENAI_MODEL_NAME = "gpt-3.5-turbo"
OPENAI_MAX_TOKENS = 150
OPENAI_TEMPERATURE = 0.4
OPENAI_TOP_P = 1
OPENAI_FREQUENCY_PENALTY = 0
OPENAI_PRESENCE_PENALTY = 0

# Console manager configuration
MAX_ROW_MESSAGES = 5