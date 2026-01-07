import os
import subprocess

def run_python_file(working_directory, file_path, args=None):

    # get the path of the full path of the directory
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs,file_path))

    # validate path
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    if not valid_target_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_dir):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    if file_path[-3:] != ".py":
        return f'Error: "{file_path}" is not a Python file'
    
    # use subprocess to run the file
    command = ["python", target_dir]
    # check for additional args
    # and add them to the command list
    if args:
        command.extend(args)     

    complete_command = subprocess.run(command,cwd=working_directory,capture_output=True,text=True,timeout=30)

    output_string = ""

    if complete_command.stdout.strip() != "":
        output_string += f"STDOUT: {complete_command.stdout}\n"

    if complete_command.stderr.strip() != "":
        output_string += f"STDERR: {complete_command.stderr}\n"

    if complete_command.stdout.strip() == "" and complete_command.stderr.strip() == "":
        output_string = f"No output produced\n"

    if complete_command.returncode != 0:
        output_string += f"Process exited with code {complete_command.returncode}"
    
    return output_string