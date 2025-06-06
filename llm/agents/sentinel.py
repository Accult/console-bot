from interfaces.agent import BaseAgentInterface
from config.prompts.agent import AGENT_PROMPTS
from interfaces.model import LLMInterface

class SentinelAgent(BaseAgentInterface):

    def get_name(self) -> str:
        return "Sentinel"

    def generate_response(self, user_input: str, llm_client: LLMInterface) -> str:
        prompt = AGENT_PROMPTS["sentinel"].format(user_input=user_input)
        return llm_client.generate(prompt)
