import itertools
import queue
from utils.matrix import Matrix
from utils.point import INVALID_POINT, Direction, Point

# def djikstra_search(grid: Matrix[int], start: Point, possible_movements: list[tuple[Point, Direction]]):
#     frontier = queue.Queue[PointFrom]()
#     came_from: dict[PointFrom, Point] = {}
#     cost_so_far: dict[PointFrom, int] = {}

#     frontier.put((start, Direction.NONE))
#     came_from[(start, Direction.NONE)] = INVALID_POINT
#     cost_so_far[(start, Direction.NONE)] = 0

#     while not frontier.empty():
#         current, direction = frontier.get()
#         for (neighbor, new_direction, cost) in get_valid_neighbors(current, direction, grid, possible_movements):
#             new_cost = cost_so_far[(current, direction)] + cost
#             if (neighbor, new_direction) not in cost_so_far or new_cost < cost_so_far[(neighbor, new_direction)]:
#                 cost_so_far[(neighbor, new_direction)] = new_cost
#                 came_from[(neighbor, new_direction)] = current
#                 frontier.put((neighbor, new_direction))

#     return cost_so_far

PointFrom = tuple[Point, Direction]

def get_paths_bfs(grid: Matrix[int], start: Point, ends: list[Point]) -> list[list[Point]]:
    frontier = queue.Queue[tuple[Point, list[Point]]]()
    frontier.put((start, []))
    all_paths: list[list[Point]] = []

    while not frontier.empty():
        current, path = frontier.get()
        for neighbor, _ in grid.get_neighbors(current):
            if grid.get_symbol(current) + 1 == grid.get_symbol(neighbor):
                new_path = path + [neighbor]
                frontier.put((neighbor, new_path))
                if neighbor in ends:
                    all_paths.append(new_path)

    return all_paths

def djikstra_search(grid: Matrix[str], start: Point, end: Point):
    frontier = queue.Queue[tuple[Point, Direction, list[Point]]]()
    cost_so_far: dict[tuple[Point, Direction], int] = {}

    all_paths: list[tuple[list[Point], int]] = []

    if start == end:
        all_paths.append(([], 0))

    frontier.put((start, Direction.NONE, []))
    cost_so_far[(start, Direction.NONE)] = 0

    while not frontier.empty():
        current, current_dir, path = frontier.get()


        for (neighbor, dir) in grid.get_neighbors(current):
            if grid.get_symbol(neighbor) == "":
                continue

            if neighbor in path:
                continue

            direction_change_penalty = 0 if current_dir == dir else 0

            new_cost = cost_so_far[(current, current_dir)] + 1 + direction_change_penalty
            if (neighbor, dir) not in cost_so_far or new_cost <= cost_so_far[(neighbor, dir)]:
                cost_so_far[(neighbor, dir)] = new_cost
                new_path = path + [neighbor]
                frontier.put((neighbor, dir, new_path))
                if neighbor == end:
                    all_paths.append((new_path, new_cost))

    min_cost = min(all_paths, key=lambda x: x[1])[1]
    return [path for path, cost in all_paths if cost == min_cost]

def get_direction(point: Point, end_point: Point) -> Direction:
    return Direction(end_point - point)

def get_symbol(dir: Direction) -> str:
    match dir:
        case Direction.UP:
            return "^"
        case Direction.LEFT:
            return "<"
        case Direction.RIGHT:
            return ">"
        case Direction.DOWN:
            return "v"        
    raise

def get_keypad_codes(keypad: Matrix[str], code: str):
    keypad_start = keypad.find_first_character_instance("A")
    start = keypad_start
    end = keypad.find_first_character_instance(code[0])

    directions = []

    i = 1
    while True:
        # print("start of the loop", start, end)
        paths = djikstra_search(keypad, start, end)
        # print("nx", start, end, "....", paths)

        new_directions: list[str] = []
        for path in paths:
            current_direction = ""
            inner_start = start
            for p in path:
                dir = get_direction(inner_start, p)
                current_direction += get_symbol(dir)
                inner_start = p

            current_direction += "A"
            new_directions.append(current_direction)

        directions.append(new_directions)
        # print(new_directions)

        if i == len(code):
            break

        next_symbol = code[i]
        start = end
        end = keypad.find_first_character_instance(next_symbol)
        i += 1

    combinations = [''.join(parts) for parts in itertools.product(*directions)]

    return combinations

