from interface import Interface


if __name__ == "__main__":
    try:
        app = Interface()
    except Exception as e:
        print(f"Error initializing the application: {e}")
