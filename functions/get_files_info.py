import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory=None):
    dir_path = os.path.abspath(os.path.join(os.path.abspath(working_directory), directory))
    working_dir_abs = os.path.abspath(working_directory)
    #print(f"dir: {dir_path}")
    #print(f"working dir: {working_dir_abs}")
    #print(dir_path.startswith(working_dir_abs))

    if not dir_path.startswith(working_dir_abs):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(dir_path):
        return f'Error: "{directory}" is not a directory' 

    strings = []
    for file_obj in os.listdir(dir_path):
        name = file_obj
        file_path = os.path.abspath(os.path.join(os.path.abspath(dir_path), file_obj))
        #print(file_path)
        is_dir = os.path.isdir(file_path)
        size = os.path.getsize(file_path)
        strings.append(f"- {file_obj}: file_size={size} bytes, is_dir={is_dir}")
        
    return "\n".join(strings)