def read_api_key_from_file(filename="api_key.txt"):
    try:
        with open(filename, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {filename}")
        return None