from abc import ABC, abstractmethod
from interfaces.model import LLMInterface

class BaseAgentInterface(ABC):

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def generate_response(self, user_input: str, llm_client: LLMInterface) -> str:
        pass
