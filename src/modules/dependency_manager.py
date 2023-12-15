from modules.dir_parser import get_directory_graph, get_files
from modules.validate_arguments import validate_arguments
from modules.file_parser import get_file_dependencies, get_file_body
from modules.graph_util import  get_required_components 
from typing import List, Collection, Dict, Set
class dependency_manager:
    """
    Manage the dependency components of a given file relative to a specific
    directory.
    """
    def __init__(self, target_dir: str, target_file: str):
        dir_graph: Dict[str, Collection[str]] = get_directory_graph(target_dir)
        direct_file_dependencies: Collection[str] = get_file_dependencies(target_file)
        indirect_file_depenencies: Collection[str] = get_required_components(dir_graph, direct_file_dependencies)
        self.dependencies: Collection[str] = self.__merge(direct_file_dependencies, indirect_file_depenencies)
        self.dir_components: Collection[str] = get_files(target_dir)
    def get_internal_dependencies(self) -> Collection[str]:
        """
        Returns a list of the paths to the dependencies for the target_file
        that are inside the target directory
        """
        return {dependency for dependency in self.dependencies if dependency in self.dir_components}
    def get_external_dependencies(self) -> Collection[str]:
        """
        Returns a list of the dependencies (including sub-dependencies) that are
        dependencies to the file and are outside the target directory (e.x #include <vector>)
        """
        return {dependency for dependency in self.dependencies if dependency not in self.dir_components}
    def __merge(self, C1: Collection[str], C2: Collection[str]) -> Collection[str]:
        merged_collection: Set[str] = set()
        for c in C1:
            merged_collection.add(c)
        for c in C2:
            merged_collection.add(c)
        return merged_collection
