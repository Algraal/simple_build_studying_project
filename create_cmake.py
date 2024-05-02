import os
from typing import List
import subprocess
from utility import move_to_dir

# Directories that may have executables, headers, configs, libs
POSSIBLE_DIRECTORIES_FOR_SOURCES  = ("include", "config", "lib", "src")
def create_list_of_files() -> List[str]:
    # Script moves to root directory
    raw_dir_list = []
    os.chdir("../")
    for directory_name in POSSIBLE_DIRECTORIES_FOR_SOURCES:
        if os.path.exists(directory_name) and os.path.isdir(directory_name):
            raw_dir_list += [os.path.join(os.getcwd(), directory_name, file) 
                             for file in  os.listdir(directory_name)]
    return raw_dir_list


def main() -> bool:
    raw_dir_list = []
    if move_to_dir("src"):
        raw_dir_list = create_list_of_files()
    else:
        raw_dir_list = os.listdir()
    # Seeks for main source file
    language_extensions = []
    if any(file.endswith("main.cpp") for file in raw_dir_list):
        language_extensions = [".cpp"]
    if any(file.endswith("main.c") for file in raw_dir_list):
        if not language_extensions:
            language_extensions = [".c"]
        else:
            print("Error: both main.cpp and main.c are in the project.")
            return False
    if not language_extensions:
        print("Error: main.cpp/main.c was not found.")
        return False
    # deletes non executables files
    dir_list = []
    for file in raw_dir_list:
        if file.endswith(tuple(language_extensions)):
            dir_list.append(file)
    # Block to test filehandling
    try:
        filehandler = open("CMakeLists.txt", "w", encoding='utf-8')

    except Exception as e:
        print(f'Error: {e}')
        return False
    # puts main.cpp in the begining, joins list into string
    element_to_move = 'main' + language_extensions[0]
    # looks for main source file with passed extension
    element_to_move = [file for file in dir_list if file.endswith(element_to_move)]
    # Previous step turned element_to_move into list, if list has != 1 element
    # it means project has few main sources or zero 
    if len(element_to_move) != 1:
        print(f"Error: too many instances of {'main' + language_extensions[0]}")
        return False
    # As there are only one elemnt in list it is possible to pass the first el 
    index_to_move = dir_list.index(element_to_move[0])
    element_to_move = dir_list.pop(index_to_move)
    dir_list.insert(0, element_to_move)
    file_list = '\n\t'.join(dir_list)
    
    # writes content into CMakeLists.txt
    project_name = input("Enter project: ")
    content = f'cmake_minimum_required(VERSION 3.27)\nproject({project_name})\n'
    content += 'set(CMAKE_CXX_STANDARD 11)\n'
    content += 'set(CMAKE_EXPORT_COMPILE_COMMANDS ON)\n'
    content += f'include_directories({os.path.join(os.getcwd(), "include")})\n'
    content += f'add_executable({project_name} {file_list}\n)'
    filehandler.write(content)
    filehandler.close() 
    os.chmod("CMakeLists.txt", 0o600)
    print("CMakeLists.txt is created successfully.")
    subprocess.run(["cp", "/home/alga/vim-build-auto/templates/.clang-format", "."], check=True)
    return True

if __name__ == '__main__':
    main()
