
# DocChat

I, Eru Iluvatar of Middle-CSCI40, used Python and the Groq API to breathe life into this chatbot. The chatbot responds like a pirate and has MEMORY of previous messages within the same conversation. 

## Features

- Interactive chatbot with pirate-style responses
- Remembers conversation history
- Handles Ctrl+C and end-of-input to exit cleanly
- Includes offline doctests using mocked API responses

## Installation

Install the required dependencies and the chatbot:

```bash
python -m pip install .
```

## Usage

Start the chatbot by typing:

```bash
chat
```

Enter a message to receive a response. The chatbot remembers previous messages during the session.

A valid Groq API key must be provided through the `GROQ_API_KEY` environment variable for live conversations.

## Testing

Run the doctests:

```bash
python -m pytest chat.py --doctest-modules
```

Check code coverage:

```bash
python -m coverage run --include="./chat.py" -m pytest chat.py --doctest-modules
python -m coverage report -m chat.py
```
