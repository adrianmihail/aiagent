import os

def run_python_file(working_directory, file_path, args=None):

    # get the path of the full path of the directory
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.join(working_dir_abs,file_path)

    # validate path
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    if not valid_target_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if os.path.isfile(target_dir):
        return f'Error: Cannot write to: {file_path} as it is a directory'

    return None