import os
from pathlib import Path

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    working_path_abs = Path(working_directory).resolve()
    target_file_path_abs = Path(working_directory, file_path).resolve()
    
    if not (str(target_file_path_abs).startswith(str(working_path_abs))):
        return f'Error: Cannot access "{file_path}" as it is outside the permitted working directory'

    if not target_file_path_abs.is_file():
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(target_file_path_abs, 'r', encoding='utf-8') as file:
            file_content_str = file.read(MAX_CHARS)
            if len(file.read()) > MAX_CHARS:
                return f'{file_content_str}\n\n[...File "{file_path}" truncated at {MAX_CHARS} characters].'
        return file_content_str
    
    except Exception as e:
        return f"Error: {str(e)}"