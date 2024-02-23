from project import Project
from typing import Type

class Main:
    def __init__(self) -> None:
        project_to_build = Project()
        Main.build_using_cmake(project_to_build)
        return None
    @staticmethod
    def build_using_cmake(project_to_build: Type[Project]) -> bool:
        while True:
            build_dir = input("Enter: 'build', 'debug', or "\
                              "'exit' (to cancel): ")
            if build_dir == 'build':
                break
            elif build_dir == 'debug':
                break
            elif build_dir == 'exit':
                print("Building was canceled. Aborting...")
                return True
        if not project_to_build.create_build_directory(build_dir):
            return False
        return True

if __name__ == "__main__":
    app = Main()

