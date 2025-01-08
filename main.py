import argparse
import importlib.util
import sys
import time
from types import ModuleType
from typing import Callable, NamedTuple
from dotenv import load_dotenv
from colorama import Fore
from utils.aoc import copy_template_file, download_answers_file, get_solution_module_path, read_input_file, read_test_input

class ProgramArguments(NamedTuple):
    year: int
    day: int | tuple[int, int]
    silver: bool
    gold: bool
    test: bool
    add_template: bool
    validate: bool

def parse_arguments() -> ProgramArguments:
    parser = argparse.ArgumentParser(prog="Advent of Code runner", description="Runs Advent of Code solutions.")
    parser.add_argument("-y", "--year", type=int, help="solution year", required=True)
    parser.add_argument("-d", "--day", type=lambda arg: int(arg) if arg.isdecimal() else arg, help="solution day or day range", required=True)
    parser.add_argument("-s", "--silver", action="store_true", help="only run silver solution")
    parser.add_argument("-g", "--gold", action="store_true", help="only run gold solution")
    parser.add_argument("-t", "--test", action="store_true", help="run with test input")
    parser.add_argument("-a", "--add-template", action="store_true", help="add template solution module")
    parser.add_argument("-v", "--validate", action="store_true", help="validate solution answers based on displayed results on puzzle page")
    args = parser.parse_args()

    if not 2015 <= args.year <= 2025:
        parser.error("Year (-y/--year) is not a valid Advent of Code year.")

    day: int | tuple[int, int]
    if isinstance(args.day, str):
        if "-" not in args.day:
            parser.error("Day (-d/--day) range doesn't have '-' symbol.")

        first_day, last_day = args.day.split("-")
        if not first_day.isdecimal() or not last_day.isdecimal():
            parser.error("Day (-d/--day) ranges are not valid numbers.")

        first_day_number, last_day_number = int(first_day), int(last_day)
        if not 1 <= first_day_number <= 25 or not 1 <= last_day_number <= 25:
            parser.error("Day (-d/--day) ranges are not valid Advent of Code days.")

        day = (first_day_number, last_day_number)

    if isinstance(args.day, int):
        if not 1 <= args.day <= 25:
            parser.error("Day (-d/--day) is not a valid Advent of Code day.")

        day = args.day

    return ProgramArguments(args.year, day, args.silver, args.gold, args.test, args.add_template, args.validate)

def timed_solution(function: Callable[[list[str]], int | str], function_params: list[str]) -> tuple[int | str, int]:
    start_time = time.perf_counter_ns()
    result = function(function_params)
    end_time = time.perf_counter_ns()

    return result, end_time - start_time

def format_nanoseconds_string(nanoseconds: int) -> str:
    seconds = nanoseconds / 1e9

    if seconds < 1:
        color = Fore.GREEN
    elif seconds < 10:
        color = Fore.YELLOW
    else:
        color = Fore.RED

    return f"{color}{seconds:>0.9f}s{Fore.RESET}"

def load_module(year: int, day: int) -> ModuleType:
    module_path = get_solution_module_path(year, day)
    spec = importlib.util.spec_from_file_location(str(day), module_path)
    if spec is None or spec.loader is None:
        print(f"Error: Spec from a file '{module_path}' failed to load.")
        sys.exit(-1)

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, "silver_solution"):
        print(f"Error: Loaded module '{module_path}' doesn't have silver solution function.")
        sys.exit(-1)

    if not hasattr(module, "gold_solution"):
        print(f"Error: Loaded module '{module_path}' doesn't have gold solution function.")
        sys.exit(-1)

    return module

def run_solution(year: int, day: int, run_silver: bool, run_gold: bool, test_input: bool):
    module = load_module(year, day)
    input_data = read_input_file(year, day) if not test_input else read_test_input(year, day)

    if run_silver:
        result, time_taken = timed_solution(module.silver_solution, input_data)
        print(f"Silver solution: {result:>20} | time {format_nanoseconds_string(time_taken)}")

    if run_gold:
        result, time_taken = timed_solution(module.gold_solution, input_data)
        print(f"Gold solution:   {result:>20} | time {format_nanoseconds_string(time_taken)}")

def run_all_solutions(year: int, day_range: tuple[int, int]):
    total_silver_time, total_gold_time = 0, 0
    first_day, last_day = day_range
    split_line = f"{"-" * 43}+{"-" * 27}"

    print(split_line)

    for day in range(first_day, last_day + 1):
        module = load_module(year, day)
        input_data = read_input_file(year, day)

        _, silver_time_taken = timed_solution(module.silver_solution, input_data)
        _, gold_time_taken = timed_solution(module.gold_solution, input_data)
        total_silver_time += silver_time_taken
        total_gold_time += gold_time_taken

        print(f"[Day {day:0>2} time] Silver: {(format_nanoseconds_string(silver_time_taken)):>30} | Gold: {(format_nanoseconds_string(gold_time_taken)):>30}")

    print(split_line)
    print(f"[Total times] Silver: {(format_nanoseconds_string(total_silver_time)):>30} | Gold: {(format_nanoseconds_string(total_gold_time)):>30}")
    print(split_line)

def validate_solutions(year: int, days: int | tuple[int, int], answers: dict[str, dict[str, int | str]]):
    if isinstance(days, int):
        first_day, last_day = days, days
    else:
        first_day, last_day = days

    split_line = f"{"-" * 43}+{"-" * 27}"

    print(split_line)

    for day in range(first_day, last_day + 1):
        module = load_module(year, day)
        input_data = read_input_file(year, day)

        silver_answer: int | str = module.silver_solution(input_data)
        gold_answer: int | str = module.gold_solution(input_data)

        cached_answers = answers[str(day)]

        cached_silver_answer = cached_answers["silver"]
        if silver_answer == cached_silver_answer:
            print(f"[Day {day:0>2} silver answer] {Fore.GREEN}{silver_answer}{Fore.RESET}")
        else:
            print(f"[Day {day:0>2} silver answer] {Fore.RED}ERROR:{Fore.RESET} Expected {Fore.BLUE}{cached_silver_answer}{Fore.RESET}, Actual {Fore.RED}{silver_answer}{Fore.RESET}")

        cached_gold_answer = cached_answers["gold"]
        if gold_answer == cached_gold_answer:
            print(f"[Day {day:0>2}   gold answer] {Fore.GREEN}{gold_answer}{Fore.RESET}")
        else:
            print(f"[Day {day:0>2}   gold answer] {Fore.RED}ERROR:{Fore.RESET} Expected {Fore.BLUE}{cached_gold_answer}{Fore.RESET}, Actual {Fore.RED}{gold_answer}{Fore.RESET}")

    print(split_line)

def main():
    args = parse_arguments()
    load_dotenv()

    if args.validate:
        answers = download_answers_file(args.year, args.day)
        validate_solutions(args.year, args.day, answers)
        return

    if not isinstance(args.day, int):
        run_all_solutions(args.year, args.day)
        return

    if args.add_template:
        copy_template_file(args.year, args.day)
        return

    run_solution(args.year, args.day, args.silver or not args.gold, args.gold or not args.silver, args.test)

if __name__ == "__main__":
    main()
