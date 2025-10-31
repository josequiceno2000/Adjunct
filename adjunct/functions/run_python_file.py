import os
import subprocess
from pathlib import Path

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