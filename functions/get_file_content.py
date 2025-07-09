from .config import MAX_CHARS
import os

def get_file_content(working_directory, file_path):
    try:
        dir_path = os.path.abspath(os.path.join(os.path.abspath(working_directory), file_path))
        working_dir_abs = os.path.abspath(working_directory)
        #print(os.path.join(os.path.abspath(working_directory)))
        #print(dir_path)

        if not dir_path.startswith(working_dir_abs):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(dir_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(dir_path, "r") as f:
            file_content_string = f.read()

            if len(file_content_string) > MAX_CHARS:
                file_content = file_content_string[:MAX_CHARS]
                file_content += f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            else:
                file_content = file_content_string
            
            return file_content
    except Exception as e:
        print(f"Error: {e}")