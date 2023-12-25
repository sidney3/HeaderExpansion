import subprocess
import re
import os
from util import f_write, f_delete, d_make, cmp_strings
TEST_PATH = os.path.abspath(__file__)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(TEST_PATH)))
SCRIPT_PATH = os.path.join(PROJECT_ROOT, 'src', 'main.py')

def macro_test():
    MOCK_SRC = \
    """
#include <dependency1.cpp>
#include <dependency2.cpp>
#define HI cout << \"Hello\"

    int main()
    {
        HI;
    }
    """
    MOCK_DEP1 = \
    """
#include <dependency2.cpp>
#define HEY cout << \"Hey\"
    int do_it()
    {
        return 1 + 2;
    }
    """
    MOCK_DEP2 = \
    """
    int also_di_it()
    {
        return 2 + 3;
    }
    """
    EXPECTED_DEP: str = \
    """
#define HI cout << "Hello"
#define HEY cout << \"Hey\"

    int also_di_it()
    {
        return 2 + 3;
    }


    int do_it()
    {
        return 1 + 2;
    }



    int main()
    {
        HI;
    }
    """
    TEST_DIR_PATH = 'test_dir'
    MODULE_PATH = os.path.join(TEST_DIR_PATH, 'modules')
    d_make(TEST_DIR_PATH)
    d_make(MODULE_PATH)
    
    MOCK_SRC_FP = os.path.join(TEST_DIR_PATH, 'src.cpp')
    MOCK_DEP1_FP = os.path.join(MODULE_PATH, 'dependency1.cpp')
    MOCK_DEP2_FP = os.path.join(MODULE_PATH, 'dependency2.cpp')
    f_write(MOCK_SRC_FP, MOCK_SRC)
    f_write(MOCK_DEP1_FP, MOCK_DEP1)
    f_write(MOCK_DEP2_FP, MOCK_DEP2)
    
    subprocess.run(['python', SCRIPT_PATH, MODULE_PATH, MOCK_SRC_FP], capture_output=True, text=True)
    
    with open(MOCK_SRC_FP, 'r') as file:
        assert(cmp_strings(file.read(), EXPECTED_DEP))

def external_header_test():
    MOCK_SRC = \
    """
#include <unordered_map>
#include <dependency1.cpp>

    int main()
    {
    }
    """
    MOCK_DEP1 = \
    """
#include <string>
    int do_it()
    {
        return 1 + 2;
    }
    """
    EXPECTED_DEP: str = \
    """
    """
    TEST_DIR_PATH = 'test_dir'
    MODULE_PATH = os.path.join(TEST_DIR_PATH, 'modules')
    d_make(TEST_DIR_PATH)
    d_make(MODULE_PATH)
    
    MOCK_SRC_FP = os.path.join(TEST_DIR_PATH, 'src.cpp')
    MOCK_DEP1_FP = os.path.join(MODULE_PATH, 'dependency1.cpp')
    f_write(MOCK_SRC_FP, MOCK_SRC)
    f_write(MOCK_DEP1_FP, MOCK_DEP1)
    
    subprocess.run(['python', SCRIPT_PATH, MODULE_PATH, MOCK_SRC_FP], capture_output=True, text=True)
    
    with open(MOCK_SRC_FP, 'r') as file:
        assert(cmp_strings(file.read(), EXPECTED_DEP))
# TODO: test with default imports
if __name__ == "__main__":
    macro_test()
