from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python import run_python_file
from functions.write_file import write_file

func_dict = {
    "write_file" : write_file,
    "run_python_file" : run_python_file,
    "get_file_content" : get_file_content,
    "get_files_info" : get_files_info
}