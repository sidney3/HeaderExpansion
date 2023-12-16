from typing import Dict, Collection, List, Set
from modules import file_parser 
import os
import re

def get_dependency_graph(root_path: str) -> Dict[str, Collection[str]]:
    """
    Given a filepath to a directory, returns a graph with

    (filepath) -> the components (filepath) depends on
    """
    dependencies: Dict[str, Collection[str]] = {}
    for file in get_files(root_path):
        if file not in dependencies:
            dependencies[file] = []
        if not (__is_file_extension(file, ".cpp") or __is_file_extension(file, ".cc")):
            continue
        for dependency in file_parser.get_file_dependencies(os.path.join(root_path, file)):
            dependencies[dependency] = __merge([file], dependencies.get(dependency, []))
    return dependencies
def get_module_graph(root_path: str) -> Dict[str, Collection[str]]:
    """
    Given a filepath to a directory, returns a graph with

    (filepath) -> the components FOR WHICH (filepath) is a dependency
    """
    dependencies: Dict[str, Collection[str]] = {}
    return {file: file_parser.get_file_dependencies(os.path.join(root_path,file)) for file in get_files(root_path) if __is_file_extension(file, ".cpp") or __is_file_extension(file, ".cc")}
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
def __merge(c1: Collection[str], c2: Collection[str]) -> Collection[str]:
    merged: List[str] = []
    for c in c1:
        merged.append(c)
    for c in c2:
        merged.append(c)
    return merged
