from typing import Collection
import re
import os

INCLUDE_REGEX = "#[\\s]*include[\\s]*<([^>]+)>" 

def get_file_dependencies(file_path: str) -> Collection[str]:
    """
    Given a filepath, returns a list of all filepaths that it is a dependency of. 

    Args:
        file_path (str): a path to the root directory

    Returns:
        List[str]: List of file path dependencies
    """
    with open(file_path, "r") as file:
        return re.findall(INCLUDE_REGEX, file.read())

def get_file_body(file_path: str) -> str:
    """
    Given a filepath, returns a list of all filepaths that it is a dependency of. 

    Args:
        file_path (str): a path to the target file

    Returns:
        str: The body (components minus import statements) of the file
    """
    BODY_REGEX = "#[^\n]*\n" 
    with open(file_path, "r") as file:
        return re.sub(BODY_REGEX, '', file.read())
