import os
import shutil
from typing import List, Tuple


# Checks if provided path is existing directory. Returns True on success
# otherwise False
def is_directory(directory_name: str) -> bool:
    try:
        directory_name = os.path.abspath(directory_name)
        return os.path.exists(directory_name) and os.path.isdir(directory_name)
    # Other exceptions are not explicitly raised
    except OSError as e:
        # Raises OS error again
        raise e


# Checks of provided path is existing file
def is_file(file_name: str) -> None:
    try:
        file_name = os.path.abspath(file_name)
        return os.path.exists(file_name) and os.path.isfile(file_name)
    except OSError as e:
        raise e


# Removes passed directory, if removed succesfully return True
# otherwise False
def remove_directory(directory_name: str) -> bool:
    try:
        shutil.rmtree(directory_name)
        print("Previous build was removed.")
    except Exception as e:
        raise ValueError(f"Error: directory cannot be removed {e}.")


# Function checks if it is inside standard c++ project. If true moves/stays to
# passed directory and return True, otherwise returns False
def move_to_dir(ending: str) -> bool:
    # Current location is not src directory
    try:
        path: Tuple[str, str] = os.path.split(os.getcwd())
        # Case process is already in the required directory
        if path[1] == ending:
            return True
        else:
            target_path: str = os.path.join(os.getcwd(), ending)
            # case we are in a root directory of a project
            if is_directory(target_path):
                os.chdir(target_path)
                return True
            # case we are in a nested directory of a project
            else:
                from_nested: str = os.path.join(os.path.pardir, ending)
                if is_directory(from_nested):
                    os.chdir(from_nested)
                    return True
        return False
    except OSError as e:
        print(f"Error move_to_dir: {e}")
        raise e
    except ValueError as e:
        print(f"Error move_to_dir: {e}")
        raise e
    except TypeError as e:
        print(f"Error move_to_dir: {e}")
        raise e


# Function looks for an index of a string that ends with passed substring in
# a provided list
def find_index_with_substring(str_list: List[str], substr: str) -> int | None:
    for index, string in enumerate(str_list):
        if string.endswith(substr):
            return index
    return None
