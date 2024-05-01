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

        super().__init__(
                Option("br", self.build_and_run_using_cmake)
                )
        self.__options = options
        self.run_options()
        return None

    # Runs option that was passed as argument
    def run_options(self) -> bool:
        # Script name and one arg are expected
        if len(sys.argv) != 2:
            print("Only one argument is expected.")
            return False
        for option in self.__options:
            if option.option_name == sys.argv[1]:
                return option.action()
        print("Provided argument is not a command.")
        return False

    @staticmethod
    def create_cmake_option() -> bool:
        CG: Type[CmakeGenerator] = CmakeGenerator()
        return CG.generate_cmake()

    @staticmethod
    def build_and_run_using_cmake() -> bool:
        try:
            project_to_build: Type[Project] = Project()
            while True:
                build_dir = input("Enter: 'build', 'debug', or "
                                  "'exit' (to cancel): ")
                if build_dir in ['build', 'debug', 'exit']:
                    break
            if build_dir == 'exit':
                print("Building was canceled. Aborting...")
                return False
            else:
                project_to_build.create_build_directory(build_dir)
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
        app = Main()
    except Exception as e:
        print(f"Error initializing the application: {e}")
