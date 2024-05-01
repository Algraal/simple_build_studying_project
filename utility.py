import os
import shutil
from typing import List, Tuple


def is_directory(directory_name: str) -> bool:
    """
    Checks if the provided path exists and corresponds to a directory.
    Directory path should be joined with os.path.join

    Parameters:
        directory_name (str): The path to check.

    Returns:
        bool: True if the path exists and is a directory, False otherwise.    """
    try:
        directory_path: str = os.path.abspath(directory_name)
        return os.path.exists(directory_path) and os.path.isdir(directory_path)
    # Other exceptions are not explicitly raised
    except OSError as e:
        # Raises OS error again
        raise e


def is_file(file_name: str) -> bool:
    """
    Checks if the provided path exists and corresponds to a file. Filename
    should be joined with os.path.join.
    Parameters:
        file_name (str): The filename to be checled.

    Returns:
        bool: True if the path exists and is a file, False otherwise.
    """
    try:
        file_path: str = os.path.abspath(file_name)
        return os.path.exists(file_path) and os.path.isfile(file_path)
    except OSError as e:
        print(f"Error is_file {e}")
        raise e


def remove_directory(directory_name: str) -> bool:
    """
    Removes the specified directory and all its contents.

    Parameters:
        directory_name (str): the path of the directory to remove.

    Returns:
        bool: True if the directory was successfully removed, False otherwise.
    """
    try:
        directory_path: str = os.path.abspath(directory_name)
        shutil.rmtree(directory_path)
        print("Previous build was removed.")
    except OSError as e:
        print(f"Error remove_directory: {e}")
        raise e


def move_to_dir(ending: str) -> bool:
    """
    Checks if the current current directory is insed a standard c++ project
    structure. It it is, the function moves (or stays) to the path with the
    specified ending as a tail.

    Parameters:
        ending (str): The tail of the path where the process should move

    Returns:
        bool: True if the current directory is already the specified path,
        or if it successfully moves to the specified ending, False otherwise.
    """
    try:
        path: Tuple[str, str] = os.path.split(os.getcwd())
        # Case process is already in the required directory
        if path[1] == ending:
            return True
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


def find_index_with_substring(str_list: List[str], substr: str) -> int | None:
    """
    Finds tje index of the first string in the given list that ends with the
    specified substring.

    Parameters:
        str_list (List[str]): A list of string to search through.
        substr (str): The substring to search for at the end of each string

    Returns:
        int | None: The index of the first string that ends with the specified
            substring or None if no such string is found.
    """
    for index, string in enumerate(str_list):
        if string.endswith(substr):
            return index
    return None
