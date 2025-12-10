# pylint: disable-all
from itertools import combinations
from utils.point2d import Point2d

def parse_input(lines: list[str]) -> list[Point2d]:
    return [Point2d(*map(int, line.split(","))) for line in lines]

def silver_solution(lines: list[str]) -> int:
    points = parse_input(lines)

    return max(
        (abs(p1.x - p2.x) + 1) * (abs(p1.y - p2.y) + 1)
        for p1, p2
        in combinations(points, 2)
    )

class Line2d:
    def __init__(self, start: Point2d, end: Point2d):
        self.start = start
        self.end = end

    def __str__(self) -> str:
        return f"{{{self.start} -> {self.end}}}"

    def __repr__(self) -> str:
        return self.__str__()

    def is_horizontal(self) -> bool:
        return self.start.y == self.end.y
    
    def is_vertical(self) -> bool:
        return self.start.x == self.end.x

    def on_line(self, point: Point2d) -> bool:
        if self.is_horizontal():
            return point.y == self.start.y and (self.start.x < point.x < self.end.x or self.start.x > point.x > self.end.x)
        if self.is_vertical():
            return point.x == self.start.x and (self.start.y < point.y < self.end.y or self.start.y > point.y > self.end.y)

        return False

def lines_intersecting(line1: Line2d, line2: Line2d) -> bool:
    if line1.start == line1.end or line2.start == line2.end:
        return False
    
    if line1.is_horizontal() and line2.is_vertical():
        point = Point2d(line2.start.x, line1.start.y)
        if point == line1.start or point == line1.end or point == line2.start or point == line2.end:
            return False
        return line1.on_line(point) and line2.on_line(point)
    elif line1.is_vertical() and line2.is_horizontal():
        point = Point2d(line1.start.x, line2.start.y)
        if point == line1.start or point == line1.end or point == line2.start or point == line2.end:
            return False
        return line1.on_line(point) and line2.on_line(point)
    
    return False

def gold_solution(lines: list[str]) -> int:
    points = parse_input(lines)
    polygon_segments = [Line2d(p1, p2) for p1, p2 in zip(points, points[1:] + points[:1])]
    long_segment1, long_segment2 = [segment for segment in polygon_segments if abs(segment.start.x - segment.end.x) > 50000]
    
    min_bad_y, max_bad_y = min(long_segment1.start.y, long_segment2.start.y), max(long_segment1.start.y, long_segment2.start.y)
    # print(min_bad_y, max_bad_y)
    
    test = []
    
    # print(len(points))
    
    i=0
    max_c = len(list(combinations(points, 2)))
    
    max_area = 0
    for point1, point2 in combinations(points, 2):
        # if i% 100 == 0:
        #     print(f"{i} / {max_c}")
        # i+=1
        
        width = abs(point1.x - point2.x) + 1
        height = abs(point1.y - point2.y) + 1

        area = width * height
        if area < max_area:
            continue
        
        min_x, max_x = min(point1.x, point2.x), max(point1.x, point2.x)
        min_y, max_y = min(point1.y, point2.y), max(point1.y, point2.y)
    
        # if not (max_y <= min_bad_y or min_y >= max_bad_y):
        #     continue
        
        if not (max_y <= min_bad_y or min_y >= max_bad_y):
            continue
    
        is_good = True
        for y in range(min_y, max_y + 1, 1000):
            p1 = Point2d(min_x, y)
            p2 = Point2d(max_x, y)

            if not point_in_polygon(p1, points) or not point_in_polygon(p2, points):
                is_good = False
                break

        if not is_good:
            continue

        for x in range(min_x, max_x + 1, 1000):
            p1 = Point2d(x, min_y)
            p2 = Point2d(x, max_y)

            if not point_in_polygon(p1, points) or not point_in_polygon(p2, points):
                is_good = False
                break
    
        if not is_good:
            continue
        
            
        p1 = Point2d(min_x, min_y)
        p2 = Point2d(max_x, min_y)
        p3 = Point2d(max_x, max_y)
        p4 = Point2d(min_x, max_y)
        
        max_area = max(max_area, area)
        test = [p1,p2,p3,p4]
        # print(p1, p2, p3, p4, area)
    


        # pls1 = point_in_polygon(p1, points)
        # pls2 = point_in_polygon(p2, points) 
        # pls3 = point_in_polygon(p3, points) 
        # pls4 = point_in_polygon(p4, points)
        
        # if pls1 and pls2 and pls3 and pls4:
        #     max_area = max(max_area, area)
        #     test = [p1,p2,p3,p4]
        #     print(p1, p2, p3, p4, area)
    
        
    # import numpy as np
    # from PIL import Image, ImageDraw

    # polygon_points =[(*(map(int,o.split(","))),)for o in open("i").readlines()]

    # # choose a reasonable output size (e.g., 4000 x 4000)
    # W, H = 4000, 4000  

    # # your real logical grid size
    # GRID_W, GRID_H = 100_000, 100_000

    # # scale polygon coordinates
    # scale_x = W / GRID_W
    # scale_y = H / GRID_H

    # polygon = [(x * scale_x, y * scale_y) for (x, y) in polygon_points]
    # polygon2 = [(a.x * scale_x, a.y * scale_y) for a in test]

    # img = Image.new("RGB", (W, H), "white")
    # draw = ImageDraw.Draw(img)
    # draw.polygon(polygon, outline="black", fill="black")
    # draw.polygon(polygon2, outline="green", fill=None)
    # img.save("polygon.png")
    
    return max_area
    

