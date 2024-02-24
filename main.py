from project import Project
from typing import Type

class Main:
    def __init__(self) -> None:
        try:
            project_to_build = Project()
            Main.build_and_run_using_cmake(project_to_build)
        except Exception as e:
            raise ValueError(f"Failed building using cmake: {e}")
    @staticmethod
    def build_and_run_using_cmake(project_to_build: Type[Project]) -> None:
        try:
            while True:
                build_dir = input("Enter: 'build', 'debug', or "\
                                  "'exit' (to cancel): ")
                if build_dir in ['build', 'debug', 'exit']:
                    break
            if build_dir == 'exit':
                print("Building was canceled. Aborting...")
            else:
                project_to_build.create_build_directory(build_dir)
            project_to_build.run_cmake()
            project_to_build.complete_building()
            project_to_build.run_build()
        except Exception as e:
            raise ValueError(f"Error in build_and_run_using_cmake: {e}")
    @staticmethod
    def run_with_args(ptoject_to_build: Type[Project]) -> None:
        try:
            arguments = []
            print("Enter arguments if neccessary,"\
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

