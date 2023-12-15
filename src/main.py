import sys
from modules.dir_parser import get_directory_graph
from modules.validate_arguments import validate_arguments
from modules.file_parser import get_file_dependencies, get_file_body
from modules.graph_util import get_external_nodes, get_required_components 
from typing import List, Collection, Dict, Iterable

NUM_ARGS = 2

def main():
    if(len(sys.argv) != 2):
        raise Exception("expected 2 arguments")
    root_dir, target_file = sys.argv
    validate_arguments(root_dir, target_file)
    dir_graph: Dict[str, Collection[str]] = get_directory_graph(root_dir)

def get_external_dependencies(dir_graph: Dict[str, Collection[str]], target_file: str):
    file_dependencies: Iterable[str] = get_file_dependencies(target_file)
    direct_external_dependencies = filter(lambda dep: dep in dir_graph, file_dependencies)

    indirect_dependencies: Iterable[str] = get_required_components(dir_graph, file_dependencies)
    

def get_internal_dependencies(dir_graph: Dict[str, Collection[str]], target_file: str, target_file_dependencies: Iterable[str]):
    pass



if __name__ == "__main__":
    main()
