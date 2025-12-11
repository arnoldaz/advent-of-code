from functools import cache

def parse_input(lines: list[str]) -> dict[str, list[str]]:
    return {left: right.split() for left, right in (line.split(": ") for line in lines)}

def get_paths_count(graph: dict[str, list[str]], start: str, end: str) -> int:
    @cache
    def get_paths_count_dfs(start: str, end: str) -> int:
        if start == end:
            return 1

        if start not in graph:
            return 0

        return sum(get_paths_count_dfs(neighbor, end) for neighbor in graph[start])

    return get_paths_count_dfs(start, end)

def silver_solution(lines: list[str]) -> int:
    graph = parse_input(lines)
    return get_paths_count(graph, "you", "out")

def gold_solution(lines: list[str]) -> int:
    graph = parse_input(lines)

    svr_fft = get_paths_count(graph, "svr", "fft")
    fft_dac = get_paths_count(graph, "fft", "dac")
    dac_out = get_paths_count(graph, "dac", "out")

    svr_dac = get_paths_count(graph, "svr", "dac")
    dac_fft = get_paths_count(graph, "dac", "fft")
    fft_out = get_paths_count(graph, "fft", "out")

    return svr_fft * fft_dac * dac_out + svr_dac * dac_fft * fft_out
