import sys
import os
from modules.validate_arguments import validate_arguments
from modules.dependency_manager import dependency_manager
from modules.file_parser import get_file_body
from typing import List, Collection, Dict, Iterable

NUM_ARGS = 2

def main():
    if(len(sys.argv) != 3):
        raise Exception("expected 2 arguments")
    _, root_dir, target_file = sys.argv
    validate_arguments(root_dir, target_file)
    dependency_state = dependency_manager(root_dir, target_file)
    target_file_header: str = dependency_state.get_full_header()
    target_file_body: str = get_file_body(target_file)
    new_file:str = target_file_header + target_file_body
    with open(target_file, "w") as destination_file:
        destination_file.write(new_file)

if __name__ == "__main__":
    main()
