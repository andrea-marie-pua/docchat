"""Test DocChat's tool calls, conversation history, and extra-credit features."""
from chat import Chat


def test_butterfly_image_upload():
    """Make sure my butterfly image gets added to the chat."""
    import base64
    from pathlib import Path
    from tempfile import TemporaryDirectory

    from tools.load_image import load_image

    bot = Chat()

    with TemporaryDirectory(dir=".") as temp_dir:
        image_path = Path(temp_dir) / "butterfly-shoe-bow.png"
        image_bytes = b"\x89PNG\r\n\x1a\nbutterfly image test"
        image_path.write_bytes(image_bytes)

        # Use a relative path without the leading "./" or ".\".
        relative_path = Path(temp_dir).name + "/butterfly-shoe-bow.png"
        result = load_image(bot, relative_path)

        assert result == "Image loaded successfully"
        assert len(bot.messages) == 2

        image_message = bot.messages[-1]
        assert image_message["role"] == "user"

        image_content = image_message["content"][0]
        assert image_content["type"] == "image_url"

        data_url = image_content["image_url"]["url"]
        assert data_url.startswith("data:image/png;base64,")

        encoded = data_url.split(",", 1)[1]
        assert base64.b64decode(encoded) == image_bytes


def test_image_paths_stay_in_project():
    """Make sure DocChat can't wander outside the project folder."""
    from copy import deepcopy

    from tools.load_image import load_image

    bot = Chat()
    original_messages = deepcopy(bot.messages)

    unsafe_paths = [
        "../butterfly.png",
        "images/../butterfly.png",
        "C:/Users/Pictures/butterfly.png",
        "/outside-project/butterfly.png",
    ]

    for path in unsafe_paths:
        result = load_image(bot, path)

        assert result.startswith("Error:")
        assert bot.messages == original_messages


def test_compact_history():
    """Check that DocChat remembers a short summary instead of every message."""
    from unittest.mock import MagicMock, patch
    from tools.compact import compact

    bot = Chat()
    bot.messages.extend([
        {"role": "user", "content": "My favorite color is blue."},
        {"role": "assistant", "content": "Ahoy! Blue it be."},
        {"role": "user", "content": "Remember my favorite color."},
    ])

    response = MagicMock()
    response.content = "The user likes blue.\nRemember this preference."

    with patch("chat.llm", return_value=response) as mock_llm:
        summary = compact(bot)

    assert summary == "The user likes blue.\nRemember this preference."
    assert len(bot.messages) == 1
    assert bot.messages[0]["role"] == "system"
    assert bot.messages[0]["content"] == summary

    sent_messages = mock_llm.call_args.args[0]
    assert sent_messages[1]["content"] == "My favorite color is blue."


def test_compact_five_line_limit():
    """Make sure DocChat doesn't keep a summary longer than five lines."""
    from unittest.mock import MagicMock, patch
    from tools.compact import compact

    bot = Chat()
    bot.messages.append({
        "role": "user",
        "content": "Summarize this conversation."
    })

    response = MagicMock()
    response.content = "\n".join(
        f"Summary line {number}" for number in range(1, 8)
    )

    with patch("chat.llm", return_value=response):
        compact(bot)

    assert len(bot.messages) == 1
    assert len(bot.messages[0]["content"].splitlines()) == 5
    assert "Summary line 6" not in bot.messages[0]["content"]


def test_automatic_tool_call():
    """Make sure DocChat runs a tool when the model requests one."""
    from unittest.mock import MagicMock, patch

    tool_call = MagicMock()
    tool_call.id = "test-call-1"
    tool_call.function.name = "calculate"
    tool_call.function.arguments = '{"expression": "2 + 3"}'

    first = MagicMock()
    first.tool_calls = [tool_call]
    first.model_dump.return_value = {
        "role": "assistant",
        "tool_calls": [{
            "id": "test-call-1",
            "type": "function",
            "function": {
                "name": "calculate",
                "arguments": '{"expression": "2 + 3"}',
            },
        }],
    }

    second = MagicMock()
    second.tool_calls = None
    second.content = "The answer is 5."
    second.model_dump.return_value = {
        "role": "assistant",
        "content": "The answer is 5.",
    }

    bot = Chat()

    with patch("chat.llm", side_effect=[first, second]) as mock_llm:
        answer = bot.send_message("What is 2 + 3?")

    assert answer == "The answer is 5."
    assert mock_llm.call_count == 2
    assert any(
        message["role"] == "tool" and message["content"] == "5"
        for message in bot.messages
    )


def test_manual_command_history():
    """Make sure manual commands work without calling Groq."""
    from unittest.mock import patch

    from chat import repl

    inputs = iter(["/calculate 2 + 3"])

    with patch("builtins.input", side_effect=lambda prompt: next(inputs)):
        with patch("chat.llm") as mock_llm:
            with patch("builtins.print") as mock_print:
                try:
                    repl()
                except StopIteration:
                    pass

    mock_llm.assert_not_called()
    mock_print.assert_any_call("5")
