
import os
from copy import deepcopy
from unittest.mock import MagicMock, patch

from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.environ.get('GROQ_API_KEY'))


def llm(messages, temperature=1):
    completion = client.chat.completions.create(
        messages=messages,
        model='openai/gpt-oss-20b',
        temperature=temperature,
    )
    return completion.choices[0].message.content


class Chat:
    def __init__(self, system='You are a helpful assistant.'):
        self.messages = [{'role': 'system', 'content': system}]

    def send_message(self, message, temperature=0.8):
        """Send a message and retain the reply.

        >>> response = MagicMock()
        >>> response.choices[0].message.content = 'Hello!'
        >>> with patch.object(client.chat.completions, 'create', return_value=response):
        ...     chat = Chat(system='Be brief.')
        ...     print(chat.send_message('Hi', temperature=0))
        Hello!
        >>> expected = [
        ...     {'role': 'system', 'content': 'Be brief.'},
        ...     {'role': 'user', 'content': 'Hi'},
        ...     {'role': 'assistant', 'content': 'Hello!'},
        ... ]
        >>> chat.messages == expected
        True

        >>> first = MagicMock()
        >>> first.choices[0].message.content = 'Ahoy!'
        >>> second = MagicMock()
        >>> second.choices[0].message.content = 'You said hello!'
        >>> snapshots = []
        >>> responses = iter([first, second])
        >>> def fake_create(*args, **kwargs):
        ...     snapshots.append(deepcopy(kwargs['messages']))
        ...     return next(responses)
        >>> with patch.object(client.chat.completions, 'create', side_effect=fake_create):
        ...     bot = Chat(system='Be a pirate.')
        ...     print(bot.send_message('Hello', temperature=0))
        ...     print(bot.send_message('What did I say?', temperature=0))
        Ahoy!
        You said hello!
        >>> snapshots[1] == [
        ...     {'role': 'system', 'content': 'Be a pirate.'},
        ...     {'role': 'user', 'content': 'Hello'},
        ...     {'role': 'assistant', 'content': 'Ahoy!'},
        ...     {'role': 'user', 'content': 'What did I say?'},
        ... ]
        True
        >>> bot.messages[-1] == {
        ...     'role': 'assistant',
        ...     'content': 'You said hello!'
        ... }
        True
        """
        self.messages.append({'role': 'user', 'content': message})
        reply = llm(self.messages, temperature=temperature)
        self.messages.append({'role': 'assistant', 'content': reply})
        return reply


def repl(temperature=0.8):
    """Run an interactive chatbot conversation.

    Test two messages, retained history, and EOFError.

    >>> first = MagicMock()
    >>> first.choices[0].message.content = 'Ahoy!'
    >>> second = MagicMock()
    >>> second.choices[0].message.content = 'You said hello!'
    >>> snapshots = []
    >>> responses = iter([first, second])
    >>> def fake_create(*args, **kwargs):
    ...     snapshots.append(deepcopy(kwargs['messages']))
    ...     return next(responses)
    >>> with patch('builtins.input', side_effect=['Hello', 'What did I say?', EOFError]):
    ...     with patch.object(client.chat.completions, 'create', side_effect=fake_create):
    ...         repl(temperature=0)
    Ahoy!
    You said hello!
    <BLANKLINE>
    >>> len(snapshots)
    2
    >>> snapshots[1][1:4] == [
    ...     {'role': 'user', 'content': 'Hello'},
    ...     {'role': 'assistant', 'content': 'Ahoy!'},
    ...     {'role': 'user', 'content': 'What did I say?'},
    ... ]
    True

    Test KeyboardInterrupt separately.

    >>> with patch('builtins.input', side_effect=KeyboardInterrupt):
    ...     repl(temperature=0)
    <BLANKLINE>
    """
    chat = Chat(
        system='You are a helpful assistant. You always speak like a pirate.'
    )
    try:
        while True:
            user_input = input('chat> ')
            print(chat.send_message(user_input, temperature=temperature))
    except (KeyboardInterrupt, EOFError):
        print()


if __name__ == '__main__':
    repl()
