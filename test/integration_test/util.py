
import os
import re
def f_write(file_path: str, to_write: str):
    with open(file_path, 'w') as file:
        file.write(to_write)
def f_delete(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)
def d_make(directory_path: str):
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)
def cmp_strings(s1, s2):
    s1_no_whitespace = re.sub(r'\s+', '', s1)
    s2_no_whitespace = re.sub(r'\s+', '', s2)
    return s1_no_whitespace == s2_no_whitespace
