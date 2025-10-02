# agents.py
# Defines lightweight "agents" for downstream use.

import os
from openai import OpenAI

# Setup OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None


def agent_moneypenny(raw_text: str) -> str:
    """
    Pass raw transcript directly to GPT-4o.
    Returns the model response as string.
    """
    if not client:
        return "[MOCK RESPONSE: no OPENAI_API_KEY set]"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": raw_text}
            ],
            max_tokens=800
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[ERROR calling Agent Moneypenny: {e}]"


def agent_maxwell(raw_text: str) -> str:
    """
    Placeholder for coding-agent style summarization.
    For now, returns a dummy string.
    """
    return "[Agent Maxwell stub: structured coding prompt will go here]"
