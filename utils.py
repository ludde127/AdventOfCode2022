import functools
def readfile(path: str, strip=True) -> list[str]:
    with open(path, "r") as f:
        if strip:
            return [l.strip() for l in f.readlines()]
        else:
            return list(f.readlines())

class Position:
    def __init__(self, *args):
        self.coordinates = [int(i) for i in args]

    def __add__(self, other):
        assert isinstance(other, Position)

        coords = [a+b for (a,b) in zip(self.coordinates, other.coordinates)]
        return Position(*coords)

    def __sub__(self, other):
        assert isinstance(other, Position)

        coords = [a - b for (a, b) in zip(self.coordinates, other.coordinates)]
        return Position(*coords)

    def __repr__(self):
        return "Point("+", ".join([str(i) for i in self.coordinates]) +")"

    def __eq__(self, other):
        return isinstance(other, Position) and other.coordinates == self.coordinates

    def __getitem__(self, item):
        return self.coordinates[item]

    def __abs__(self):
        return Position(*[abs(e) for e in self.coordinates])

    def __hash__(self):
        return tuple(self.coordinates).__hash__()

    def manhattan_distance(self, other):
        return abs(self.coordinates[0]-other[0])+abs(self.coordinates[1]-other[1])

    @property
    def x(self):
        return self.coordinates[0]

    @property
    def y(self):
        return self.coordinates[1]


class Line:
    def __init__(self, point1: Position, point2: Position):
        assert len(point1.coordinates) == len(point2.coordinates)
        self.pos1 = point1
        self.pos2 = point2
        self.ranges = [range(min(self.pos1[i], self.pos2[i]), max(self.pos1[i], self.pos2[i])+1) for i in range(len(point1.coordinates))]

    @functools.lru_cache(3500)
    def __contains__(self, item: Position):
        # THIS IS SLOW
        return all((item[i] in range for (i, range) in enumerate(self.ranges)))

    def __repr__(self):
        return f"{self.pos1}-->{self.pos2}"

    def to_set(self):
        assert isinstance(self.pos1[0], int)
        assert len(self.ranges) == 2, "Pallade inte br??nna min hj??rna"
        points = set()

        if len(self.ranges[0]) == 1:
            return {(list(self.ranges[0])[0], y) for y in self.ranges[1]}
        elif len(self.ranges[1]) == 1:
            return {(x, list(self.ranges[1])[0]) for x in self.ranges[0]}
        else:
            assert False

    def contains_y(self, y):
        return y in self.ranges[1]

    def contains_x(self, x):
        return x in self.ranges[1]
