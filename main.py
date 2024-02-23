from project import Project
from typing import Type

class Main:
    def __init__(self) -> None:
        try:
            project_to_build = Project()
            Main.build_using_cmake(project_to_build)
        except Exception as e:
            raise ValueError(f"Failed building using cmake: {e}")
    @staticmethod
    def build_using_cmake(project_to_build: Type[Project]) -> None:
        try:
            while True:
                build_dir = input("Enter: 'build', 'debug', or "\
                                  "'exit' (to cancel): ")
                if build_dir in ['build', 'debug', 'exit']:
                    break
            if build_dir == 'exit':
                print("Building was canceled. Aborting...")
            elif not project_to_build.create_build_directory(build_dir):
                raise ValueError("Error: cannot create build directory.")
        except Exception as e:
            raise ValueError(f"Error in build_using_cmake: {e}")
if __name__ == "__main__":
    try:
        app = Main()
    except Exception as e:
        print(f"Error initializing the application: {e}")

