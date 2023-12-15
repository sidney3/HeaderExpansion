from modules.dir_parser import get_directory_graph, get_files
from modules.validate_arguments import validate_arguments
from modules.file_parser import get_file_dependencies, get_file_body
from modules.graph_util import  get_required_components 
from typing import List, Collection, Dict, Set, Iterable
class dependency_manager:
    """
    Manage the dependency components of a given file relative to a specific
    directory.
    """
    def __init__(self, target_dir: str, target_file: str):
        dir_graph: Dict[str, Collection[str]] = get_directory_graph(target_dir)
        direct_file_dependencies: Iterable[str] = {dep for dep in get_file_dependencies(target_file) if dep not in dir_graph}
        indirect_file_depenencies: Iterable[str] = get_required_components(dir_graph, direct_file_dependencies)
        self.dependencies: Iterable[str] = self.__merge(direct_file_dependencies, indirect_file_depenencies)
        self.dir_components: Iterable[str] = get_files(target_dir)
    def __get_internal_dependencies(self) -> Iterable[str]:
        """
        Returns a list of the paths to the dependencies for the target_file
        that are inside the target directory
        """
        return [dependency for dependency in self.dependencies if dependency in self.dir_components]
    def __get_external_dependencies(self) -> Iterable[str]:
        """
        Returns a list of the dependencies (including sub-dependencies) that are
        dependencies to the file and are outside the target directory (e.x #include <vector>)
        """
        return [dependency for dependency in self.dependencies if dependency not in self.dir_components]
    def get_full_header(self) -> str:
        top_header: str = "#pragma once\n"
        includes: str = "\n".join([self.get_include(inc) for inc in self.__get_external_dependencies()])
        import_bodies: str = "\n".join([get_file_body(dep_path) for dep_path in self.__get_internal_dependencies()])
        return "\n".join([top_header, includes, import_bodies]) + "\n"

    def get_include(self, dependency: Iterable[str]) -> str:
        return f"#include <{dependency}>"
    def __merge(self, C1: Iterable[str], C2: Iterable[str]) -> Iterable[str]:
        """
        Merge two iterables, with the elements in the first getting placed before the second
        """
        merged: List[str] = []
        for c in C1:
            merged.append(c)
        for c in C2:
            merged.append(c)
        return merged
