from typing import NamedTuple, Optional

class File(NamedTuple):
    size: int
    name: str

class Directory:
    def __init__(self, directories: list["Directory"], files: list[File], directory_name: str):
        self.directories = directories
        self.files = files
        self.name = directory_name

    def add_item(self, directory_path: str, item: "Directory | File"):
        paths = directory_path.split("\\")

        current_directory = self
        for path in paths:
            current_directory = next((directory for directory in current_directory.directories if directory.name == path), self)

        if isinstance(item, Directory):
            current_directory.directories.append(item)
        elif isinstance(item, File):
            current_directory.files.append(item)

    def print_tree(self, indent = 0):
        print(f"{'  ' * indent}- {self.name or "root"} (dir)")
        for file in self.files:
            print(f"{'  ' * (indent + 1)}- {file.name} (file, size={file.size})")
        for directory in self.directories:
            directory.print_tree(indent + 1)

    def get_directory_sum(self) -> int:
        return sum(file.size for file in self.files) + sum(directory.get_directory_sum() for directory in self.directories)

    def get_all_directory_sums(self, sum_list: Optional[list[int]] = None) -> list[int]:
        if sum_list is None:
            sum_list = []

        if self.name:
            sum_list.append(self.get_directory_sum())

        for directory in self.directories:
            directory.get_all_directory_sums(sum_list)

        return sum_list

def create_file_tree(lines: list[str]) -> Directory:
    root_directory: Directory = Directory([], [], "")

    command, first_directory_name = lines[0].removeprefix("$ ").split()
    assert command == "cd"

    current_directory_path = first_directory_name
    root_directory.add_item(current_directory_path, Directory([], [], first_directory_name))

    for line in lines[1:]:
        if line.startswith("$"):
            command = line.removeprefix("$ ")
            if command == "ls":
                # Only non-command text is result from "ls", so let other branch automatically handle it
                pass
            else:
                _, location = command.split()
                if location == "..":
                    index = current_directory_path.rfind("\\")
                    current_directory_path = current_directory_path[:index]
                else:
                    current_directory_path += f"\\{location}"
        else:
            prefix, name = line.split()
            if prefix == "dir":
                root_directory.add_item(current_directory_path, Directory([], [], name))
            else:
                root_directory.add_item(current_directory_path, File(int(prefix), name))

    return root_directory

def silver_solution(lines: list[str]) -> int:
    root_directory = create_file_tree(lines)
    return sum(directory_sum for directory_sum in root_directory.get_all_directory_sums() if directory_sum <= 100_000)

def gold_solution(lines: list[str]) -> int:
    root_directory = create_file_tree(lines)

    total_disk_space = 70_000_000
    required_disk_space = 30_000_000
    root_sum = root_directory.get_directory_sum()
    additional_space_required = required_disk_space - (total_disk_space - root_sum)

    return next((directory_sum for directory_sum in sorted(root_directory.get_all_directory_sums()) if directory_sum > additional_space_required), -1)
