import os
from google.genai import types

def write_file(working_directory, file_path, content):

    # get the path of the full path of the directory
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.join(working_dir_abs,file_path)

    # validate path
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    if not valid_target_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if os.path.isdir(target_dir):
        return f'Error: Cannot write to: {file_path} as it is a directory'

    # check if parent directories of file_path exists
    # if does not exist, create missing directories
    os.makedirs(name=os.path.dirname(target_dir),exist_ok=True)

    # open file
    # and overwrite its contents
    with open(target_dir,"w") as f:
        f.write(content)

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Converts the content into a string and writes the converted content into a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Which file to write into"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="What to write into the file"
            ),
        },
        required=["file_path","content"]
    ),
)