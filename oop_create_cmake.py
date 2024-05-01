import os
from typing import List, Dict
from utility import move_to_dir, find_index_with_substring, is_directory


class CmakeGenerator:
    # Default standards for c++ and c
    C_STANDARD: str = ("set(CMAKE_C_STANDARD_REQUIRED ON)\n"
                       "set(CMAKE_C_STANDARD 99)\n")
    CXX_STANDARD: str = ("set(CMAKE_CXX_STANDARD REQUIRED ON)\n"
                         "set(CMAKE_CXX_STANDARD 17)\n")
    # Expected that all sources of a project have the same extension as the
    # main source file
    POSSIBLE_MAIN_SOURCES: Dict[str, List[str]] = {
            "main.cpp": [".cpp", CXX_STANDARD],
            "main.cxx": [".cxx", CXX_STANDARD],
            "main.CPP": [".CPP", CXX_STANDARD],
            "main.c++": [".c++", CXX_STANDARD],
            "main.c": [".c", C_STANDARD]
            }
    # Stores all files from src directory
    __raw_src_list: List[str] = []
    __language_extensions: List[str] = None
    __language_standards: List[str] = None
    __src_list: List[str] = []
    __cmake_content: str = None

    # Creates list of files in a directory that can be used for
    # compiling/setting up programm.
    def list_files(self) -> None:
        """
        Fetches all files in src directory. Stores them to the private property
        __raw_src_list.

        Returns:
            None: empty __raw_src_list is not an error but a case that should
                be handled.
        """
        self.__raw_src_list += [os.path.join(os.getcwd(), file) for file in
                                os.listdir()]
        return None

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
                if filename.endswith("/" + possible_src):
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

    # Generates CMakeLists.txt
    def generate_cmake(self) -> bool:
        if not self.fetch_src_files():
            return False
        if not self.create_src_list():
            return False

        try:
            filehandler = open("CMakeLists.txt", "w", encoding="utf-8")
            filehandler.write(self.__cmake_content)
            filehandler.close()
        except Exception as e:
            print(f'Error: {e}')
            return False

    # Fills content string used for initializing CMakeLists.txt using values
    # from private properties of CmakeGenerator instance
    def fill_content(self) -> bool:

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
        self.__cmake_content += (f'add_executable({project_name}'
                                 f'{src_string}\n)')

        # At that moment process is located in "src" directory of the project
        # But CmakeLists.txt should be located inside of the project root
        # directory
        try:
            os.chdir(os.path.pardir())
            # Include "include" directory if it exists
            if is_directory(os.path.join(os.getcwd(), "include")):
                self.__cmake_content += ("target_include_directories("
                                         f"{project_name}")
                self.__cmake_content += ("PUBLIC \"{CMAKE_SOURCE_DIR}/"
                                         "include\")\n")
        except OSError as e:
            print(f"Error fill_content: {e}")
        finally:
            return True
