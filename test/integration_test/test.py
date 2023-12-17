import subprocess
import re
import os
import sys
script_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(script_path)))
# from src import main

MOCK_SRC = \
"""
#include <vector>
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
#include <string>
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
#include <vector>
#include <string>
#define HI cout << "Hello"


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
def run_full_cycle():
    if not os.path.exists('test_dir'):
        os.mkdir('test_dir')
    if not os.path.exists('test_dir/modules'):
        os.mkdir('test_dir/modules')
    
    with open('test_dir/src.cpp', 'w') as file:
        file.write(MOCK_SRC)
    with open('test_dir/modules/dependency1.cpp', 'w') as file:
        file.write(MOCK_DEP1)
    with open('test_dir/modules/dependency2.cpp', 'w') as file:
        file.write(MOCK_DEP2)
    
    script_path = os.path.join(project_root, 'src', 'main.py')
    src_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_dir', 'src.cpp')
    dep_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_dir', 'modules')
    print(script_path, src_file_path, dep_file_path)

    subprocess.run(['python', script_path, dep_file_path, src_file_path], capture_output=True, text=True)
    
    with open('test_dir/src.cpp', 'r') as file:
        assert(cmp_strings(file.read(), EXPECTED_DEP))
def cmp_strings(s1, s2):
    s1_no_whitespace = re.sub(r'\s+', '', s1)
    s2_no_whitespace = re.sub(r'\s+', '', s2)
    return s1_no_whitespace == s2_no_whitespace

if __name__ == "__main__":
    run_full_cycle()
