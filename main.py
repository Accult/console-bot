import logging

from llm.agents.sentinel import SentinelAgent
from llm.agents.finguide import FinGuideAgent
from llm.agents.edubot import EduBotAgent
from manager.console import ConversationManager
from llm.models.openai import OpenAIClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("chatbot")

def main():
    print("\nWelcome to the Multi-Agent Chatbot!")
    print("Instructions:")
    print(" - Type your message and press Enter to chat.")
    print(" - To address a specific agent, use @agent_tag (e.g., @sentinel, @finguide, @edubot).")
    print(" - Type `/reset` to restart the conversation.")
    print(" - Type `/exit` to quit.\n")

    llm_client = OpenAIClient()
    agents = {
        "sentinel": SentinelAgent(),
        "finguide": FinGuideAgent(),
        "edubot": EduBotAgent(),
    }
    manager = ConversationManager(llm_client=llm_client, agents=agents)

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "/exit":
            logger.info("Goodbye!")
            break

        if user_input.lower() == "/reset":
            manager.reset_conversation()
            logger.info("Conversation reset!")
            continue

        try:
            response = manager.process_user_message(user_input)
            print(f"{manager.current_agent_tag.capitalize()}: {response}\n")
        except Exception as e:
            logger.error(f"[ERROR] {str(e)}\n")


if __name__ == "__main__":
    main()
