
"""Validate file paths before allowing file access."""

from pathlib import Path


def is_path_safe(path):
    """Check that a path is relative and contains no parent traversal.

    >>> is_path_safe("notes.txt")
    True
    >>> is_path_safe("tools/calculate.py")
    True
    >>> is_path_safe("../secret.txt")
    False
    >>> is_path_safe("tools/../secret.txt")
    False
    >>> is_path_safe("/etc/passwd")
    False
    >>> is_path_safe("C:\\\\Users\\\\secret.txt")
    False
    """
    import ntpath

    path = str(path)

    if path.startswith(("/", "\\")) or Path(path).is_absolute() or ntpath.isabs(path):
        return False

    parts = path.replace("\\", "/").split("/")

    if ".." in parts:
        return False

    return True
