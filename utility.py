import os
import shutil

# Checks if provided path is existing directory. Returns True in success
# otherwise False
def is_directory(directory_name: str) -> bool:
    try:
        directory_name = os.path.abspath(directory_name)
        return os.path.exists(directory_name) and os.path.isdir(directory_name)
    except Exception as e:
        raise ValueError(f"Error in is_directory: {e}")
# Checks of provided path is existing file
def is_file(file_name: str) -> bool:
    try:
        file_name = os.path.abspath(file_name)
        return os.path.exists(file_name) and os.path.isfile(file_name)
    except Exception as e:
        raise ValueError(f"Error in is_file: {e}")
# Removes passed directory, if removed succesfully return True
# otherwise False
def remove_directory(directory_name: str) -> None:
    try:
        shutil.rmtree(directory_name)
        print("Previous build was removed.")
    except Exception as e:
        raise ValueError(f"Error: directory cannot be removed {e}.")
