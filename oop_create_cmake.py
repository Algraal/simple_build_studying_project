import os
from typing import List, Dict, Tuple
from utility import move_to_dir, find_index_with_substring, is_directory


class CmakeGenerator:
    """
    A class to generate CMakeLists.txt for a C++ project based on the project's
    source files.

    Attributes:
        C_STANDARD (str): Default C standard for the project.
            CXX_STANDARD (str): Default C++ standard for the project.
        POSSIBLE_MAIN_SOURCES (Dict[str, Tuple[str]]): Dictionary mapping main
            source file names to their extensions and standards.
        __raw_src_list (List[str]): List to store raw source files from the
            'src' directory.
        __language_extensions (List[str]): List to store language extensions
            of the project.
        __language_standards (List[str]): List to store language standards
            of the project.
        __src_list (List[str]): List to store proper source files
            of the project.
        __cmake_content (str): String to store the content of the
            CMakeLists.txt file.
    """
    # Default standards for c++ and c
    C_STANDARD: str = ("set(CMAKE_C_STANDARD_REQUIRED ON)\n"
                       "set(CMAKE_C_STANDARD 99)\n")
    CXX_STANDARD: str = ("set(CMAKE_CXX_STANDARD REQUIRED ON)\n"
                         "set(CMAKE_CXX_STANDARD 17)\n")
    # Expected that all sources of a project have the same extension as the
    # main source file
    POSSIBLE_MAIN_SOURCES: Dict[str, Tuple[str]] = {
            "main.cpp": (".cpp", CXX_STANDARD),
            "main.cxx": (".cxx", CXX_STANDARD),
            "main.CPP": (".CPP", CXX_STANDARD),
            "main.c++": (".c++", CXX_STANDARD),
            "main.c": (".c", C_STANDARD)
            }
    # Stores all files from src directory
    __raw_src_list: List[str] = []
    __language_extensions: List[str] = []
    __language_standards: List[str] = []
    __src_list: List[str] = []
    __cmake_content: str = ""

    # Creates list of files in a directory that can be used for
    # compiling/setting up programm.
    def list_files(self) -> None:
        """
        Fetches all files in current directory. Stores them to the private
        property __raw_src_list.

        Returns:
            None: empty __raw_src_list is not an error but a case that should
                be handled.
        """
        try:
            dir_name: str = os.path.basename(os.getcwd())
            self.__raw_src_list += [os.path.join(dir_name, file) for file in
                                    os.listdir()]
        except OSError as e:
            raise e

    def fetch_src_files(self) -> bool:
        """
        Fetches source files from the 'src' directory matching the extension of
        the main source file.

        Returns:
            bool: True if source files are fetched successfully,
                False otherwise.
        """
        try:
            if move_to_dir("src"):
                # Successfully moved to src directory
                self.list_files()
            else:
                return False
        except OSError as e:
            print(f"Error fetch_src_files: {e}")
            return False
        except ValueError as e:
            print(f"Error fetch_src_files: {e}")
            return False
        except TypeError as e:
            print(f"Error fetch_src_files: {e}")
            return False

        # Looks for main src from directory src in predefined Dict to find out
        # extenson of file in the project
        for filename in self.__raw_src_list:
            for possible_src, extension in self.POSSIBLE_MAIN_SOURCES.items():
                # Tail in this conext will be file name
                file_tail: str = os.path.split(filename)[1]
                if file_tail == possible_src:
                    # 0th element is a extension, 1th standard
                    self.__language_extensions.append(extension[0])
                    self.__language_standards.append(extension[1])
                    break
        # Checks if only one main was found
        if len(self.__language_extensions) < 1:
            print("Main src was not found.")
            return False
        if len(self.__language_extensions) > 1:
            print("Few main sources were found.")
            return False
        return True

    def create_src_list(self) -> bool:
        """
        Appends the proper sources to the private field '__src_list' and
        returns True. If multiple or no main
        source files are found, returns False and does not modify '__src_list'.

        Returns:
            bool: True if proper list of sources is created, otherwise False.
        """
        for file in self.__raw_src_list:
            if file.endswith(self.__language_extensions[0]):
                self.__src_list.append(file)
        # Clears list, it will not be used anymore
        self.__raw_src_list.clear()

        # Moves main source file in the begging of the list
        element_to_move: str = "main" + self.__language_extensions[0]
        src_index: int = find_index_with_substring(self.__src_list,
                                                   element_to_move)
        # Impossible case
        if src_index is None:
            return False
        element_to_move = self.__src_list.pop(src_index)
        self.__src_list.insert(0, element_to_move)
        return True

    def generate_cmake(self) -> bool:
        """
        Generates the CMakeLists.txt file for the project based on the
            source files.

        Returns:
            bool: True if CMakeLists.txt is successfully generated, False
                    otherwise.
        """
        if not self.fetch_src_files():
            return False
        if not self.create_src_list():
            return False

        try:
            # Moves to the project root directory from src
            os.chdir(os.path.pardir)
            self.fill_content()
            filehandler = open("CMakeLists.txt", "w", encoding="utf-8")
            filehandler.write(self.__cmake_content)
            filehandler.close()
            return True
        except Exception as e:
            print(f'Error: {e}')
            return False

    def fill_content(self) -> None:
        """
        Fills the __cmake_content string with project-related Cmake commands.

        Returns:
            None
        """
        src_string: str = '\n\t'.join(self.__src_list)
        # Do not need anymore
        self.__src_list.clear()
        # Prompts for project name (MB should be reimplemented to get project
        # name from args)
        project_name: str = input("Enter project name: ")
        self.__cmake_content = 'cmake_minimum_required(VERSION 3.27)\n'
        self.__cmake_content += f'project({project_name})\n'

        # Sets default standard based on __language_extensions
        self.__cmake_content += self.__language_standards[0]
        # Turns on option to create compile_commands.txt for clangd
        self.__cmake_content += 'set(CMAKE_EXPORT_COMPILE_COMMANDS ON)\n'
        # Adds precompiler definitions
        self.__cmake_content += 'add_definitions(-DSOME_DEFINITION)\n'
        # I think it is better to directly list all source files than use
        # "${CMAKE_SOURCE_SIR}/src/*.cpp". If sources are listed explicitly
        # is it easier to exclude sources that should
        # not be used in compilation
        self.__cmake_content += (f'add_executable({project_name} '
                                 f'{src_string}\n)\n')
        try:
            # Include "include" directory if it exists
            if is_directory(os.path.join(os.getcwd(), "include")):
                self.__cmake_content += f"target_include_directories({project_name} "
                self.__cmake_content += "PUBLIC \"{CMAKE_SOURCE_DIR}/include\")\n"
            else:
                print("Include directory was not found.")
        except OSError as e:
            print(f"Error fill_content: {e}")
