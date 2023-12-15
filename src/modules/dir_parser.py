from typing import Dict, Collection, List
from modules import file_parser 
import os
import re

def get_directory_graph(root_path: str) -> Dict[str, Collection[str]]:
    """
    Given a filepath a directory, returns a graph representing the dependency tree of the files
    within that directory. 
    Returns:
        Dict[str, List[str]]: A graph from filenames, each pathed relative to
        the root directory, to their dependencies

    Throws:
        Error if there are cyclic dependencies
    """
    return {file: file_parser.get_file_dependencies(os.path.join(root_path, file)) \
            for file in __get_files(root_path) if __is_file_extension(file, ".cpp")}
def __get_files(root_path: str, relative_path: str = "") -> List[str]:
    """
    given a filepath to a root directory, and a relative path to this
    root directory, returns a list of the files (recursively) inside the root_path
    each prefixed with the relative path.
    """
    dir_files = []
    try:
        for item in os.listdir(os.path.join(root_path, relative_path)):
            full_path = os.path.join(root_path, relative_path, item)
            if os.path.isfile(full_path):
                dir_files.append(os.path.join(relative_path, item))
            else:
                dir_files += __get_files(root_path, os.path.join(relative_path, item))
    except OSError as e:
        print(f"Error accessing {root_path}: {e}")
    return dir_files 
def __is_file_extension(file_path, extension):
    """
    Check if the file at file_path has the given extension.
    Extension should start with a dot, e.g., '.txt', '.jpg'.
    """
    _, file_ext = os.path.splitext(file_path)
    return file_ext.lower() == extension.lower()


if __name__ == "__main__":
    pwd = '/Users/sidneylevine/personal/ws/HeaderExpansion/src'
    get_directory_graph(pwd)
