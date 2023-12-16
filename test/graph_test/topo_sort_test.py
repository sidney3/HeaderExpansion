import os
import sys
script_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(script_path)))
sys.path.append(project_root)

from src.modules import graph_util

    
