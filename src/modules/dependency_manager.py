import os
from modules.dir_parser import get_dependency_graph, get_module_graph, get_files
from modules.validate_arguments import validate_arguments
from modules.file_parser import get_file_dependencies, get_file_body, get_noninclude_headers
from modules.graph_util import  get_required_components 
from typing import List, Collection, Dict, Set, Iterable
class dependency_manager:
    """
    Manage the dependency components of a given file relative to a specific
    directory.
    """
    def __init__(self, target_dir: str, target_file: str):
        self.target_dir = target_dir
        self.target_file = target_file

        dependency_graph: Dict[str, Collection[str]] = get_dependency_graph(target_dir)
        module_graph: Dict[str, Collection[str]] = get_module_graph(target_dir)
        file_dependencies: Iterable[str] = get_file_dependencies(target_file)
        self.dependencies: Iterable[str] = get_required_components(dependency_graph, module_graph, file_dependencies)
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
        includes: str = "\n".join([self.get_include(inc) for inc in self.__get_external_dependencies()])
        non_include_headers: str = "".join(get_noninclude_headers(self.target_file))
        import_bodies: str = "\n".join([ get_file_body(os.path.join(self.target_dir, dep_path)) for dep_path in self.__get_internal_dependencies()])
        return "\n".join([includes, non_include_headers, import_bodies]) + "\n"

    def get_include(self, dependency: Iterable[str]) -> str:
        return f"#include <{dependency}>"
    def __get_unique(self, components: Collection[Collection[str]]) -> Collection[str]:
        res: Set[str] = set()
        for comp in components:
            for c in comp:
                res.add(c)
        return res
        
    def __merge(self, c1: Collection[str], c2: Collection[str]) -> Collection[str]:
        merged: List[str] = []
        for c in c1:
            merged.append(c)
        for c in c2:
            merged.append(c)
        return merged

