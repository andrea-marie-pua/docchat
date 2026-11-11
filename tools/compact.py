
"""Compact a chatbot conversation into a short summary."""


def compact(chat):
    """Replace conversation history with a summary of at most five lines.
    Example using a mocked model response:
    >>> from types import SimpleNamespace
    >>> from unittest.mock import patch
    >>> bot = SimpleNamespace(messages=[
    ...     {"role": "user", "content": "I like butterflies."}
    ... ])
    >>> response = SimpleNamespace(content="The user likes butterflies.")
    >>> with patch("chat.llm", return_value=response):
    ...     summary = compact(bot)
    >>> summary
    'The user likes butterflies.'
    >>> len(bot.messages)
    1
    """

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
