# Stdlib Imports
import os
import sys
from pathlib import PosixPath


class RecursionDepth:
    """
    A context manager that temporarily sets the recursion depth limit.
    """

    def __init__(self, limit: int):
        self.limit = limit
        self.default_limit = sys.getrecursionlimit()

    def __enter__(self):
        sys.setrecursionlimit(self.limit)

    def __exit__(self, type, value, traceback):
        sys.setrecursionlimit(self.default_limit)


def remove_file_from_root_directory(directory: PosixPath):
    """
    This function removes all images from the specified directory.

    :param file_: The name of the file that needs to be removed from the root directory
    :type file_: str

    :param parent_directory: The parent_directory parameter is a PosixPath object that represents the
        directory from which the files need to be removed
    :type parent_directory: PosixPath
    """

    for file_ in os.listdir(directory):
        os.unlink(os.path.join(directory, file_))
