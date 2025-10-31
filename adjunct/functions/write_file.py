import os
from google.genai import types
from pathlib import Path

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file, creating directories if necessary.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    working_path_abs = Path(working_directory).resolve()
    target_file_path_abs = Path(working_directory, file_path).resolve()

    if not str(target_file_path_abs).startswith(str(working_path_abs)):
        return f'Error: Cannot access "{file_path}" as it is outside the permitted working directory'

    target_dir_abs = target_file_path_abs.parent
    
    if not target_dir_abs.exists():
        try:
            os.makedirs(
                name=target_dir_abs,
                exist_ok=True
            )
        except Exception as e:
            return f'Error: Cannot create directories for "{file_path}": {str(e)}'
            
    try:
        with open(target_file_path_abs, 'w', encoding='utf-8') as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: Cannot write to "{file_path}": {str(e)}'
