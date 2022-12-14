from utils import readfile, Position, Line
import functools
SANDPOSITION = Position(500, 0)

def parse_input(data):
    rocks = list()
    for row in data:
        rocks.append([Position(x, y) for x, y in [pos.strip().split(",") for pos in row.split("->")]])
    return rocks
def partone(parsed):
    done = False
    rocks = set()
    for rock in parsed:
        past = None
        for part in rock:
            if past is not None:
                rocks.add(Line(past, part))
            past = part

    def pos_is_free(pos: Position):
        #print(r)
        return pos not in occupied_by_sand and not any((pos in _rock for _rock in rocks))

    occupied_by_sand = set()
    down = Position(0,1)
    ldiag = Position(-1, 1)
    rdiag = Position(1, 1)
    max_depth_rock = max([max([j[1] for j in i]) for i in parsed])
    @functools.lru_cache(2000)
    def in_abyss(pos: Position):
        #print(pos[1])
        #print(parsed)
        #print(pos[1],  max([max([j[1] for j in i]) for i in parsed]))
        return pos[1] > max_depth_rock
    #print(rocks)
    i = 0
    while not done:

        sand_falling = True
        temp = SANDPOSITION
        #print(len(occupied_by_sand), occupied_by_sand)
        while sand_falling:
            #print(temp)
            if in_abyss(temp):
                return len(occupied_by_sand)
            elif pos_is_free(temp+down):
                temp = temp+down
            elif pos_is_free(temp+ldiag):
                temp = temp+ldiag
            elif pos_is_free(temp+rdiag):
                temp = temp+rdiag

            else:
                occupied_by_sand.add(temp)
                sand_falling = False
        print(i)
        i+=1


def display_sand(occupied_by_sand):
    xs = [i[0] for i in occupied_by_sand]
    ys = [i[1] for i in occupied_by_sand]
    xmax = max(xs)
    xmin = min(xs)
    ymax = max(ys)
    string = ""
    for y in range(ymax):
        for x in range(xmax):
            if x > xmin:
                if Position(x, y) in occupied_by_sand:
                    string += "o"
                else:
                    string += "."
        string += "\n"
    print(string)
    return string



def parttwo(parsed):
    done = False
    rocks = set()
    for rock in parsed:
        past = None
        for part in rock:
            if past is not None:
                rocks.add(Line(past, part))
            past = part

    faster_rocks = set()
    print(len(rocks))
    for rock in rocks:
        faster_rocks.update(rock.to_set())
    print(faster_rocks)


    def pos_is_free(pos: Position):
        #print(r)
        #return pos not in occupied_by_sand and not any((pos in _rock for _rock in rocks))
        return pos not in occupied_by_sand and (pos[0], pos[1]) not in faster_rocks

    occupied_by_sand = set()
    down = Position(0,1)
    ldiag = Position(-1, 1)
    rdiag = Position(1, 1)
    max_depth_rock = max([max([j[1] for j in i]) for i in parsed])
    #floor = Line(Position(-1e9, max_depth_rock+2), Position(1e9, max_depth_rock+2))
    #rocks.add(floor)
    print(max_depth_rock)
    #print(rocks)
    i = 0
    while not done:

        sand_falling = True
        temp = SANDPOSITION
        #print(len(occupied_by_sand), occupied_by_sand)
        while sand_falling:
            #print(temp)
            if (temp+down)[1] == max_depth_rock+2:
                occupied_by_sand.add(temp)
                sand_falling = False
            elif pos_is_free(temp+down):
                temp = temp+down
            elif pos_is_free(temp+ldiag):
                temp = temp+ldiag
            elif pos_is_free(temp+rdiag):
                temp = temp+rdiag
            elif SANDPOSITION == temp:
                display_sand(occupied_by_sand)

                return len(occupied_by_sand) + 1
            else:
                occupied_by_sand.add(temp)
                sand_falling = False
        print(i, temp)
        i+=1



if __name__ == "__main__":
    real = readfile("input_real.txt")
    fake = readfile("input.txt")
    parsed = parse_input(real)
    print(parttwo(parsed))