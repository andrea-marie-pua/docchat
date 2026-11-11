
"""Run DocChat with manual commands and automatic Groq tool calling."""

import json
import os
import sys

from dotenv import load_dotenv
from groq import Groq

from tools.calculate import calculate
from tools.cat import cat
from tools.grep import grep
from tools.ls import ls

load_dotenv()

FUNCTIONS = {
    "calculate": calculate,
    "cat": cat,
    "grep": grep,
    "ls": ls,
}

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string"}
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "ls",
            "description": "List files in a directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cat",
            "description": "Read the contents of a text file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "grep",
            "description": "Search files using a regular expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {"type": "string"},
                    "path": {"type": "string"}
                },
                "required": ["pattern", "path"]
            }
        }
    }
]


def llm(messages, temperature=1):
    """Send the conversation and available tools to Groq."""
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    completion = client.chat.completions.create(
        messages=messages,
        model="openai/gpt-oss-20b",
        temperature=temperature,
        tools=TOOLS,
        tool_choice="auto",
        timeout=30,
    )

    return completion.choices[0].message


class Chat:
    """Manage chatbot conversations and tool execution."""

    def __init__(self, system="You are a helpful assistant.", debug=False):
        """Initialize conversation history and debug settings."""
        self.debug = debug
        self.messages = [{"role": "system", "content": system}]

    def send_message(self, message, temperature=0.8):
        """Send a message, execute requested tools, and retain the reply."""
        self.messages.append({"role": "user", "content": message})

        for _ in range(10):
            response = llm(self.messages, temperature=temperature)

            response_dict = response.model_dump(exclude_none=True)
            self.messages.append(response_dict)

            if not response.tool_calls:
                return response.content

            for call in response.tool_calls:
                name = call.function.name

                if self.debug:
                    print("TOOL REQUEST:", name, call.function.arguments)

                try:
                    arguments = json.loads(call.function.arguments)

                    if name not in FUNCTIONS:
                        result = f"Error: Unknown tool '{name}'"
                    else:
                        result = FUNCTIONS[name](**arguments)

                except (ValueError, TypeError, KeyError) as error:
                    result = f"Error: {error}"

                self.messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": str(result),
                })

        return "Error: Too many tool requests"


def run_command(command):
    """Execute a manual slash command using a registered tool."""
    parts = command[1:].split()

    if not parts:
        return "Error: Empty command"

    name = parts[0]
    arguments = parts[1:]

    if name not in FUNCTIONS:
        return f"Error: Unknown command '{name}'"

    try:
        if name == "calculate":
            return str(FUNCTIONS[name](" ".join(arguments)))

        if name == "grep":
            if len(arguments) < 2:
                return "Error: grep requires a pattern and path"
            return str(FUNCTIONS[name](arguments[0], arguments[1]))

        if name == "ls":
            return str(FUNCTIONS[name](*arguments))

        if name == "cat":
            return str(FUNCTIONS[name](*arguments))

    except TypeError as error:
        return f"Error: {error}"


def repl(temperature=0.8, debug=False):
    """Run an interactive chatbot with optional tool debugging."""
    chat = Chat(
        system="You are a helpful assistant. You always speak like a pirate.",
        debug=debug,
    )

    try:
        while True:
            user_input = input("chat> ")

            if user_input.startswith("/"):
                result = run_command(user_input)
                print(result)

                chat.messages.append({
                    "role": "user",
                    "content": user_input,
                })
                chat.messages.append({
                    "role": "assistant",
                    "content": str(result),
                })
            else:
                print(chat.send_message(user_input, temperature=temperature))

    except (KeyboardInterrupt, EOFError):
        print()


def main():
    """Launch interactive chat, debug mode, or a one-shot message."""
    if len(sys.argv) > 1 and sys.argv[1] == "--debug":
        repl(debug=True)

    elif len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
        bot = Chat()
        print(bot.send_message(message))

    else:
        repl()


if __name__ == "__main__":
    main()