def silver_solution(lines: list[str]) -> int:
    codes = lines
    # code = codes[0] # 029A

    keypad = Matrix[str]([
        ["7", "8", "9"],
        ["4", "5", "6"],
        ["1", "2", "3"],
        [ "", "0", "A"],
    ], str)
    keypad.print()
    directional_keypard = Matrix[str]([
        [ "", "^", "A"],
        ["<", "v", ">"],
    ], str)
    # print(code)

    nig = []

    # a = djikstra_search(keypad, Point(x=2, y=0), Point(x=0, y=1))
    # return 1
    # # paths = reconstruct_paths(came_from, cost_so_far, Point(1, 2), Point(2, 0))

    # print(a)

    # return 1

    final_sum = 0
    mins = []

    for code in codes:
        min_len = 99999999999

        initials = get_keypad_codes(keypad, code)

        for initial in initials:
            subs = get_keypad_codes(directional_keypard, initial)

            # mina = min(subs, key=lambda x: len(x))
            # if len(mina) <= min_len:
            #     min_len = min(min_len, len(mina))
            #     mins.append(mina)

            for sub in subs:
                sub_subs = get_keypad_codes(directional_keypard, sub)
                # print("ccc", sub_subs[0])
                mina = min(sub_subs, key=lambda x: len(x))
                if len(mina) <= min_len:
                    min_len = min(min_len, len(mina))
                    mins.append(mina)

        code_num = int(code.removesuffix("A"))
        print(min_len, "*", code_num)
        final_sum += min_len * code_num
    
        for a in mins:
            print(a)

        mins = []

    return final_sum

    # <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
    # v<<A>>^A<A>AvA<^AA>A<vAAA>^A
    # <A^A>^^AvvvA
    # 029A

    # v<A<AA>>^AvAA^<A>Av<<A>>^AvA^Av<<A>>^AAvA<A^>A<A>Av<A<A>>^AAA<A>vA^A
    # v<<A>>^A<A>A<AA>vA^Av<AAA^>A
    # <A^A^^>AvvvA

    for code in ["029A"]:


        keypad_start = keypad.find_first_character_instance("A")
        start = keypad_start
        end = keypad.find_first_character_instance(code[0])

        directions = ""

        for move in code[1:]:
            came_from = djikstra_search(keypad, start, end)
            path = reconstruct_shortest_path(came_from, start, end)
            path.reverse()
            
            # print(path, start, end)
            inner_start = start
            for p in path:
                dir = get_direction(inner_start, p)
                directions += get_symbol(dir)
                # print(dir)
                inner_start = p
            directions += "A"
            start = end
            end = keypad.find_first_character_instance(move)
        
        # ===================
        # duplicate lmao
        came_from = djikstra_search(keypad, start, end)
        path = reconstruct_shortest_path(came_from, start, end)
        path.reverse()
        
        # print(path, start, end)
        inner_start = start
        for p in path:
            dir = get_direction(inner_start, p)
            directions += get_symbol(dir)
            # print(dir)
            inner_start = p
        directions += "A"
        # ===================

        directions = "^A<<^^A"
        print("FIRST DIRECTION", directions)
        # mano
        # <A^A^^>AvvvA
        # <A^A>^^AvvvA


        dir_keypad_start = directional_keypard.find_first_character_instance("A")
        start = dir_keypad_start
        end = directional_keypard.find_first_character_instance(directions[0])

        directions2 = ""

        for move in directions[1:]:
            came_from = djikstra_search(directional_keypard, start, end)
            path = reconstruct_shortest_path(came_from, start, end)
            path.reverse()
            
            # print(path, "aaa", start, end)
            inner_start = start
            for p in path:
                dir = get_direction(inner_start, p)
                directions2 += get_symbol(dir)
                # print(dir)
                inner_start = p
            directions2 += "A"
            start = end
            end = directional_keypard.find_first_character_instance(move)

        # ===================
        # duplicate lmao
        came_from = djikstra_search(directional_keypard, start, end)
        path = reconstruct_shortest_path(came_from, start, end)
        path.reverse()
        
        # print(path, "aaa", start, end)
        inner_start = start
        for p in path:
            dir = get_direction(inner_start, p)
            directions2 += get_symbol(dir)
            # print(dir)
            inner_start = p
        directions2 += "A"
        # ===================

        print("DIRECTIONS2:", directions2)
        # mano
        # v<<A>^>A<A>A<AA>vA^Av<AAA^>A
        # good
        # v<<A>>^A<A>AvA<^AA>A<vAAA>^A

        # directions2 = "v<<A>>^A<A>AvA<^AA>A<vAAA>^A"

        dir_keypad_start = directional_keypard.find_first_character_instance("A")
        start = dir_keypad_start
        end = directional_keypard.find_first_character_instance(directions2[0])

        directions3 = ""

        for move in directions2[1:]:
            came_from = djikstra_search(directional_keypard, start, end)
            path = reconstruct_shortest_path(came_from, start, end)
            path.reverse()
            
            # print(path, "aaa", start, end)
            inner_start = start
            for p in path:
                dir = get_direction(inner_start, p)
                directions3 += get_symbol(dir)
                # print(dir)
                inner_start = p
            directions3 += "A"
            start = end
            end = directional_keypard.find_first_character_instance(move)

        # ===================
        # duplicate lmao
        came_from = djikstra_search(directional_keypard, start, end)
        path = reconstruct_shortest_path(came_from, start, end)
        path.reverse()
        
        # print(path, "aaa", start, end)
        inner_start = start
        for p in path:
            dir = get_direction(inner_start, p)
            directions3 += get_symbol(dir)
            # print(dir)
            inner_start = p
        directions3 += "A"
        # ===================

        print("DIRECTIONS3:", directions3)

        nig.append(directions3)

    # for i in range(len(codes)):
    #     code = codes[i]
    #     res = nig[i]

    #     code = int(code.removesuffix("A"))
    #     print(len(res), "*", code)


    for a in nig:
        print(a)

    # v<A<AA>>^AvAA^<A>Av<<A>>^AvA^Av<<A>>^AAvA<A^>A<A>Av<A<A>>^AAA<A>vA^A
    # v<<A>>^AAAvA^Av<A<AA>>^AvAA^<A>Av<A<A>>^AAA<A>vA^Av<A^>A<A>A
    # v<<A>>^Av<A<A>>^AAvAA^<A>Av<<A>>^AAvA^Av<A^>AA<A>Av<A<A>>^AAA<A>vA^A
    # v<<A>>^AAv<A<A>>^AAvAA^<A>Av<A^>A<A>Av<A^>A<A>Av<A<A>>^AA<A>vA^A
    # v<<A>>^AvA^Av<<A>>^AAv<A<A>>^AAvAA^<A>Av<A^>AA<A>Av<A<A>>^AAA<A>vA^A

    # <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
    # <v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A
    # <v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
    # <v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A
    # <v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A

    print("<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A".count("A"))
    print("v<A<AA>^>AvA^<A>vA^Av<<A>^>AvA^Av<<A>^>AAvA<A^>A<A>Av<A<A>^>AAA<A>vA^A".count("A"))

    # <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
    # v<A<AA>^>AvA^<A>vA^Av<<A>^>AvA^Av<<A>^>AAvA<A^>A<A>Av<A<A>^>AAA<A>vA^A


    # v<A<AA>^>AvAA^<A>Av<<A>^>AvA^Av<A^>Av<<A>^A>AAvA^Av<<A>A^>AAAvA^<A>A
    # <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A


    # mano
    # <A^A^^>AvvvA
    # good
    # <A^A>^^AvvvA

    # mano
    # v<<A>^>A<A>A<AA>vA^Av<AAA^>A
    # good
    # v<<A>>^A<A>AvA<^AA>A<vAAA>^A

    # mano
    # v<A<AA>^>AvA^<A>vA^Av<<A>^>AvA^Av<<A>^>AAvA<A^>A<A>Av<A<A>^>AAA<A>vA^A
    # good
    # <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A

    # v<A<AA>>^AvAA^<A>Av<<A>>^AvA^Av<<A>>^AAvA<A^>A<A>Av<A<A>>^AAA<A>vA^A


    # mano last code 379A
    # ^A^^<<A>>AvvvA
    # <A>A<AAv<AA>>^AvAA^Av<AAA^>A
    # v<<A>>^AvA^Av<<A>>^AAv<A<A>>^AAvAA^<A>Av<A^>AA<A>Av<A<A>>^AAA<A>vA^A

    # ^A<<^^A>>AvvvA
    # <A>Av<<AA>^AA>AvAA^Av<AAA^>A
    # v<<A>>^AvA^Av<A<AA>>^AAvA^<A>AAvA^Av<A^>AA<A>Av<A<A>>^AAA<A>vA^A

    # ^A^^<<A
    # <A>A<AAv<AA>>^A
    # v<<A>>^AvA^Av<<A>>^AAv<A<A>>^AAvAA^<A>A

    # ^A<<^^A
    # <A>Av<<AA>^AA>A
    # v<<A>>^AvA^Av<A<AA>>^AAvA^<A>AAvA^A


    return -123

def gold_solution(lines: list[str]) -> int:
    # Implement solution
    return -321
