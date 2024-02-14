import os
import shutil
import subprocess


def do_make():
    if not is_file_exists('Makefile'):
        return False
    try:
        subprocess.run(['make'], check=True)
        print("Make completed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f'Error running make {e}')
        return False

def remove_directory(directory_path):
    try:
        shutil.rmtree(directory_path)
        print(f"Directory '{directory_path}' and its contents removed successfully.")
        return True 
    except Exception as e:
        print(f"Error removing directory '{directory_path}': {e}")
        return False
# checks passed path 
def is_directory_exists(directory_path):
    return os.path.exists(directory_path) and os.path.isdir(directory_path)
def is_file_exists(directory_path):
    return os.path.exists(directory_path) and os.path.isfile(directory_path)
# 
def run_cmake():
    try:
        subprocess.run(['cmake', '..'], check=True)
        print('Cmake configuration completed succesfully.')
        return True
    except subprocess.CalledProcessError as e:
        print(f'Error running Cmake: {e}')
        return False
    
def build_project():
    # user inputs what kind of build they need
    build_reg = ''
    while True:
        build_reg = input("Enter 'build', 'debug' or 'exit' to cancel: ")
        if build_reg == 'exit':
            print("Building was canceled. Aborting.")
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
    os.chdir(build_reg)
    print(os.getcwd())
    
    # tries to build project
    if not run_cmake():
        return False
    if not do_make():
        return False
    return True
# start    

if __name__ = '__main__':
    app(main)
    if build_project():
        print("Built successfully.")
    else
    print("Build failed")

