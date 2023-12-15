import sys
import os
from modules.validate_arguments import validate_arguments
from modules.dependency_manager import dependency_manager
from modules.file_parser import get_file_body
from typing import List, Collection, Dict, Iterable

NUM_ARGS = 2

def main():
    if(len(sys.argv) != 2):
        raise Exception("expected 2 arguments")
    root_dir, target_file = sys.argv
    validate_arguments(root_dir, target_file)
    dependency_state = dependency_manager(root_dir, target_file)
    with open(target_file, "w") as destination_file:
        destination_file.write(get_built_file(dependency_state, target_file, root_dir))

def get_built_file(dep_manager, target_file, root_dir) -> str:
    """
    Merge the file, root_dir pair given by dep_manager into a single file
    """
    top_header: str = f"#pragma once\n"
    includes: str = "\n".join([get_include(inc) for inc in dep_manager.get_external_dependencies()])
    import_bodies: str = "\n".join([get_file_body(dep_path) for dep_path in dep_manager.get_internal_dependencies()])
    base_body: str = get_file_body(target_file)
    return "\n".join([top_header, includes, import_bodies, base_body])

def get_include(dependency: Iterable[str]) -> str:
    return f"#include <{dependency}>"


if __name__ == "__main__":
    main()
