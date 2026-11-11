
"""Search text files for lines matching a regular expression."""

import glob
import re

from tools.path_utils import is_path_safe


def grep(pattern, path):
    r"""Return matching lines from files selected by a glob pattern.

    >>> import tempfile
    >>> from pathlib import Path
    >>> import os
    >>> with tempfile.TemporaryDirectory() as folder:
    ...     original = os.getcwd()
    ...     os.chdir(folder)
    ...     try:
    ...         _ = Path("sample.txt").write_text(
    ...             "TODO: fix bug\nDONE: write code\nTODO: add tests\n",
    ...             encoding="utf-8"
    ...         )
    ...         print(grep("TODO", "*.txt"))
    ...         print(repr(grep("NOT_FOUND", "*.txt")))
    ...     finally:
    ...         os.chdir(original)
    TODO: fix bug
    TODO: add tests
    ''
    >>> grep("TODO", "../*.txt")
    'Error: Unsafe path'

    >>> with tempfile.TemporaryDirectory() as folder:
    ...     original = os.getcwd()
    ...     os.chdir(folder)
    ...     try:
    ...         _ = Path("invalid.txt").write_bytes(bytes([255, 254, 253]))
    ...         print(repr(grep("TODO", "*.txt")))
    ...     finally:
    ...         os.chdir(original)
    ''

    >>> from unittest.mock import patch
    >>> with patch("tools.grep.glob.glob", return_value=["../secret.txt"]):
    ...     grep("TODO", "*.txt")
    ''
    """

    if not is_path_safe(path):
        return "Error: Unsafe path"

    matches = []

    for filename in sorted(glob.glob(path)):
        if not is_path_safe(filename):
            continue

        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    if re.search(pattern, line):
                        matches.append(line.rstrip("\n"))
        except (OSError, UnicodeError):
            continue

    return "\n".join(matches)
