import re
from typing import List, Collection
import os

INCLUDE_REGEX = "#[\\s]*include[\\s]*<([^>]+)>" 

def get_file_dependencies(root_path: str, file_path: str) -> Collection[str]:
    """
    Given a filepath, returns a list of all filepaths that it is a dependency of. 

    Args:
        root_path (str): a path to the root directory
        file_path (str): file path to the file that we want to source

    Returns:
        List[str]: List of file path dependencies
    """
    with open(os.path.join(root_path, file_path), "r") as file:
        return re.findall(INCLUDE_REGEX, file.read())

if __name__ == "__main__":
    print(get_file_dependencies("/Users/sidneylevine/personal/ws/HeaderExpansion/src/modules", "test.cpp"))

