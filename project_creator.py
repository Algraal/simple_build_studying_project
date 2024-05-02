import os
import sys
from utility import remove_directory, create_directory
# This script creates project directory for c++ project


class ProjectCreator:
    PROJECT_DIRECTORIES = ("include", "bin", "config", "lib", "src", "tests")
    __project_name: str

    def __init__(self, provided_project_name: str) -> None:
        self.__project_name = provided_project_name
        return None

    # Method that creates boilerplate of the project.
    @staticmethod
    def create_boilerplate() -> bool:
        if len(sys.argv) != 2:
            print("Incorrect amount of arguments were provided.",
                  file=sys.stderr)
        PC = ProjectCreator(sys.argv[1])
        # Creates project root directory
        if not create_directory(PC.__project_name):
            return False
        # Moves to the created root directory
        try:
            os.chdir(PC.__project_name)
            print(os.getcwd())
        except OSError as e:
            ProjectCreator.clean_project(PC.__project_name)
            print(f"Failed to enter {PC.__project_name}: {e}. Aborting...",
                  file=sys.stderr)
            return False

        # Creates project directories
        for directory in ProjectCreator.PROJECT_DIRECTORIES:
            try:
                # If False is returned, it means that directory already exists,
                # that is not a problem
                create_directory(directory)
            # If OS error appears project should be cleaned. There is no sense
            # in partly created boilerplate.
            except OSError:
                ProjectCreator.clean_project(PC.__project_name)
                return False
        return True

    # Method that removes directories on failure
    @staticmethod
    def clean_project(project_name: str) -> bool:
        # Deletes project root directory
        try:
            # False from remove_directory is returned when directory does not
            # exist. It is fine for this method, because it is called after
            # error in creating directories.
            remove_directory(project_name)
            return True

        except OSError as e:
            print(f"Project cannot be cleaned: {e}.", file=sys.stderr)
            return False
