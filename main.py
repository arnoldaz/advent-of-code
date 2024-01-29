import argparse
import importlib.util
import sys
import time
from dotenv import load_dotenv
from types import ModuleType
from typing import Callable, NamedTuple

from utils.aoc import copy_template_file, get_solution_module_path, read_input_file, read_test_input

class ProgramArguments(NamedTuple):
    year: int
    day: int
    silver: bool
    gold: bool
    test: bool
    add_template: bool

def parse_arguments() -> ProgramArguments:
    parser = argparse.ArgumentParser(prog="Advent of Code runner", description="Runs Advent of Code solutions.")
    parser.add_argument("-y", "--year", type=int, help="solution year", required=True)
    parser.add_argument("-d", "--day", type=int, help="solution day", required=True)
    parser.add_argument("-s", "--silver", action="store_true", help="only run silver solution")
    parser.add_argument("-g", "--gold", action="store_true", help="only run gold solution")
    parser.add_argument("-t", "--test", action="store_true", help="run with test input")
    parser.add_argument("-a", "--add-template", action="store_true", help="add template solution module")

    untyped_args = parser.parse_args()
    args = ProgramArguments(untyped_args.year, untyped_args.day, untyped_args.silver, untyped_args.gold, untyped_args.test, untyped_args.add_template)

    if not 2015 <= args.year <= 2025:
        parser.error("Year (-y/--year) is not a valid Advent of Code year.")
    
    if not 1 <= args.day <= 25:
        parser.error("Day (-d/--day) is not a valid Advent of Code day.")

    return args

def timed_solution(function: Callable[[list[str]], int], function_params: list[str]) -> tuple[int, int]:
    start_time = time.perf_counter_ns()
    result = function(function_params)
    end_time = time.perf_counter_ns()

    return result, end_time - start_time

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
        print(f"Silver solution: {result:>20} | time {time_taken / 1e9}s")

    if run_gold:
        result, time_taken = timed_solution(module.gold_solution, input_data)
        print(f"Gold solution:   {result:>20} | time {time_taken / 1e9}s")

def main():
    args = parse_arguments()
    load_dotenv()

    if args.add_template:
        copy_template_file(args.year, args.day)
        return

    run_solution(args.year, args.day, args.silver or not args.gold, args.gold or not args.silver, args.test)

if __name__ == "__main__":
    main()