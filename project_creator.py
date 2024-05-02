import os
import sys
from typing import Tuple

from utility import remove_directory, create_directory


class ProjectCreator:
    """
    A class to create a directory structure for a C++ project.

    Attributes:
        PROJECT_DIRECTORIES (tuple[str]): Tuple containing names of directories
            to be created.
        __project_name (str): Name of the project.
    """
    PROJECT_DIRECTORIES: Tuple[str] = ("include", "bin", "config", "lib",
                                       "src", "tests")
    __project_name: str

    def __init__(self, provided_project_name: str) -> None:
        """
        Initialize the ProjectCreator class with a project name.

        Args:
            provided_project_name (str): Name of the project.
        """
        self.__project_name = provided_project_name
        return None

    @staticmethod
    def create_boilerplate() -> bool:
        """
        Create the boilerplate structure of the project.

        Returns:
            bool: True if successful, False otherwise.
        """
        if len(sys.argv) != 3:
            print("Incorrect amount of arguments were provided.",
                  file=sys.stderr)
        # First arg is option, second the name of the project
        PC = ProjectCreator(sys.argv[2])
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

    @staticmethod
    def clean_project(project_name: str) -> bool:
        """
        Remove project directories on failure.

        Args:
            project_name (str): Name of the project directory.

        Returns:
            bool: True if cleaning is successful, False otherwise.
        """
        try:
            # False from remove_directory is returned when directory does not
            # exist. It is fine for this method, because it is called after
            # error in creating directories.
            remove_directory(project_name)
            return True

        except OSError as e:
            print(f"Project cannot be cleaned: {e}.", file=sys.stderr)
            return False
