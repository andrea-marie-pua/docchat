
"""Load a local PNG image into chatbot conversation history."""

import base64
from pathlib import Path

from tools.path_utils import is_path_safe


def load_image(chat, path):
    """Add a safe local PNG image to chat history as a Base64 data URL.
    Unsafe paths or unreadable images leave the conversation unchanged.

    Examples:
        >>> from types import SimpleNamespace
        >>> bot = SimpleNamespace(messages=[])
        >>> load_image(bot, "../butterfly.png")
        'Error: Unsafe path'
        >>> bot.messages
        []
        >>> load_image(bot, "butterfly.jpg")
        'Error: Only PNG images are supported'
        >>> bot.messages
        []
    """

    path = str(path)

    if not is_path_safe(path):
        return "Error: Unsafe path"

    image_path = Path(path)

    if image_path.suffix.lower() != ".png":
        return "Error: Only PNG images are supported"

    try:
        image_bytes = image_path.read_bytes()
    except OSError as error:
        return f"Error: {error}"

    encoded_image = base64.b64encode(image_bytes).decode("ascii")
    data_url = f"data:image/png;base64,{encoded_image}"

    chat.messages.append({
        "role": "user",
        "content": [
            {
                "type": "image_url",
                "image_url": {
                    "url": data_url
                }
            }
        ]
    })

    return "Image loaded successfully"
