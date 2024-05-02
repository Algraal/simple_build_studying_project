General information.

Simple Program used for faster c++/c projects handling.
I use this program to quickly create project directories, automatically write 
CMakeLists.txt, automatically build a project using Smake, and to run the 
program with or without arguments. Program considers directory a root project 
if it stores CMakeLists.txt file. 

Usage:
Program is used as a CLI tool or a script for a editor (Does not work that 
    well for text editors becuase output of the executable/compilation 
    may hover over text. But it depends on text editor, plugins, e.t.c).
    I usually use from terminal of the text editor.

To utilize SimpleBuild, execute the main.py module from the command line with 
the appropriate command-line arguments:
    
    python3 /path_to_simple_build/main.py <option> <arguments>

Alternatively, you can create a symbolic link to the bin directory named 
SimpleBuild for easier access:
    
    SimpleBuild <option> <arguments>

4 options are provided:

1. "np" : New project option
    
    SimpleBuild np <project_name>
    
    Creates in the current directory new directory <project_name> 
        with directories:
        
            "include", "bin", "config", "lib", "src", "tests" inside.
        
        These dirs are defined in "project_creator.py". 
        If directory <project_name> already exist, aborts.

2. "gc" : Generate CMakeLists.txt 
    
    SimpleBuild gc <target_name>

    Generates basic CMakeLists.txt based on files in include and src. Requires
        existance of "main.*" module to define language extension (language 
        extension equals *). Creates different CMakeLists.txt for C and C++ 
        projects. Templates are defined in constants in module 
        "oop_create_cmake".

3. "bp" : Build project option
    
    SimpleBuild bp <build_directory_name> <path_to_the_roof_directory=optional>
    
    Builds project into specified in "build_directory_name" diretory. Build 
        directory should be located in the project root directory.
        Creates
        directory if it does not exist. If directory exists removes it completly,
        generates directory with the same name.

    If "path_to_the_roof_directory" is provided it is considered as a root
        project dir. Otherwise program will check if the current dir or parent 
        dir are the project root directory.

4. "ra" : run with arguments
    
    SimpleBuild ra <arg1=optional>, ... <arg_n=optional>
    
    Attempts to run executable (that is target in CMakeLists.txt) with passed
        arguments (0 arguments is ok).
 
