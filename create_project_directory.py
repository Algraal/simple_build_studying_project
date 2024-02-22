import os
# This script creates project directory for c++ project
PROJECT_DIRECTORIES = ("include", "bin", "config", "lib", "src", "tests")

class Main:
    def __init__(self) -> None:
        project_name = input("Enter project name: ")
        if "Y" != input(f"Are you sure that you want to create new project {project_name}? Y/n"):
            print("Project creation is cancelled. Aborting...")
            return None
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
    # Deletes provided directory if it exists in current dir, empty, 
    # and actually a dir
    @staticmethod
    def delete_directory(directory_name: str) -> bool:
        dir_path = os.path.join(os.getcwd(), directory_name)
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            try:
                os.rmdir(dir_path)
                print(f"Project`s {directory_name} has been deleted successfully")
                return True
            except Exception as e:
                print(f"Error: {e}. Aborting...")
                return False
        else:
            print(f"Directory {directory_name} does not exist or is not a file")
            return False
        return False

if __name__ == "__main__":
    app = Main()


