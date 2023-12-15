import sys
from modules.dir_parser import get_directory_graph
from modules.validate_arguments import validate_arguments
from modules.graph_util import get_external_nodes, get_required_components 
from typing import List, Collection, Dict, Iterable

NUM_ARGS = 2

def main():
    if(len(sys.argv) != 2):
        raise Exception("expected 2 arguments")
    root_dir, target_file = sys.argv
    validate_arguments(root_dir, target_file)
    dir_graph: Dict[str, Collection[str]] = get_directory_graph(root_dir)
if __name__ == "__main__":
    main()
