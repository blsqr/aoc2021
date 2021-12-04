"""Assorted tools that are used within the puzzle solutions"""

import os
from urllib.request import urlopen as _urlopen
from typing import List

# -----------------------------------------------------------------------------

def relative_to_file(filepath: str, *args) -> str:
    """Returns a file path relative to a certain file's path.
    This is useful when requiring an absolute path of a file relative to some
    module file (which can be passed via ``__file__``).
    
    Args:
        module_filepath (str): File path to generate the relative path to
        *args: Arguments to ``os.path.join``
    
    Returns:
        str: Absolute file path
    """
    module_dir = os.path.dirname(filepath)
    return os.path.join(module_dir, *args)


def load_input(
    mode: str, *, day: int, fpath: str, url: str = None, test_input: str = None
) -> List[str]:
    """Loads input from different sources: from a file, a URL, or directly from
    a multi-line string object.
    Always returns a list of strings (the lines of the file) which still need
    to be parsed further. Line breaks are stripped away.

    .. note::

        Each line's whitespace is stripped away regardless of mode.

    Args:
        mode (str): Which mode to use for loading input, can be:
            ``file``, ``url``, ``test``
        day (int): The day to load (not used currently)
        fpath (str): The absolute file path from which to load the input data
        url (str, optional): The URL from which to load the input data (not
            possible to implement at the moment)
        test_input (str, optional): Some test input, provided as multi-line.
    """
    print(f"Loading input data (mode: {mode}) ...")

    if mode == "file":
        with open(fpath, mode="r") as f:
            data = [line.strip() for line in f.readlines()]

    elif mode == "url":
        # return [line.decode("utf-8").strip() for line in _urlopen(url)]
        raise NotImplementedError(
            "Loading input from URL is not possible yet because it requires "
            "to be logged in to Advent of Code ..."
        )

    elif mode == "test":
        data = [line.strip() for line in test_input.strip().split("\n")]

    else:
        raise ValueError(
            f"Invalid input loading mode '{mode}'! Choose from: file, test"
        )

    print("Input data loaded.\n")
    return data
