from project import Project
from oop_create_cmake import CmakeGenerator

from typing import Type, Callable, List
from dataclasses import dataclass
import sys


@dataclass
class Option:
    option_name: str
    action: Callable


class Main:
    __options: List[Option]

    def __init__(self, options: List[Option]) -> None:
        self.__options = options
        self.run_options()
        return None

    # Runs option that was passed as argument
    def run_options(self) -> bool:
        # Script name and one arg are expected
        if len(sys.argv) == 1:
            print("Arguments were not provided.")
            return False
        for option in self.__options:
            if option.option_name == sys.argv[1]:
                return option.action()
        print("Provided argument is not a command.")
        return False

    @staticmethod
    def create_cmake_option() -> bool:
        if (len(sys.argv) != 3):
            print("Project name was not provided. Enter it as a second arg.")
            return False
        CG: Type[CmakeGenerator] = CmakeGenerator(sys.argv[2])
        return CG.generate_cmake()

    @staticmethod
    def build_and_run_using_cmake() -> bool:
        if len(sys.argv) < 3 or len(sys.argv) > 4:
            print("Wrong amount arguments for this option were provided.")
            return False
        try:
            # Third argument is a path to root directory. If there is no third
            # argument script checks if current or parent directory is a root.
            if len(sys.argv) == 4:
                project_to_build: Type[Project] = Project(sys.argv[3])
            else:
                project_to_build: Type[Project] = Project()
            project_to_build.create_build_directory(sys.argv[2])
            project_to_build.run_cmake()
            project_to_build.complete_building()
            project_to_build.run_build()
            return True
        except Exception as e:
            print(f"Error in build_and_run_using_cmake: {e}")
            return False

    @staticmethod
    def run_with_args(project_to_build: Type[Project]) -> None:
        try:
            arguments = []
            print("Enter arguments if neccessary,"
                  " otherwise enter empty string.")
            while True:
                user_input = input("Enter argument: ")
                if not user_input:
                    break
                arguments += user_input
            project_to_build.run_build(arguments)
        except Exception as e:
            raise ValueError(f"Error in run_with_args: {e}")


if __name__ == "__main__":
    try:
        options = [
            # br for build and run
            Option("br", Main.build_and_run_using_cmake),
            # gc for generate cmake
            Option("gc", Main.create_cmake_option)
            ]
        app = Main(options)
    except Exception as e:
        print(f"Error initializing the application: {e}")
