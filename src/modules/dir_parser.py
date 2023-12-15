from typing import Dict, Collection, List, Set
from modules import file_parser 
import os
import re

def get_directory_graph(root_path: str) -> Dict[str, Collection[str]]:
    """
    Given a filepath a directory, returns a graph representing the dependency tree of the files
    within that directory. 
    Returns:
        Dict[str, List[str]]: A graph from filenames, each pathed relative to
        the root directory, to their dependencies. Note that we consider external dependencies
        (like <vector>) as leaf nodes that don't depend on any values.

    Throws:
        Error if there are cyclic dependencies
    """
    local_dependencies: Dict[str, Collection[str]] = {file: file_parser.get_file_dependencies(os.path.join(root_path, file)) \
            for file in get_files(root_path) if __is_file_extension(file, ".cpp")}
    nonlocal_dependencies: Dict[str, Collection[str]] = {}
    for dep_collection in local_dependencies.values():
        for dep in dep_collection:
            if dep not in local_dependencies and dep not in nonlocal_dependencies:
                nonlocal_dependencies[dep] = []
    return (local_dependencies | nonlocal_dependencies)
def get_files(root_path: str, relative_path: str = "") -> Collection[str]:
    """
    given a filepath to a root directory, and a relative path to this
    root directory, returns a list of the files (recursively) inside the root_path
    each prefixed with the relative path.
    """
    dir_files: Set[str] = set() 
    try:
        for item in os.listdir(os.path.join(root_path, relative_path)):
            full_path = os.path.join(root_path, relative_path, item)
            if os.path.isfile(full_path):
                dir_files.add(os.path.join(relative_path, item))
            else:
                dir_files = dir_files | set(get_files(root_path, os.path.join(relative_path, item)))
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
