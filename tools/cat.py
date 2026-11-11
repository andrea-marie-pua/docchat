
"""Read the contents of text files safely."""

from tools.path_utils import is_path_safe


def cat(path):
    """Return the contents of a text file or an error message.

    >>> import tempfile
    >>> from pathlib import Path
    >>> with tempfile.TemporaryDirectory() as folder:
    ...     path = Path(folder) / "test.txt"
    ...     _ = path.write_text("Hello from docchat!", encoding="utf-8")
    ...     # TemporaryDirectory uses an absolute path, so test
    ...     # successful reading from within the directory instead.
    ...     import os
    ...     original = os.getcwd()
    ...     os.chdir(folder)
    ...     try:
    ...         print(cat("test.txt"))
    ...     finally:
    ...         os.chdir(original)
    Hello from docchat!
    >>> cat("../secret.txt")
    'Error: Unsafe path'
    >>> cat("missing_file.txt").startswith("Error:")
    True
    """

    if not is_path_safe(path):
        return "Error: Unsafe path"

    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except (OSError, UnicodeError) as error:
        return f"Error: {error}"
