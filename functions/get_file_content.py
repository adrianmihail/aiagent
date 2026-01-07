import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        # get the path of the full path of the directory
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.join(working_dir_abs,file_path)

        # validate path
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_dir):
            return f'Error: File not found or is not a regular file: {file_path}'

        # read file until configurable limit
        content = open(target_dir).read(MAX_CHARS)
        # check if file was larger than limit
        if open(target_dir).read(1):
            content += f'\n[... File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content
    except:
        return "Error: something went wrong"