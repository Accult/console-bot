from openai import OpenAI
from interfaces.model import LLMInterface
from config.base import (
    get_openai_api_key,
    OPENAI_MODEL_NAME,
    OPENAI_MAX_TOKENS,
    OPENAI_TEMPERATURE,
    OPENAI_TOP_P,
    OPENAI_FREQUENCY_PENALTY,
    OPENAI_PRESENCE_PENALTY,
)

class OpenAIClient(LLMInterface):
    def __init__(self, max_tokens: int = OPENAI_MAX_TOKENS, temperature: float = OPENAI_TEMPERATURE):
        api_key = get_openai_api_key()
        self.client = OpenAI(api_key=api_key)
        self.max_tokens = max_tokens
        self.temperature = temperature

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.max_tokens,
                top_p=OPENAI_TOP_P,
                frequency_penalty=OPENAI_FREQUENCY_PENALTY,
                presence_penalty=OPENAI_PRESENCE_PENALTY,
                temperature=self.temperature,
            )
            result = response.choices[0].message.content
            cleaned_result = result.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
            return cleaned_result.strip()
        except Exception as e:
            return f"[ERROR] Failed to generate response: {str(e)}"
