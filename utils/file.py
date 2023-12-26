
def read_lines(file_name: str) -> list[str]:
    with open(file_name) as file:
        return [line.rstrip() for line in file]