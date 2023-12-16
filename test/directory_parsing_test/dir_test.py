import os
import sys
from typing import Collection
script_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(script_path)))
sys.path.append(project_root)

from src.modules import dir_parser

def collection_equality(c1: Collection[str], c2: Collection[str]):
    for elt in c1:
        if elt not in c2:
            return False
    return len(c1) == len(c2)
def test_dependency_list():
    expected_dir_graph = {"main.cpp": 
                             ["sub_dir/dependency1.cpp",
                              "sub_dir/sub_sub_dir/dependency2.cpp","unrelated"],
                         "sub_dir/dependency1.cpp":
                             ["sub_dir/sub_sub_dir/dependency2.cpp",
                              "another_unrelated"],
                         "sub_dir/sub_sub_dir/dependency2.cpp":
                             ["unrelated"]}
    
    current_file_path = os.path.abspath(__file__)
    parent_directory = os.path.dirname(current_file_path)
    neighboring_directory_name = "test_dir"
    neighboring_directory_path = os.path.join(parent_directory, neighboring_directory_name)

    test_module_graph = dir_parser.get_module_graph(neighboring_directory_path)
    assert(len(test_module_graph) == len(expected_dir_graph))
    for item in expected_dir_graph:
        assert(item in test_module_graph)
        assert(collection_equality(test_module_graph[item], expected_dir_graph[item]))

if __name__ == "__main__":
    test_dependency_list()

