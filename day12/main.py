from utils import readfile
from functools import lru_cache
from collections import deque
DIRECTIONS = {(1, 0), (0, 1), (-1, 0), (0, -1)}
class SHORTEST:
    def __init__(self):
        self.shortest = 10000000
        self.path = []
    def add_new(self, path):
        if len(path) < self.shortest:
            self.path = path
            self.shortest = len(path)

SHORTEST_HAHA = SHORTEST()
def find_start_end(data):
    start = None
    end = None

    for (y, row) in enumerate(data):
        for (x, char) in enumerate(row):
            if char == "S":
                start = (x, y)
            elif char == "E":
                end = (x, y)
    assert end is not None and start is not None, "End or Start was None + " + end + " s: " + start
    return start, end

@lru_cache(1000)
def to_normalized_integer(char: str):
    if char == "E":
        return ord("z") - ord("a")
    elif char == "S":
        return 0
    return ord(char) - ord("a")

def move(current_position, end_goal, data, current_steps = 0, path=None):
    if path is None:
        path = list()

    current_char  = data[current_position[0]][current_position[1]]
    elevation = to_normalized_integer(current_char)
    paths = list()
    if current_position == end_goal or current_steps >= 1000:
        if len(path) == 0:
            return 1e5
        return len(path)
    for _dir in DIRECTIONS:
        c = char_from_pos(current_position, data, _dir)
        new_pos = (current_position[0]+_dir[0], current_position[1]+_dir[1])
        if c and new_pos not in path:
            """
            print(current_position)
            print(elevation, to_normalized_integer(c), c)
            print(to_normalized_integer(c)-elevation)"""
            if to_normalized_integer(c)-elevation <= 1:
                #print("B")
                path2 = path.copy()
                path2.append(new_pos)
                next = move(new_pos, end_goal, data, current_steps=current_steps+1, path=path2)
                if next:
                    path2.extend(next)
                    paths.append(path2)
    try:
        return sorted(paths, key=lambda p: len(p))[0]
    except IndexError:
        return None
def char_from_pos(pos, data, direction=None):
    try:
        if direction is None:
            return data[pos[1]][pos[0]]
        else:
            x = pos[0]+direction[0]
            y = pos[1]+direction[1]
            if x >= 0 and y >=0:
                return data[y][x]

    except IndexError:
        pass
    return None


def mover(start, data, path):
    current_char  = data[start[0]][start[1]]
    elevation = to_normalized_integer(current_char)
    if current_char == "E":
        print("FOUND ONE PATH ", len(path))
        SHORTEST_HAHA.add_new(path)
        return path
    elif len(path) > SHORTEST_HAHA.shortest or len(path) > 500:
        return []
    path.append(start)

    found_paths = list()
    for _dir in DIRECTIONS:
        c = char_from_pos(start, data, _dir)
        new_pos = (start[0]+_dir[0], start[1]+_dir[1])
        if new_pos not in path and c:
            if to_normalized_integer(c)-elevation <= 1:
                #print("B")
                try:
                    found_paths.append(mover(new_pos, data, path=path.copy()))
                except IndexError:
                    pass
    return sorted(found_paths, key=lambda p: len(p))[0]

"""def mover_bruteforce(start, data):
    found = False
    while not found:
        for _dir in DIRECTIONS:
            c = char_from_pos(current_pos, data, _dir)
            new_pos = (current_pos[0] + _dir[0], current_pos[1] + _dir[1])
            if new_pos not in visited and c:
                if to_normalized_integer(c) - elevation <= 1:"""

def mover2(start, data, path):
    path.append(start)
    current_char  = data[start[0]][start[1]]
    elevation = to_normalized_integer(current_char)
    if current_char == "E":
        SHORTEST_HAHA.add_new(path)
        return path
    elif len(path) > SHORTEST_HAHA.shortest:
        return []

    found_paths = list()
    open_list = [start]
    visited = set()

    while open_list:
        current_pos = open_list.pop()
        visited.add(current_pos)
        current_char  = data[current_pos[0]][current_pos[1]]
        elevation = to_normalized_integer(current_char)

        if current_char == "E":
            SHORTEST_HAHA.add_new(path)
            return path

        for _dir in DIRECTIONS:
            c = char_from_pos(current_pos, data, _dir)
            new_pos = (current_pos[0]+_dir[0], current_pos[1]+_dir[1])
            if new_pos not in visited and c:
                if to_normalized_integer(c)-elevation <= 1:
                    path2 = path.copy()
                    path2.append(new_pos)
                    open_list.append(new_pos)
                    found_paths.append(path2)

    return sorted(found_paths, key=lambda p: len(p))[0]


def bfs(start, data):
    frontier = deque()
    frontier.append(start)
    links = dict()
    links[start] = None

    while len(frontier) > 0:
        current = frontier.popleft()

        char = char_from_pos(current, data)
        elevation = to_normalized_integer(char)

        for _dir in DIRECTIONS:
            c = char_from_pos(current, data, _dir)
            new_pos = (current[0] + _dir[0], current[1] + _dir[1])
            if new_pos not in links and c and to_normalized_integer(c) - elevation <= 1:
                frontier.append(new_pos)

                links[new_pos] = current

    return links
def partone(data):
    start, end = find_start_end(data)
    all_paths = bfs(start, data)

    current = end
    i = 0
    while current != start:
        i+=1
        current = all_paths[current]
    print(i)

    print(bfs(start, data))

def parttwo(data):
    _, end = find_start_end(data)
    starts = list()
    minimum = 1000
    for x in range(len(data[0])):
        for y in range(len(data)):
            if char_from_pos((x,y), data) == "a":
                starts.append((x, y))
    for start in starts:

        all_paths = bfs(start, data)

        current = end
        i = 0
        if not end in all_paths:
            print("No solution")
        else:
            while current != start:
                i+=1
                current = all_paths[current]
            if i<minimum:
                minimum = i
            print(i)

    print(minimum)
if __name__ == "__main__":
    next = "p"
    current = "y"
    assert to_normalized_integer(next) - to_normalized_integer(current) <= 1

    example = readfile("input.txt")
    real = readfile("input_real.txt")

    parttwo(real)