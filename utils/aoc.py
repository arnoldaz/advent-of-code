import json
import os
import re
import shutil
import sys
from pathlib import Path
import requests

HEADERS = { "User-Agent": "Personal AoC solutions by ArnoldaZ (github.com/arnoldaz/advent-of-code) (testing some automation for a bit)" }
INPUT_URL = "https://adventofcode.com/{year}/day/{day}/input"
PUZZLE_URL = "https://adventofcode.com/{year}/day/{day}"
TEMPLATE_FILE_PATH = "solution_template.py"
PUZZLE_ANSWER_REGEX = r"Your puzzle answer was <code>([a-zA-Z0-9,-=]+)<\/code>"
NO_ANSWER_VALUE = "No answer"

def get_solution_module_path(year: int, day: int) -> Path:
    return Path(f"{year}/{day:0>2}.py")

def get_input_file_path(year: int, day: int) -> Path:
    return Path(f"input/{year}/{day:0>2}/input.txt")

def get_test_input_file_path(year: int, day: int) -> Path:
    return Path(f"input/{year}/{day:0>2}/input-test.txt")

def get_answers_file_path(year: int) -> Path:
    return Path(f"answers/{year}.json")

def get_session_cookie():
    session_cookie = os.getenv("AOC_SESSION_COOKIE")
    if session_cookie is None:
        print("Session cookie is not defined in environment file, impossible to download input.")
        sys.exit(-1)

    return { "session": session_cookie }

def get_url_response(url: str) -> str:
    response = requests.get(url, cookies=get_session_cookie(), headers=HEADERS, timeout=20)

    if not response.ok:
        if response.status_code == 400:
            print("Session cookie has expired, enter a new one in environment file.")
            sys.exit(-1)
        else:
            response.raise_for_status()

    return response.text

def download_input_file(year: int, day: int):
    url = INPUT_URL.format(year=year, day=day)
    data = get_url_response(url)

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

def download_answers_file(year: int, days: int | tuple[int, int]) -> dict[str, dict[str, int | str]]:
    answers_file_path = get_answers_file_path(year)

    answers_file_directory = os.path.dirname(answers_file_path)
    if not os.path.exists(answers_file_directory):
        os.makedirs(answers_file_directory)

    answers: dict[str, dict[str, int | str]] = {}
    if os.path.exists(answers_file_path):
        with open(answers_file_path, encoding="utf-8") as file:
            answers = json.load(file)

    if isinstance(days, int):
        start_day, end_day = days, days
    else:
        start_day, end_day = days

    for day in range(start_day, end_day + 1):
        day_key = str(day)
        if day_key in answers:
            cached_answers = answers[day_key]
            if NO_ANSWER_VALUE not in (cached_answers["silver"], cached_answers["gold"]):
                continue

        url = PUZZLE_URL.format(year=year, day=day)
        data = get_url_response(url)

        parsed_answers: list[str] = re.findall(PUZZLE_ANSWER_REGEX, data)
        converted_answers = [int(answer) if answer.isnumeric() else answer for answer in parsed_answers]
        silver_answer, gold_answer = (converted_answers + [NO_ANSWER_VALUE, NO_ANSWER_VALUE])[:2]
        if day == 25:
            gold_answer = 0

        answers[day_key] = { "silver": silver_answer, "gold": gold_answer }

    json_object = json.dumps(answers, indent=4)
    with open(answers_file_path, "w", encoding="utf-8") as file:
        file.write(json_object)

    return answers

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
    if not os.path.exists(str(year)):
        os.makedirs(str(year))

    module_file_path = get_solution_module_path(year, day)
    if os.path.exists(module_file_path):
        return

    shutil.copyfile(TEMPLATE_FILE_PATH, module_file_path)
