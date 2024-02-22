import os
from typing import List

# Directories that may have executables
POSSIBLE_DIRECTORIES_FOR_SOURCES  = ("include", "config", "lib", "src")

# Functions cheks if it is inside standard c++ project. If true moves/stays to
# passed directory and return True, otherwise returns False
def is_inside_dir(ending: str) -> bool:
    # Script is expected to be started from src/main.cpp or src/main.c
    if not os.getcwd().endswith(ending):
        target_path = os.path.join(os.getcwd(), ending)
        # case we are in a root directory of a project
        if os.path.exists(target_path) and os.path.isdir(target_path):
            os.chdir(target_path)
        # case we are in a nested directory of a project
        elif os.path.exists("../" + ending) and os.path.isdir("../" + ending):
            os.chdir("../" + ending)
        else:
            print("Error: current directory is not a project. Aborting...")
            return False
    return True

def create_list_of_executables() -> List[str]:
    # Script moves to root directory
    raw_dir_list = []
    os.chdir("../")
    for directory_name in POSSIBLE_DIRECTORIES_FOR_SOURCES:
        if os.path.exists(directory_name) and os.path.isdir(directory_name):
            raw_dir_list += os.listdir(directory_name)
    return raw_dir_list
def main() -> bool:
    raw_dir_list = []
    if is_inside_dir("src"):
        raw_dir_list = create_list_of_executables()
    else:
        raw_dir_list = os.listdir()
    if not ('main.cpp' in raw_dir_list or 'main.c' in raw_dir_list):
        print('Error: main.cpp/main.c is not found')
        return False
    elif 'main.cpp' in raw_dir_list and 'main.c' in raw_dir_list:
        print("Error: both main.cpp and main.c are in the directory")
        return False
    elif 'main.cpp' in raw_dir_list:
        # possible extensions for cpp sources/headers
        language_extensions = ['.cpp', '.h']
    elif 'main.c' in raw_dir_list:
        language_extensions = ['.c', '.h']
    
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
    index_to_move = dir_list.index(element_to_move)
    element_to_move = dir_list.pop(index_to_move)
    dir_list.insert(0, element_to_move)
    file_list = '\n\t'.join(dir_list)
    
    # writes content into CMakeLists.txt
    project_name = input("Enter project: ")
    content = f'cmake_minimum_required(VERSION 3.27)\nproject({project_name})\n'
    content += 'set(CMAKE_CXX_STANDARD 11)\n'
    content += f'add_executable({project_name} {file_list}\n)'
    filehandler.write(content)
    filehandler.close() 
    os.chmod("CMakeLists.txt", 0o600)
    return True

if __name__ == '__main__':
    main()
