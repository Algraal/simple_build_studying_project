import os
import shutil
import sys
import subprocess
import re
from typing import List
from utility import is_directory, is_file, remove_directory


# Class that has methods and properties to handle building project
class Project:
    __executable_name: str
    __project_name: str
    __current_location: str
    __root_directory: str
    __build_directory: str
    __userpath: str
    # Directory with this const variable is considered root
    PROJECT_ROOT_FILE = "CMakeLists.txt"
    PATTERN_PROJECT_NAME = re.compile(r"add_executable\((\w+)\s")
    PATTERN_EXECUTABLE_NAME = re.compile(r'add_executable\((\w+)')

    def __init__(self, path: str = "") -> None:
        try:
            # sets initial values of object using CMakeList.txt
            self.__executable_name = ""
            self.__project_name = ""
            self.__current_location = os.path.abspath(os.getcwd())
            self.__root_directory = ""
            self.__build_directory = ""
            self.__user_path = path
            if self.__user_path == "":
                self.find_root_directory()
            else:
                self.check_if_root_directory(self.__user_path)

            if not self.__root_directory:
                raise ValueError("Error: could not find root directory.")

            if self.__root_directory != self.__current_location:
                self.move_to_directory(self.__root_directory)

            self.__project_name = self.find_in_cmake(self.PATTERN_PROJECT_NAME)
            self.__executable_name = \
                self.find_in_cmake(self.PATTERN_EXECUTABLE_NAME)

            if not self.__executable_name or not self.__project_name:
                raise ValueError("Project name or executable name not found.")

            print(self.__root_directory, self.__current_location,
                  self.__project_name, self.__executable_name)
            return None

        except Exception as e:
            raise ValueError(f"Error during project initialization: {e}")

    # Creates build directory, if exists removes it completly and creates
    # another one
    def create_build_directory(self, dir_build) -> None:
        try:
            if self.__current_location != self.__root_directory:
                self.move_to_directory(self.__root_directory)
            # Absolute path to expected directory for build
            path_to_dir_build = os.path.join(self.__current_location,
                                             dir_build)
            if is_directory(path_to_dir_build):
                remove_directory(path_to_dir_build)
            os.mkdir(path_to_dir_build)
            self.__build_directory = path_to_dir_build
        except Exception as e:
            raise ValueError(f"Error: creating {dir_build} directory {e}")

    # Looks in CMakeLists.txt using provided pattern
    def find_in_cmake(self, pattern: str) -> str:
        try:
            if self.__current_location != self.__root_directory:
                self.move_to_directory(self.__root_directory)

            with open(self.PROJECT_ROOT_FILE, 'r', encoding='utf-8') as filehandler:
                content = filehandler.read()

            match = re.search(pattern, content)

            if not match:
                raise ValueError(f"Pattern not found in {self.PROJECT_ROOT_FILE}.")

            search_result = match.group(1)
            return search_result
        except FileNotFoundError:
            print(f"File {self.__PROJECT_ROOT_FILE} not found. Aborting")
            # Is not a error of script execution
            sys.exit(0)
        except OSError:
            # Permission error, isADirectoryError e.t.c.
            print(f"OS error occured to open {self.__PROJECT_ROOT_FILE}")
            sys.exit(0)

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
            raise ValueError(f"Error in check_if_root_directory: {e}")

    # Checks if the current or a parent directories is project`s root
    # directory, (directory with CMakeLists.txt is considered the project
    # root directory) sets __root_directory. Aborts script if root directory
    # can not be found or system error appeared.
    def find_root_directory(self) -> None:
        # List of files in the current directory
        try:
            current_dir_files = os.listdir()

            if self.PROJECT_ROOT_FILE in current_dir_files:
                self.__root_directory = os.path.abspath(os.getcwd())
                return None
        # Platform independent way of getting list of files
        # in a previous directory
            parent_directory_path = os.path.abspath(os.path.join(os.getcwd(),
                                                    os.pardir))
            previous_dir_files = os.listdir(parent_directory_path)

            if self.PROJECT_ROOT_FILE in previous_dir_files:
                self.__root_directory = parent_directory_path
                return None 
            else:
                print(f"{self.PROJECT_ROOT_FILE} was not found in current or"
                      "parent directory. Aborting")
                return sys.exit(0)
        except OSError as e:
            print("System error appeared during indexing files in "
                  f"find_root_directory: {e}. Aborting")
            return sys.exit(0)

    # Moves to passed directory, changes __curent_position property of an object
    # Returns True on Success, otherwise False
    def move_to_directory(self, directory_name: str) -> None:
        try:
            directory_name = os.path.abspath(directory_name)

            if is_directory(directory_name):
                os.chdir(directory_name)
                self.__current_location = os.path.abspath(os.getcwd())
                return None
            else:
                raise ValueError(f"Error: {directory_name} is not a directory.")
        except Exception as e:
            raise ValueError(f"Error in move_to_directory: {e}")

    # Runs cmake to get Makefile done
    def run_cmake(self) -> None:
        try:
            if self.__current_location != self.__build_directory:
                self.move_to_directory(self.__build_directory)
            subprocess.run(['cmake', '..'], check=True)
            print(f"Cmake configuration in {self.__build_directory} "\
                  "is completed.")
            self.move_to_directory(self.__root_directory)
        except Exception as e:
            raise ValueError(f"Error in run_cmake: {e}")

    # Builds using Makefile 
    def complete_building(self) -> None:
        try:
            if self.__current_location != self.__build_directory:
                self.move_to_directory(self.__build_directory)
            subprocess.run(['cmake', '--build', '.'], check=True)
            # Creates path to expected old executable to remove it before
            # moving new executable to that directory
            path_to_executable = os.path.join(self.__root_directory, "bin",
                                              self.__executable_name)
            if is_file(path_to_executable):
                os.remove(path_to_executable)
            shutil.move(self.__executable_name, path_to_executable)
            self.move_to_directory(self.__root_directory)
            # Symblink to compiler datebase for clangd autocomplete
            subprocess.run(["ln", "-s", os.path.join(self.__build_directory, \
                            "compile_commands.json"), "compile_commands.json"])
        except Exception as e:
            raise ValueError(f"Error in complete_building: {e}")
    
    # Runs built program in bin directory
    def run_build(self, args: List[str] = []) -> None:
        try:
            if self.__current_location != self.__root_directory:
                self.move_to_directory(self.__root_directory)
            path_to_executable = os.path.abspath(
                    os.path.join(self.__root_directory, 'bin',
                                 self.__executable_name))
            if is_file(path_to_executable):
                print(f"Program {self.__executable_name} is started.")
                # Creates list what will be passed to execve call
                path_args_list = [path_to_executable] + args
                subprocess.run(path_args_list, check = True)
            else:
                raise ValueError("Error: executable file does not exist")
        except Exception as e:
            raise ValueError(f"Error in run_build: {e}")
