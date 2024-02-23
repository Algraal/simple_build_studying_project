import os
import shutil

# Checks if provided path is existing directory. Returns True in success
# otherwise False
def is_directory(directory_name: str) -> bool:
    directory_name = os.path.abspath(directory_name)
    return os.path.exists(directory_name) and os.path.isdir(directory_name)
# Removes passed directory, if removed succesfully return True
# otherwise False
def remove_directory(directory_name: str) -> bool:
    try:
        shutil.rmtree(directory_name)
        print("Previous build was removed.")
        return True
    except Exception as e:
        print(f"Error: directory cannot be removed {e}.")
        return False
