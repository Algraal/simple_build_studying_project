
import os
from utility import remove_directory
# This script creates project directory for c++ project


PROJECT_DIRECTORIES = ("include", "bin", "config", "lib", "src", "tests")

class ProjectCreator:
    __project_name: str
    def __init__(self, project_name: str) -> None:
        self.__project_name = project_name
        
        # Creates project root directory
        Main.create_directory(project_name)
        # Moves to the created root directory
        try:
            os.chdir(project_name)
            print(os.getcwd())
        except Exception as e:
            Main.clean_project(project_name)
            print(f"Failed to enter {project_name}: {e}. Aborting...")
            return None

        # Creates project directories
        for directory in PROJECT_DIRECTORIES:
            if not Main.create_directory(directory):
                Main.clean_project(project_name)
                return None
        return None
    # Method that creates directory, returns True if no Exception appears
    @staticmethod
    def create_directory(directory_name: str) -> bool:
        try:
            os.mkdir(directory_name)
            print(f"Directory {directory_name} created successfully")
            return True
        except Exception as e:
            print(f"Failed to create directory {directory_name}: {e}. Aborting...")
            return False
    # Method that removes directories on failure
    @staticmethod
    def clean_project(project_name: str) -> bool:
        # deletes project root directory
        if not os.getcwd().endswith(project_name):
            return Main.delete_directory(project_name)
        else:
            for directory in PROJECT_DIRECTORIES:
                Main.delete_directory(directory)
            os.chdir("..")
            Main.clean_project(project_name)
        return False


if __name__ == "__main__":
    app = Main()

