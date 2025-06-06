from interfaces.agent import BaseAgentInterface
from config.prompts.agent import AGENT_PROMPTS
from interfaces.model import LLMInterface

class FinGuideAgent(BaseAgentInterface):

    def get_name(self) -> str:
        return "FinGuide"

    def generate_response(self, user_input: str, llm_client: LLMInterface) -> str:
        prompt = AGENT_PROMPTS["finguide"].format(user_input=user_input)
        return llm_client.generate(prompt)
