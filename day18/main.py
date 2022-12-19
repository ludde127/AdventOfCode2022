import time
from typing import Optional
from utils import readfile
from collections import deque
def parse(data) -> set[tuple[int, int, int]]:
    positions = set()
    for row in data:
        positions.add(tuple([int(i) for i in row.split(",")]))
    return positions

def cube_sides(cube):
    return [(cube[0] + 1, cube[1], cube[2]),
            (cube[0] - 1, cube[1], cube[2]),
            (cube[0], cube[1] + 1, cube[2]),
            (cube[0], cube[1] - 1, cube[2]),
            (cube[0], cube[1], cube[2] + 1),
            (cube[0], cube[1], cube[2] - 1)]
def count_air_sides(cube, parsed_data):
    sides = 0
    for side in cube_sides(cube):
        if side not in parsed_data:
            sides+=1
    return sides

def recursive_count_sides(cube, parsed_data, depth=0):
    sides = 0
    if depth == 0:
        for side in cube_sides(cube):
            if side in parsed_data:
                sides += 1

        return sides
    for side in cube_sides(cube):
        if side in parsed_data:
            sides+=recursive_count_sides(side, parsed_data, depth-1)
    return sides

def partone(parsed_data: set[tuple[int, int, int]]):
    sides = 0
    for cube in parsed_data:
        sides += count_air_sides(cube, parsed_data)
    print(sides)
    return sides

def parttwo(parsed_data: set[tuple[int, int, int]]):
    xs, ys, zs = zip(*parsed_data)
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    minz, maxz = min(zs), max(zs)
    print(minx, maxx, miny, maxy, minz, maxz)
    def cube_in_window(cube, extra=1):
        return minx-extra<=cube[0]<=maxx+extra and miny-extra<=cube[1]<=maxy+extra and minz-extra<=cube[2]<=maxz+extra

    """Loops over all cords if have passed one cube in all directions and will se one more count it"""
    all_sides = set()


    """print(parsed_data)

    for potential in all_sides:

        if minx<potential[0]<maxx and miny<potential[1]<maxy and minz<potential[2]<maxz:
            print("a", potential, count_air_sides(potential, parsed_data))
            if potential not in parsed_data:
                print("b", potential)
                mutated_parsed_data.add(potential)
                mutated_parsed_data.update(cube_sides(potential))"""
    """for x in range(minx, maxx):
        points = [e for e in parsed_data if e[0] == x]
        min_y_for_this_x = min((e[1] for e in points))
        max_y_for_this_x = max((e[1] for e in points))
        for y in range(min_y_for_this_x, max_y_for_this_x):

            _points = [e for e in points if e[1] == y]

            min_z_for_this_xy = min((e[2] for e in _points))
            max_z_for_this_xy = max((e[2] for e in _points))
            for z in range(min_z_for_this_xy, max_z_for_this_xy):
                mutated_parsed_data.add((x,y,z))"""

    air_start = (minx-1, miny-1, minz-1)


    to_check = deque()
    to_check.append(air_start)
    sides = 0
    checked = set()
    while to_check:
        current = to_check.popleft()
        for neighbour in cube_sides(current):
            in_window = cube_in_window(neighbour)
            #print(neighbour, in_window)
            if neighbour not in checked and in_window:
                if not neighbour in parsed_data:
                    checked.add(neighbour)
                    to_check.append(neighbour)
                else:
                    sides += 1

    print(sides)


    #print(partone(mutated_parsed_data))

if __name__ == "__main__":
    t0 = time.time()
    real_data = readfile("input_real.txt")
    #data = readfile("input.txt")
    parttwo(parse(real_data)) # 2049<x<2784<3408
    print(time.time()-t0)