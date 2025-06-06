from typing import List, Optional, Dict
import re

from config.base import MAX_ROW_MESSAGES
from config.prompts.summary import generate_summary
from interfaces.agent import BaseAgentInterface
from interfaces.model import LLMInterface


class AgentSelector:
    AGENT_KEYWORDS_MAP = {
        "security": "sentinel",
        "finance": "finguide",
        "money": "finguide",
        "budget": "finguide",
        "learn": "edubot",
        "explain": "edubot",
        "encrypt": "sentinel",
    }

    def __init__(self, agents: Dict[str, BaseAgentInterface], default_agent_tag: str = "edubot"):
        self.agents = agents
        self.default_agent_tag = default_agent_tag

    def extract_agent_tag(self, user_input: str) -> tuple[str, Optional[str]]:
        match = re.search(r"@(\w+)", user_input)
        if match:
            tag = match.group(1).lower()
            cleaned_input = re.sub(r"@\w+", "", user_input).strip()
            return cleaned_input, tag
        return user_input, None

    def select_agent(self, user_input: str, forced_agent_tag: Optional[str] = None) -> BaseAgentInterface:
        if forced_agent_tag and forced_agent_tag in self.agents:
            selected_agent_tag = forced_agent_tag
        else:
            selected_agent_tag = self.default_agent_tag
            for keyword, agent_tag in AgentSelector.AGENT_KEYWORDS_MAP.items():
                if keyword.lower() in user_input.lower():
                    selected_agent_tag = agent_tag
                    break
        return self.agents[selected_agent_tag]

class ConversationManager:
    def __init__(
        self,
        llm_client: LLMInterface,
        agents: Dict[str, BaseAgentInterface],
        max_raw_messages: int = MAX_ROW_MESSAGES,
        default_agent_tag: str = "edubot"
    ):
        self.llm_client = llm_client
        self.agent_selector = AgentSelector(agents, default_agent_tag)
        self.max_raw_messages = max_raw_messages
        self.raw_messages: List[str] = []
        self.summaries: List[str] = []
        self.current_agent_tag: Optional[str] = None

    def reset_conversation(self):
        self.raw_messages.clear()
        self.summaries.clear()
        self.current_agent_tag = None

    def add_message(self, message: str):
        self.raw_messages.append(message)
        if len(self.raw_messages) > self.max_raw_messages:
            self._update_summary()

    def _update_summary(self):
        history_to_summarize = self.raw_messages[:-self.max_raw_messages]
        if not history_to_summarize:
            return
        summary_text = generate_summary("\n".join(history_to_summarize), self.llm_client)
        self.summaries.append(summary_text)
        self.raw_messages = self.raw_messages[-self.max_raw_messages:]

    def process_user_message(self, user_input: str) -> str:
        cleaned_input, forced_agent_tag = self.agent_selector.extract_agent_tag(user_input)
        agent = self.agent_selector.select_agent(cleaned_input, forced_agent_tag)
        self.current_agent_tag = agent.get_name().lower()
        self.add_message(f"User: {user_input}")

        prompt_parts = self.summaries + self.raw_messages
        full_context = "\n".join(prompt_parts) + f"\nAgent ({agent.get_name()}):"

        response = agent.generate_response(full_context, self.llm_client)
        self.add_message(f"{agent.get_name()}: {response}")

        return response