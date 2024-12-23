import networkx as nx

def parse_input(lines: list[str]) -> dict[str, list[str]]:
    connections = [tuple[str, str](line.split("-")) for line in lines]
    groups: dict[str, list[str]] = {}
    for left, right in connections:
        groups.setdefault(left, []).append(right)
        groups.setdefault(right, []).append(left)

    return groups

def silver_solution(lines: list[str]) -> int:
    graph = parse_input(lines)

    return sum(1 for clique in nx.enumerate_all_cliques(nx.Graph(graph))
            if len(clique) == 3 and any(str(x).startswith("t") for x in clique))

def gold_solution(lines: list[str]) -> str:
    graph = parse_input(lines)

    largest_clique = max(nx.find_cliques(nx.Graph(graph)), key=len)
    return ",".join(sorted(largest_clique))
