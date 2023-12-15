from typing import Collection
import re
import os

INCLUDE_REGEX = "#[\\s]*include[\\s]*<([^>]+)>" 

def get_file_dependencies(file_path: str) -> Collection[str]:
    """
    Given a filepath, returns a list of all filepaths that it is a dependency of. 

    Args:
        root_path (str): a path to the root directory
        file_path (str): file path to the file that we want to source

    Returns:
        List[str]: List of file path dependencies
    """
    with open(file_path, "r") as file:
        return re.findall(INCLUDE_REGEX, file.read())

def get_file_body(file_path: str) -> str:
    with open(file_path, "r") as file:
        return re.sub(INCLUDE_REGEX, '', file.read())