def gold_solution2(lines: list[str]) -> int:
    points = parse_input(lines)
    polygon_segments = [Line2d(p1, p2) for p1, p2 in zip(points, points[1:] + points[:1])]
    long_segment1, long_segment2 = [segment for segment in polygon_segments if abs(segment.start.x - segment.end.x) > 50000]
    
    min_bad_y, max_bad_y = min(long_segment1.start.y, long_segment2.start.y), max(long_segment1.start.y, long_segment2.start.y)
    print(min_bad_y, max_bad_y)
    
    max_area = 0
    for point1, point2 in combinations(points, 2):
        width = abs(point1.x - point2.x) + 1
        height = abs(point1.y - point2.y) + 1

        area = width * height
        if area < max_area:
            continue
        
        min_x, max_x = min(point1.x, point2.x), max(point1.x, point2.x)
        min_y, max_y = min(point1.y, point2.y), max(point1.y, point2.y)
    
        if max_y <= min_bad_y or min_y >= max_bad_y:
            max_area = max(max_area, area)
            print(point1, point2)

    return max_area
        

def point_on_axis_aligned_segment(p, a, b):
    """Exact check for horizontal or vertical segment. No eps."""
    px, py = p.x, p.y
    ax, ay = a.x, a.y
    bx, by = b.x, b.y

    # Horizontal segment
    if ay == by:
        if py != ay:
            return False
        return min(ax, bx) <= px <= max(ax, bx)

    # Vertical segment
    if ax == bx:
        if px != ax:
            return False
        return min(ay, by) <= py <= max(ay, by)

    # Should never happen in rectilinear polygon
    return False


def is_left(p0, p1, p2):
    """Cross product orientation test (exact if integer coords)."""
    return ((p1.x - p0.x) * (p2.y - p0.y)
          - (p2.x - p0.x) * (p1.y - p0.y))

def winding_number(point, polygon):
    px, py = point.x, point.y
    wn = 0

    for i in range(len(polygon)):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % len(polygon)]

        # Exact boundary check
        if point_on_axis_aligned_segment(point, p1, p2):
            return 1  # boundary = inside

        y1 = p1.y
        y2 = p2.y

        # Upward crossing
        if y1 <= py < y2:
            if is_left(p1, p2, point) > 0:
                wn += 1

        # Downward crossing
        elif y2 <= py < y1:
            if is_left(p1, p2, point) < 0:
                wn -= 1

    return wn


def point_in_polygon(point, polygon):
    return winding_number(point, polygon) != 0

def gold_solution3(lines: list[str]) -> int:
    points = parse_input(lines)
    polygon_segments = [Line2d(p1, p2) for p1, p2 in zip(points, points[1:] + points[:1])]

    long_segment1, long_segment2 = [segment for segment in polygon_segments if abs(segment.start.x - segment.end.x) > 50000]
    
    min_bad_y, max_bad_y = min(long_segment1.start.y, long_segment2.start.y), max(long_segment1.start.y, long_segment2.start.y)
    print(min_bad_y, max_bad_y)
    

    max_area = 0
    for point1, point2 in combinations(points, 2):
        width = abs(point1.x - point2.x) + 1
        height = abs(point1.y - point2.y) + 1

        area = width * height
        if area < max_area:
            continue
        
        min_y, max_y = min(point1.y, point2.y), max(point1.y, point2.y)
    
        if not (max_y <= min_bad_y or min_y >= max_bad_y):
            continue
        
        is_bad = False
        for polygon_segment in polygon_segments:
            min_x, max_x = min(point1.x, point2.x), max(point1.x, point2.x)
            min_y, max_y = min(point1.y, point2.y), max(point1.y, point2.y)
            
            l1 = Line2d(Point2d(min_x, min_y), Point2d(max_x, min_y))
            l2 = Line2d(Point2d(max_x, min_y), Point2d(max_x, max_y))
            l3 = Line2d(Point2d(max_x, max_y), Point2d(min_x, max_y))
            l4 = Line2d(Point2d(min_x, max_y), Point2d(min_x, min_y))
            
            pls1 = lines_intersecting(polygon_segment, l1)
            pls2 = lines_intersecting(polygon_segment, l2) 
            pls3 = lines_intersecting(polygon_segment, l3) 
            pls4 = lines_intersecting(polygon_segment, l4)
            
            if pls1 or pls2 or pls3 or pls4:
                print("bad", polygon_segment, point1, point2)
                if pls1:
                    print(l1)
                if pls2:
                    print(l2)
                if pls3:
                    print(l3)
                if pls4:
                    print(l4)
                is_bad = True
                break
            
        if is_bad:
            continue
        

        max_area = max(max_area, area)

    return max_area

    max_c = len(list(combinations(points, 2)))
    i = 1

    max_area = 0
    for point1, point2 in combinations(points, 2):
        width = abs(point1.x - point2.x) + 1
        height = abs(point1.y - point2.y) + 1

        area = width * height
        if area < max_area:
            continue

        min_x, max_x = min(point1.x, point2.x), max(point1.x, point2.x)
        min_y, max_y = min(point1.y, point2.y), max(point1.y, point2.y)

        is_good = True
        for y in range(min_y, max_y + 1):
            p1 = Point2d(min_x, y)
            p2 = Point2d(max_x, y)

            if not point_in_polygon(p1, points) or not point_in_polygon(p2, points):
                is_good = False
                break

        if not is_good:
            continue

        for x in range(min_x, max_x + 1):
            p1 = Point2d(x, min_y)
            p2 = Point2d(x, max_y)

            if not point_in_polygon(p1, points) or not point_in_polygon(p2, points):
                is_good = False
                break

        max_area = max(max_area, area)

    return max_area


# 2445498515 too high
# 2382215991 too high
# 1606063024 bad

# 1772274119 wrong from VV