import os
import shutil
import sys
from pathlib import Path
import requests

HEADERS = { "User-Agent": "Personal AoC solutions by ArnoldaZ (github.com/arnoldaz/advent-of-code)" }
INPUT_URL = "https://adventofcode.com/{year}/day/{day}/input"
TEMPLATE_FILE_PATH = "solution_template.py"

def get_solution_module_path(year: int, day: int) -> Path:
    return Path(f"{year}/{day:0>2}.py")

def get_input_file_path(year: int, day: int) -> Path:
    return Path(f"input/{year}/{day:0>2}/input.txt")

def get_test_input_file_path(year: int, day: int) -> Path:
    return Path(f"input/{year}/{day:0>2}/input-test.txt")

def get_session_cookie():
    session_cookie = os.getenv("AOC_SESSION_COOKIE")
    if session_cookie is None:
        print("Session cookie is not defined in environment file, impossible to download input.")
        sys.exit(-1)

    return { "session": session_cookie }

def download_input_file(year: int, day: int):
    url = INPUT_URL.format(year=year, day=day)
    response = requests.get(url, cookies=get_session_cookie(), headers=HEADERS, timeout=20)

    if not response.ok:
        if response.status_code == 400:
            print("Session cookie has expired, enter a new one in environment file.")
            sys.exit(-1)
        else:
            response.raise_for_status()

    data = response.text

    input_file_path = get_input_file_path(year, day)
    input_file_directory = os.path.dirname(input_file_path)
    if not os.path.exists(input_file_directory):
        os.makedirs(input_file_directory)

    input_file_path.write_text(data, encoding="utf-8")

def read_input_file(year: int, day: int) -> list[str]:
    input_file_path = get_input_file_path(year, day)
    if not os.path.exists(input_file_path):
        download_input_file(year, day)

    with open(input_file_path, encoding="utf-8") as file:
        return [line.rstrip() for line in file]

def read_user_input() -> list[str]:
    print("Enter/Paste your test data. Enter Ctrl-Z to save it.")
    user_input: list[str] = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        user_input.append(line)

    return user_input

def read_test_input(year: int, day: int) -> list[str]:
    input_file_path = get_test_input_file_path(year, day)
    input_file_directory = os.path.dirname(input_file_path)
    if not os.path.exists(input_file_directory):
        os.makedirs(input_file_directory)

    if not os.path.exists(input_file_path):
        user_input = read_user_input()
        input_file_path.write_text("\n".join(user_input), encoding="utf-8")
        return user_input

    with open(input_file_path, encoding="utf-8") as file:
        return [line.rstrip() for line in file]

def copy_template_file(year: int, day: int):
    if not os.path.exists(year):
        os.makedirs(str(year))

    module_file_path = get_solution_module_path(year, day)
    if os.path.exists(module_file_path):
        return

    shutil.copyfile(TEMPLATE_FILE_PATH, module_file_path)
