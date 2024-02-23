import os
import shutil
import subprocess
import sys
import re
from utility import is_directory, remove_directory

# Class that has methods and properties to handle building project
class Project:
    __executable_name: str
    __project_name: str
    __current_location: str
    __root_directory: str
    # Directory with this const variable is considered root
    PROJECT_ROOT_FILE = "CMakeLists.txt"
    PATTERN_PROJECT_NAME = r"add_executable\((\w+)"
    PATTERN_EXECUTABLE_NAME = r"project\s*\(\s*([^\s]+)"

    def __init__(self) -> None:
        # sets initial values of object using CMakeList.txt
        self.__executable_name = ""
        self.__project_name = ""
        self.__current_location = os.path.abspath(os.getcwd())
        self.__root_directory = ""
        user_path = input("Enter path to a project`s root directory, "\
                         "enter empty string for autosearch: ")
        if user_path == "":
            self.find_root_directory()
        else:
            self.check_if_root_directory(user_path)
        if self.__root_directory == "":
            print("Error: directory has not been found.")
            return None
        if not self.move_to_directory(self.__root_directory):
            print("Error: cannot move to the root directory.")
            return None
        self.__project_name = self.find_in_cmake(self.PATTERN_PROJECT_NAME)
        self.__executable_name = self.find_in_cmake(self.PATTERN_EXECUTABLE_NAME)
        if not self.__executable_name or not self.__project_name:
            print("Error: project name or executable name has not been found.")
            return None
        print(self.__root_directory, self.__current_location,
              self.__project_name, self.__executable_name)
        return None
    # Creates build directory, if exists removes it completly and creates
    # another one
    def create_build_directory(self, dir_build) -> bool:
        if self.__current_location != self.__root_directory:
            if self.move_to_directory(self.__root_directory):
                return False
        # Absolute path to expected directory for build
        path_to_dir_build = os.path.abspath(os.path.join(os.getcwd(), dir_build))
        if is_directory(path_to_dir_build):
            if not remove_directory(path_to_dir_build):
                return False
        try:
            os.mkdir(path_to_dir_build)
            return True
        except Exception as e:
            print(f"Error: creating {dir_build} directory {e}.")
            return False

    # Looks in CMakeLists.txt using provided pattern
    def find_in_cmake(self, pattern: str) -> str:
        try:
            if self.__current_location != self.__root_directory:
                if not self.move_to_directory(self.__root_directory):
                    return None
            filehandler = open(self.PROJECT_ROOT_FILE, 'r', encoding='utf-8')
            content = filehandler.read()
            match = re.search(pattern, content)
            filehandler.close()
            if not match:
                print("Error: Could not get project name. Aborting...")
                return None
            search_result = match.group(1)
            return search_result
        except Exception as e:
            print(f"Error. Binary was not found: {e}")
            return None
    # Checks if provided name is a root directory, sets property 
    # __root_directory. Returns True on success, otherwise returns False
    # sets __root_directory to emprty string
    def check_if_root_directory(self, directory_path) -> bool:
        try:
            directory_path = os.path.abspath(directory_path)
            if not is_directory(directory_path):
                self.__root_directory = ""
                return False
            files = os.listdir(directory_path)
            if self.PROJECT_ROOT_FILE in files:
                self.__root_directory = directory_path
                return True
            return False
        except Exception as e:
            print(f"Error is_directory: {e}")
            return False

    # Checks if the current or a parent directories is project`s root 
    # directory, (directory with CMakeLists.txt is considered the project 
    # root directory) sets __root_directory. Returns True on success, 
    # otherwise False
    def find_root_directory(self) -> bool:
        # List of files in the current directory
        try:
            current_dir_files = os.listdir()
        except Exception as e:
            print(f"Error listing files: {e}")
            return False
        if self.PROJECT_ROOT_FILE in current_dir_files:
            self.__root_directory = os.path.abspath(os.getcwd())
            return True
        # Platform independent way of getting list of files 
        # in a previous directory
        try:
            parent_directory_path = os.path.abspath(os.path.join(os.getcwd(),
                                                os.pardir))
        except Exception as e:
            print("Error find_root_directory: {e}.")
            return False
        try:
            previous_dir_files = os.listdir(parent_directory_path)
        except Exception as e:
            print(f"Error listing files: {e}")
            return False

        if self.PROJECT_ROOT_FILE in previous_dir_files:
            self.__root_directory = parent_directory_path
            return True
        print(f"Error: {self.PROJECT_ROOT_FILE} was not found")
        return False
    # Moves to passed directory, changes __curent_position property of an object
    # Returns True on Success, otherwise False
    def move_to_directory(self, directory_name: str) -> bool:
        directory_name = os.path.abspath(directory_name)
        try:
            if is_directory(directory_name):
                os.chdir(directory_name)
                self.__current_location = os.path.abspath(os.getcwd())
                return True
            else:
                print(f"Error move_to_directory: {directory_name} is not a directory")
                return False
        except Exception as e:
            print(f"Error move_to_directory: {e}")
        return False
