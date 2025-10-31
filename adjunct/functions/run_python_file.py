import os
import subprocess
from google.genai import types
from pathlib import Path

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file", # 💡 Changed name to reflect file execution
    description="Runs a given Python file with optional arguments and returns its output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="List of arguments (strings) to pass to the Python file when executing.",
                # 🛠️ FIX: An ARRAY type MUST specify the type of its items
                items=types.Schema(
                    type=types.Type.STRING 
                )
            ),
        },
        # Assuming file_path is required, which is typical for running a file
        required=["file_path"],
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    working_path_abs = Path(working_directory).resolve()
    target_file_path_abs = Path(working_directory, file_path).resolve()

    if not (str(target_file_path_abs).startswith(str(working_path_abs))):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not target_file_path_abs.exists():
        return f'Error: "{file_path}" not found.'
    
    if not target_file_path_abs.suffix == '.py':
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        completed_process = subprocess.run(
            args=['python', str(target_file_path_abs)] + args,
            capture_output=True,
            text=True,
            cwd=str(working_path_abs),
            timeout=30
        )

        if not completed_process.stdout and not completed_process.stderr:
            return "No output produced."
        

        result_string =  f'STDOUT: {completed_process.stdout.strip()}\nSTDERR: {completed_process.stderr.strip()}'

        if completed_process.returncode != 0:
            result_string += f'\nProcess exited with return code {completed_process.returncode}.'
        
        return result_string
    
    except Exception as e:
        return f"Error: executing Python file: {str(e)}"