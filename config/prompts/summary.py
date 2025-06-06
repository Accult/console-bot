from llm.models.openai import OpenAIClient

SUMMARY_PROMPT = "Summarize the following conversation briefly:\n\n{conversation}"

def generate_summary(conversation: str, llm_client: OpenAIClient) -> str:
    prompt = SUMMARY_PROMPT.format(conversation=conversation)
    return llm_client.generate(prompt)