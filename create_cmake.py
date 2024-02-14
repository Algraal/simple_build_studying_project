import os

def main() -> bool:
    raw_dir_list = os.listdir()
    if not 'main.cpp' in raw_dir_list:
        print('Error: main.cpp is not found')
        return False
    # deletes non executables files
    dir_list = []
    for file in raw_dir_list:
        if file.endswith('.cpp') or file.endswith('.h'):
            dir_list.append(file)
    # Block to test filehandling
    try:
        filehandler = open("CMakeLists.txt", "w", encoding='utf-8')

    except Exception as e:
        print(f'Error: {e}')
        return False
    # puts main.cpp in the begining, joins list into string
    element_to_move = 'main.cpp'
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
