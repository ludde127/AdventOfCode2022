from typing import Optional

from utils import readfile
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('QtAgg')

def partone(data):
    #HEAD MUST TOUCH TAIL, DIAGONAL IS OK
    size = 32
    array = np.ndarray((size, size))
    visited_positions = list()
    starting_pos = (size//2, size//2)
    head = starting_pos
    tail = starting_pos
    visited_positions.append(starting_pos)

    def move(direction, head, tail):
        # Move one step to dir
        old_pos = head
        print(direction, "head")

        match direction:
            case "D":
                head = (head[0], head[1] - 1)
            case "R":
                head = (head[0]+1, head[1])
            case "L":
                head = (head[0] - 1, head[1])
            case "U":
                head = (head[0], head[1] + 1)
            case _:
                assert False, "Should not get here " + direction
        if not is_touching(head[0], head[1], tail[0], tail[1]):
            tail = old_pos
            visited_positions.append(tail)
            array[tail[0]][tail[1]] = len(visited_positions)
            print(direction, "TAIL")
        assert head != old_pos
        return head, tail

    for row in data:
        direction, distance = row.split(" ")
        distance = int(distance)
        for _ in range(distance):
            head, tail = move(direction, head, tail)
    print(visited_positions)
    print(len(set(visited_positions)))
    sns.heatmap(array)
    plt.show()

def parttwo(data):
    #HEAD MUST TOUCH TAIL, DIAGONAL IS OK
    size = 30
    array = np.ndarray((size, size))
    visited_positions = list()
    starting_pos = (size // 2, size // 2)
    head = starting_pos
    tails = [starting_pos for _ in range(9)]

    visited_positions.append(starting_pos)

    def move(direction, head, tails):
        # Move one step to dir
        old_pos = head
        #print(direction, "head")

        match direction:
            case "D":
                head = (head[0], head[1] - 1)
            case "R":
                head = (head[0]+1, head[1])
            case "L":
                head = (head[0] - 1, head[1])
            case "U":
                head = (head[0], head[1] + 1)
            case _:
                assert False, "Should not get here " + direction
        past_tail_spot = old_pos
        for (i, tail) in enumerate(tails):
            if i == 0:
                if not is_touching(head[0], head[1], tail[0], tail[1]):
                    tails[i] = past_tail_spot
                else:
                    break
            else:
                if not is_touching(tails[i-1][0], tails[i-1][1], tail[0], tail[1]):
                    tails[i] = past_tail_spot
                else:
                    break

                    #print(tails[i], i)
            if i == len(tails)-1:
                visited_positions.append(tails[i])
                print(len(visited_positions))
                array[tails[i]] = len(visited_positions)
            past_tail_spot = tails[i]
        assert head != old_pos
        return head, tails

    for row in data:
        direction, distance = row.split(" ")
        distance = int(distance)
        for _ in range(distance):
            head, tails = move(direction, head, tails)


    print(visited_positions)
    print(len(set(visited_positions)))
    sns.heatmap(array)
    plt.show()

def parttwo_two(data):
    size = 30
    array = np.ndarray((size, size))
    visited_positions = list()
    starting_pos = (size // 2, size // 2)
    head = starting_pos
    tails = [starting_pos for _ in range(9)]

    visited_positions.append(starting_pos)
    def move(direction, head, tails):
        # Move one step to dir
        old_pos = head
        #print(direction, "head")

        match direction:
            case "D":
                head = (head[0], head[1] - 1)
            case "R":
                head = (head[0]+1, head[1])
            case "L":
                head = (head[0] - 1, head[1])
            case "U":
                head = (head[0], head[1] + 1)
            case _:
                assert False, "Should not get here " + direction
        past_tail_spot = old_pos
        for (n, tail) in enumerate(tails):
            if not is_touching(tail[0], tail[1], past_tail_spot[0], past_tail_spot[1]):
                tails[n] = past_tail_spot
                if n == len(tails) - 1:
                    visited_positions.append(tails[n])
            past_tail_spot = tail

        return head, tails

    for row in data:
        direction, distance = row.split(" ")
        distance = int(distance)
        for _ in range(distance):
            head, tails = move(direction, head, tails)


    print(visited_positions)
    print(len(set(visited_positions)))
    sns.heatmap(array)
    plt.show()

def partone2(data):
    starting_state = (0,0)
    head = Rope(*starting_state)
    tail = head.add_knots(1)
    visited_positions = list()
    visited_positions.append(starting_state)
    for row in data:
        direction, distance = row.split(" ")
        distance = int(distance)
        for _ in range(distance):
            head.move(direction)
            visited_positions.append((tail.x, tail.y))
    print(len(set(visited_positions)))
    head.display()


def distance(x1, y1, x2, y2):
    return np.hypot(x1-x2, y1-y2)

def is_touching(x1, y1, x2, y2):
    return np.hypot(x1-x2, y1-y2) <= np.sqrt(2) + 0.01


class Rope:
    def __init__(self, x, y, parent=None):
        self.parent = parent
        self.child: Optional[Rope] = None
        self.x = x
        self.y = y
        self.visited_positions = [(x, y), ]

    def add_knots(self, n: int):
        assert not self.parent

        current_tail = self
        for _ in range(n):
            current_tail.child = Rope(current_tail.x, current_tail.y, current_tail)
            current_tail = current_tail.child
        return current_tail

    def distance_to_parent(self):
        return distance(self.x, self.y, self.parent.x, self.parent.y)

    def distance_to_child(self):
        return distance(self.x, self.y, self.child.x, self.child.y)

    def new_pos_dont_move(self, direction):
        match direction:
            case "D":
                return (self.x, self.y - 1)
            case "R":
                return (self.x + 1, self.y)
            case "L":
                return (self.x - 1, self.y)
            case "U":
                return (self.x, self.y + 1)
            case "UR":
                return (self.x + 1, self.y + 1)
            case "DR":
                return (self.x + 1, self.y - 1)
            case "UL":
                return (self.x - 1, self.y + 1)
            case "DL":
                return (self.x - 1, self.y - 1)
            case _:
                assert False, "Should not get here " + direction
    def dirs(self):
        return ["D", "R", "L", "U", "UR", "DR", "UL", "DL"]
    def move(self, direction):
        if self.parent and self.distance_to_parent() > np.sqrt(2)-0.02:
            x, y = 0, 0
            for dir in self.dirs()[4:]:
                x, y = self.new_pos_dont_move(dir)
                if distance(x, y, self.parent.x, self.parent.y):
                    direction = dir
                    break
            self.x, self.y = x, y

        elif not self.parent or self.distance_to_parent() == 1:
                self.x, self.y = self.new_pos_dont_move(direction)
                self.visited_positions.append((self.x, self.y))
        if not self.parent or not self.child:
            print("PARENT" if not self.parent else "CHILD", self.visited_positions[-1])

        if self.child and not is_touching(self.x, self.y, self.child.x, self.child.y):
            self.child.move(direction)



def parttwo2(data):
    starting_state = (0,0)
    head = Rope(*starting_state)
    tail = head.add_knots(2)
    for row in data:
        direction, distance = row.split(" ")
        distance = int(distance)
        for _ in range(distance):
            head.move(direction)
    print(tail.visited_positions)
    assert (s:=len(set(tail.visited_positions))) == 36, "WTF SHOULD BE 36 got " + str(s)


if __name__ == "__main__":
    real_data = readfile("input_real.txt")
    data = readfile("input.txt") # 6097 to low, 8k to high 6098 correct
    parttwo2(data) # 1466 wrong, too low
