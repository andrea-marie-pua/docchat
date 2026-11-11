
"""Compact a chatbot conversation into a short summary."""


def compact(chat):
    """Replace conversation history with a summary of at most five lines."""
    from chat import llm

    messages = chat.messages + [
        {
            "role": "user",
            "content": (
                "Summarize the conversation so far in no more than "
                "five lines. Preserve important facts and context."
            ),
        }
    ]

    response = llm(messages, temperature=0)

    summary = response.content or ""
    summary = "\n".join(summary.splitlines()[:5])

    chat.messages = [
        {
            "role": "system",
            "content": summary,
        }
    ]

    return summary
