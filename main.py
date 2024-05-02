from interface import Interface, Option


if __name__ == "__main__":
    try:
        options = [
            # br for build and run
            Option("br", Interface.br_option),
            # gc for generate cmake
            Option("gs", Interface.gc_option),
            # ra for run with arguments
            Option("ra", Interface.ra_option)
            ]
        app = Interface(options)
    except Exception as e:
        print(f"Error initializing the application: {e}")
