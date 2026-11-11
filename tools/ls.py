
"""List files in a directory safely."""

import glob
import os

from tools.path_utils import is_path_safe


def ls(path="."):
    """List the contents of a directory in alphabetical order.

    >>> isinstance(ls("."), str)
    True
    >>> "ls.py" in ls("tools").split()
    True
    >>> ls("..")
    'Error: Unsafe path'
    >>> ls("../secret")
    'Error: Unsafe path'
    """
    if not is_path_safe(path):
        return "Error: Unsafe path"

    files = sorted(glob.glob(os.path.join(path, "*")))
    return " ".join(os.path.basename(file) for file in files)
