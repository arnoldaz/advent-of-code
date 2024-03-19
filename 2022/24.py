# pylint: disable=unused-argument

import queue
from utils.point import INVALID_POINT, Direction, Point

class BlizzardMap:
    def __init__(self, blizzards: list[tuple[Point, Direction]], width: int, height: int):
        self.width = width
        self.height = height
        self.max_timer = 0
        self.blizzard_states: dict[int, list[tuple[Point, Direction]]] = { 0: blizzards }

    def move_blizzards(self):
        latest_blizzard_state = self.blizzard_states[self.max_timer].copy()

        for i, blizzard in enumerate(latest_blizzard_state):
            position, direction = blizzard

            position += direction
            if position.y < 0:
                position.y = self.height - 1
            elif position.y > self.height - 1:
                position.y = 0
            elif position.x < 0:
                position.x = self.width - 1
            elif position.x > self.width - 1:
                position.x = 0

            latest_blizzard_state[i] = (position, direction)

        self.max_timer += 1
        self.blizzard_states[self.max_timer] = latest_blizzard_state

    def get_state(self, timer: int) -> list[tuple[Point, Direction]]:
        while self.max_timer < timer:
            self.move_blizzards()

        return self.blizzard_states[timer]

def parse_input(lines: list[str]) -> tuple[BlizzardMap, Point, Point]:
    blizzards: list[tuple[Point, Direction]] = []
    width = len(lines[0]) - 2
    height = len(lines) - 2

    for y, line in enumerate(lines[1:-1]):
        for x, char in enumerate(line[1:-1]):
            match char:
                case "^":
                    direction = Direction.UP
                case "<":
                    direction = Direction.LEFT
                case ">":
                    direction = Direction.RIGHT
                case "v":
                    direction = Direction.DOWN
                case ".":
                    continue
                case _:
                    raise ValueError("Unknown symbol")

            blizzards.append((Point(x, y), direction))

    blizzard_map = BlizzardMap(blizzards, width, height)
    start = Point(0, -1)
    end = Point(width - 1, height)

    return blizzard_map, start, end

def djikstra_search(blizzard_map: BlizzardMap, start: Point, end: Point):
    frontier = queue.Queue[tuple[Point, int]]()
    came_from: dict[tuple[Point, int], tuple[Point, int]] = {}
    # cost_so_far: dict[tuple[Point, int], int] = {}

    frontier.put((start, 0))
    came_from[(start, -1)] = (INVALID_POINT, 0)
    # cost_so_far[(start, -1)] = 0

    while not frontier.empty():
        # print(list(frontier.queue))
        current, cost = frontier.get()
        if current == end:
            print("wowaweeva")
            break

        neighbors = [current + direction for direction in Direction]

        new_cost = cost + 1

        print(new_cost, current)
        blizzards = blizzard_map.get_state(new_cost) # cost equals to steps moved

        real_neighbors = []
        for neighbor in neighbors:
            if any(neighbor == position for position, _ in blizzards):
                continue

            if not (0 <= neighbor.x <= blizzard_map.width - 1 and 0 <= neighbor.y <= blizzard_map.height - 1) and neighbor != end and neighbor != start:
                continue

            real_neighbors.append(neighbor)

        # non_blizzard_neighbors = [neighbor for position, _ in blizzards for neighbor in neighbors if neighbor == position]
        # final_neighbors = [neighbor for neighbor in non_blizzard_neighbors if not (0 <= neighbor.x <= blizzard_map.width - 1 and 0 <= neighbor.y <= blizzard_map.height - 1)]

        # to not camp at start
        if current != start and len(real_neighbors) == 1 and real_neighbors[0] == start:
            continue

        for neighbor in real_neighbors:
            # cost_so_far[neighbor] = new_cost
            came_from[(neighbor, new_cost)] = (current, cost)
            frontier.put((neighbor, new_cost))

    return came_from

def heuristic_manhattan_distance(point1: Point, point2: Point) -> int:
    return abs(point1.x - point2.x) + abs(point1.y - point2.y)

def a_star_search(blizzard_map: BlizzardMap, start: Point, end: Point):
    open_set = queue.Queue[tuple[Point, int]]()
    open_set.put((start, 0))

    came_from: dict[tuple[Point, int], tuple[Point, int]] = {}
    came_from[(start, -1)] = (INVALID_POINT, 0)

    g_score: dict[tuple[Point, int], int] = {}
    g_score[(start, 0)] = 0

    f_score: dict[tuple[Point, int], int] = {}
    f_score[(start, 0)] = heuristic_manhattan_distance(start, end)

    while not open_set.empty():
        pass

