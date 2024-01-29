import os
import requests
import sys
from pathlib import Path

HEADERS = { "User-Agent": "Personal AoC solutions by ArnoldaZ (github.com/arnoldaz/advent-of-code)" }
INPUT_URL = "https://adventofcode.com/{year}/day/{day}/input"

def get_solution_module_path(year: int, day: int) -> Path:
    return Path(f"{year}/{day:0>2}/{day:0>2}.py")

def get_input_file_path(year: int, day: int) -> Path:
    return Path(f"input/{year}/{day:0>2}/input.txt")

def get_session_cookie():
    session_cookie = os.getenv("AOC_SESSION_COOKIE")
    if session_cookie is None:
        print("Session cookie is not defined in environment file, impossible to download input.")
        sys.exit(-1)

    return { "session": session_cookie }

def download_input_file(year: int, day: int):
    url = INPUT_URL.format(year=year, day=day)
    response = requests.get(url, cookies=get_session_cookie(), headers=HEADERS)

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

    input_file_path.write_text(data)

def read_input_file(year: int, day: int) -> list[str]:
    input_file_path = get_input_file_path(year, day)
    if not os.path.exists(input_file_path):
        download_input_file(year, day)

    with open(input_file_path) as file:
        return [line.rstrip() for line in file]