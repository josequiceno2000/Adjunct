import os
from pathlib import Path

def write_file(working_directory, file_path, content):
    working_path_abs = Path(working_directory).resolve()
    target_file_path_abs = Path(working_directory, file_path).resolve()

    if not (str(target_file_path_abs).startswith(str(working_path_abs))):
        return f'Error: Cannot access "{file_path}" as it is outside the permitted working directory'

    if not target_file_path_abs.exists():
        try:
            os.makedirs(
                name=file_path,
                exist_ok=True)
        except Exception as e:
            return f'Error: Cannot create directories for "{file_path}": {str(e)}'
    
    try:
        with open(target_file_path_abs, 'w', encoding='utf-8') as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: Cannot write to "{file_path}": {str(e)}'
