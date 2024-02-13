def convert_snafu_to_decimal(number: str) -> int:
    decimal_number = 0
    for i, symbol in enumerate(reversed(number)):
        match symbol:
            case "-":
                decimal_number += (5 ** i) * -1
            case "=":
                decimal_number += (5 ** i) * -2
            case _:
                digit = int(symbol)
                decimal_number += (5 ** i) * digit

    return decimal_number

def convert_decimal_to_snafu(number: int) -> str:
    snafu_number: list[str] = []
    while number > 0:
        division, remainder = divmod(number, 5)
        match remainder:
            case 4:
                snafu_number.append("-")
                division += 1
            case 3:
                snafu_number.append("=")
                division += 1
            case _:
                snafu_number.append(str(remainder))

        number = division

    return "".join(reversed(snafu_number))

def silver_solution(lines: list[str]) -> str:
    return convert_decimal_to_snafu(sum(convert_snafu_to_decimal(line) for line in lines))

def gold_solution(_lines: list[str]) -> int:
    return 0