# function reconstruct_path(cameFrom, current)
#     total_path := {current}
#     while current in cameFrom.Keys:
#         current := cameFrom[current]
#         total_path.prepend(current)
#     return total_path

# // A* finds a path from start to goal.
# // h is the heuristic function. h(n) estimates the cost to reach goal from node n.
# function A_Star(start, goal, h)
#     // The set of discovered nodes that may need to be (re-)expanded.
#     // Initially, only the start node is known.
#     // This is usually implemented as a min-heap or priority queue rather than a hash-set.
#     openSet := {start}

#     // For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from the start
#     // to n currently known.
#     cameFrom := an empty map

#     // For node n, gScore[n] is the cost of the cheapest path from start to n currently known.
#     gScore := map with default value of Infinity
#     gScore[start] := 0

#     // For node n, fScore[n] := gScore[n] + h(n). fScore[n] represents our current best guess as to
#     // how cheap a path could be from start to finish if it goes through n.
#     fScore := map with default value of Infinity
#     fScore[start] := h(start)

#     while openSet is not empty
#         // This operation can occur in O(Log(N)) time if openSet is a min-heap or a priority queue
#         current := the node in openSet having the lowest fScore[] value
#         if current = goal
#             return reconstruct_path(cameFrom, current)

#         openSet.Remove(current)
#         for each neighbor of current
#             // d(current,neighbor) is the weight of the edge from current to neighbor
#             // tentative_gScore is the distance from start to the neighbor through current
#             tentative_gScore := gScore[current] + d(current, neighbor)
#             if tentative_gScore < gScore[neighbor]
#                 // This path to neighbor is better than any previous one. Record it!
#                 cameFrom[neighbor] := current
#                 gScore[neighbor] := tentative_gScore
#                 fScore[neighbor] := tentative_gScore + h(neighbor)
#                 if neighbor not in openSet
#                     openSet.add(neighbor)

#     // Open set is empty but goal was never reached
#     return failure



# // A* (star) Pathfinding// Initialize both open and closed list
# let the openList equal empty list of nodes
# let the closedList equal empty list of nodes// Add the start node
# put the startNode on the openList (leave it's f at zero)// Loop until you find the end
# while the openList is not empty    // Get the current node
#     let the currentNode equal the node with the least f value
#     remove the currentNode from the openList
#     add the currentNode to the closedList    // Found the goal
#     if currentNode is the goal
#         Congratz! You've found the end! Backtrack to get path    // Generate children
#     let the children of the currentNode equal the adjacent nodes

#     for each child in the children        // Child is on the closedList
#         if child is in the closedList
#             continue to beginning of for loop        // Create the f, g, and h values
#         child.g = currentNode.g + distance between child and current
#         child.h = distance from child to end
#         child.f = child.g + child.h        // Child is already in openList
#         if child.position is in the openList's nodes positions
#             if the child.g is higher than the openList node's g
#                 continue to beginning of for loop        // Add the child to the openList
#         add the child to the openList





# PointFrom = tuple[Point, Direction]
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

def silver_solution(lines: list[str]) -> int:
    blizzard_map, start, end = parse_input(lines)

    result = djikstra_search(blizzard_map, start, end)

    print("end btw", end)
    for x, y in result.items():
        print(x, y)

    for key_point, key_cost in result:
        if key_point == end:
            return key_cost



    # for key, value in blizzard_map.blizzard_states.items():
    #     print(f"blizzard key: {key}")
    #     for y in range(blizzard_map.height):
    #         for x in range(blizzard_map.width):
    #             for a, b in value:
    #                 if Point(x, y) == a:
    #                     match b:
    #                         case Direction.LEFT:
    #                             print("<", end="")
    #                         case Direction.RIGHT:
    #                             print(">", end="")
    #                         case Direction.UP:
    #                             print("^", end="")
    #                         case Direction.DOWN:
    #                             print("v", end="")
    #                     break
    #             else:
    #                 print(".", end="")
    #         print()

    return -123

def gold_solution(lines: list[str]) -> int:
    # Implement solution
    return -321
