import os
import shutil
import subprocess
import sys
import re


# runs make in created directory
def do_make() -> bool:
    if not is_file_exists('Makefile'):
        return False
    try:
        subprocess.run(['cmake', '--build', '.'], check=True)
        print("Make completed successfully.")
        executable_name = find_executable_name()
        if executable_name == "":
            print(f"Executable does not exist")
            return False
        shutil.move(executable_name, "../bin")
        return True
    except subprocess.CalledProcessError as e:
        print(f'Error running make {e}')
        return False


def find_executable_name() -> str:
    try:
        filehandler = open('../CMakeLists.txt', 'r', encoding='utf-8')
        content = filehandler.read()
        match = re.search(r'project\s*\(\s*([^\s)]+)', content)
        filehandler.close()

        if not match:
            print("Error: Could not get project name. Aborting...")
            return False

        executable_name = match.group(1)
        # Check if the executable exists
        if not is_file_exists(executable_name):
            print(f"Error: Executable does not exist")
            return ""
        else:
            return executable_name
    except Exception as e:
        print(f"Error. Binary was not found: {e}")
        return ""


# runs execuatble in the same directory if it has the same name as defined in
# CMakeList.txt located in parent directory. Returns false if CMakeLists.txt
# does not exist, cannot be opened, does not have project name 
def run_build() -> bool:
    executable_name = find_executable_name()
    move_to_root()
    if executable_name == "":
        print(f"Executable does not exist.")
        return False
    try:
        print(f"Program {executable_name} started")
        completed_process = subprocess.run(f'bin/{executable_name}', check=True)
        return True
    except Exception as e:
        print(f"Program failed to start: {e}. Aborting...")

# TODO delete
def remove_directory(directory_path: str) -> bool:
    try:
        shutil.rmtree(directory_path)
        print(f"Directory '{directory_path}' and its contents removed successfully.")
        return True 
    except Exception as e:
        print(f"Error removing directory '{directory_path}': {e}")
        return False

# checks passed path 
def is_directory_exists(directory_path: str) -> bool:
    return os.path.exists(directory_path) and os.path.isdir(directory_path)
def is_file_exists(directory_path: str) -> bool:
    return os.path.exists(directory_path) and os.path.isfile(directory_path)
# 
def run_cmake() -> bool:
    try:
        subprocess.run(['cmake', '..'], check=True)
        print('Cmake configuration completed succesfully.')
        return True
    except subprocess.CalledProcessError as e:
        print(f'Error running Cmake: {e}')
        return False

# Moves to root directory of a project, for now directory with src
# is considered root directory
def move_to_root() -> bool:
    current_dir_files = os.listdir()
    previous_dir_files = os.listdir("../")
    if "src" in current_dir_files:
        return True
    elif "src" in previous_dir_files:
        try:
            os.chdir("..")
            return True
        except Exception as e:
            print("Error moving to root dir: {e}")
            return False
    else:
        return False

def main(option: str) -> bool:
    # user inputs what kind of build they need
    if option != 'run' and option != 'build':
        print('Undefined option. Aborting...')
        return False
    if not move_to_root():
        print("Unable to find root directory. Aborting...")
        return False
    build_reg = ''
    while True:
        build_reg = input("Enter 'build', 'debug' or 'exit' to cancel: ")
        if build_reg == 'exit':
            print("Building was canceled. Aborting...")
            return False
        elif build_reg == 'build':
            break
        elif build_reg == 'debug':
            break
    build_reg = './' + build_reg
    
    # Checks if it is possible to start building process
    if not is_file_exists("CMakeLists.txt"):
        print("CMakeLists.txt file does not exist. Aborting.")
        return False
    if is_directory_exists(build_reg):
        # if process has not enought right to delete existing build cancel building
        if not remove_directory(build_reg):
            return False
    # makes dir for new build and moves over there
    os.mkdir(build_reg)
    try:
        os.chdir(build_reg)
    except Exception as e:
        print(f"Error cannot enter {build_reg}: {e}")
        return False
    print(os.getcwd())
    
    # tries to build project
    if not run_cmake():
        return False
    if not do_make():
        return False
    if option == 'run':
        if run_build():
            print('Program started.')
        else:
            print("Error: program start is cancelled. Aborting...")
            return False
    return True
  
if __name__ == '__main__':
    if main(sys.argv[1]):
        print("Built successfully.")
    else:
        print("Build failed")

