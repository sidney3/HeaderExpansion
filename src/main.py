import sys
from modules.file_parser import get_file_dependencies
from modules.validate_arguments import validate_arguments

NUM_ARGS = 2

if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise Exception("expected 2 arguments")
    root_dir, target_file = sys.argv
    validate_arguments(root_dir, target_file)
