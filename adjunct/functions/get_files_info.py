import os

def get_files_info(working_directory, directory="."):
    if not os.path.isabs(directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.exists(os.path.join(working_directory, directory)):
        return f'Error: "{directory}" is not a directory'
    
    full_path = os.path.join(working_directory, directory)

    for file in os.listdir(full_path):
        file_path = os.path.join(full_path, file)
        file_size = os.path.get_size(file_path)
        is_dir = os.path.isdir(file_path)

        print(f"{file}: file_size={file_size} bytes, is_dir={is_dir}")