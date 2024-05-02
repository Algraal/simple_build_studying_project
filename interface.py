from project import Project
from oop_create_cmake import CmakeGenerator

from typing import Callable, List
from dataclasses import dataclass
import sys


@dataclass
class Option:
    option_name: str
    action: Callable


class Interface:
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

    # Build and run using cmake
    def br_option():
        Project.build_and_run_using_cmake()

    # Run with arguments
    def ra_option():
        Project.run_with_args()

    # Generate cmake
    def gc_option():
        CmakeGenerator.create_cmake_option()
