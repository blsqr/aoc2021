"""Assorted tools that are used within the puzzle solutions"""

import os

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
