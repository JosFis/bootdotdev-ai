import os

def write_file(working_directory, file_path, content):
    try:
        dir_path = os.path.abspath(os.path.join(os.path.abspath(working_directory), file_path))
        working_dir_abs = os.path.abspath(working_directory)
        #print(os.path.join(os.path.abspath(working_directory)))
        #print(dir_path)

        if not dir_path.startswith(working_dir_abs):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(dir_path):
            os.makedirs(os.path.dirname(dir_path), exist_ok=True)

        with open(dir_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        print(f"Error: {e}")