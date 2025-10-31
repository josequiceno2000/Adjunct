import os
from google.genai import types
from pathlib import Path

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

def get_files_info(working_directory, directory="."):
    working_path_abs = Path(working_directory).resolve()
    target_path_abs = Path(working_directory, directory).resolve()
    
    if not (str(target_path_abs).startswith(str(working_path_abs))):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not target_path_abs.is_dir():
        return f'Error: "{directory}" is not a directory'
    
    directory_name = target_path_abs.name
    
    files_list = [f"Result for {directory_name}:"]

    try:
        for file in os.listdir(target_path_abs):
            file_path = target_path_abs / file
            file_size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)

            files_list.append(f"- {file}: file_size={file_size} bytes, is_dir={is_dir}")
        
        return "\n".join(files_list) if files_list else "Directory is empty."
        
    
    except Exception as e:
        return f"Error: {str(e)}"