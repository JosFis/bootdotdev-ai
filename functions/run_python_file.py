import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file at the given path using the 'uv' runner and returns its output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the Python file to execute.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of command-line arguments to pass to the Python file.",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try:
        dir_path = os.path.abspath(os.path.join(os.path.abspath(working_directory), file_path))
        working_dir_abs = os.path.abspath(working_directory)
        #print(os.path.join(os.path.abspath(working_directory)))
        #print(dir_path)

        if not dir_path.startswith(working_dir_abs):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(dir_path):
            return f'Error: File "{file_path}" not found.'
        if not dir_path.lower().endswith(('.py')):
            return f'Error: "{file_path}" is not a Python file.'
        
        #return_value = subprocess.run(["uv","run",dir_path], timeout=30, capture_output=True, cwd=working_dir_abs)
        commands = ["uv", "run", dir_path]
        if args:
            commands.extend(args)
        result = subprocess.run(
            commands,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=working_dir_abs,
        )

        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")

        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        return "\n".join(output) if output else "No output produced."
    except Exception as e:
        print(f"Error: executing Python file: {e}")