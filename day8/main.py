from pprint import pprint

from utils import readfile
import seaborn as sns
import matplotlib.pyplot as plt

class Tree:
    def __init__(self, x, y, left=None, right=None, up=None, down=None):
        self.x = x
        self.y = y

        self.left = left
        self.right = right
        self.up = up
        self.down = down

    def __eq__(self, other):
        if isinstance(other, Tree):
            return self.x == other.x and self.y == other.y
        return False




def slow_part_one(data):
    # O(n**2)
    visible_trees = list()

    def is_visible(x, y, num):
        left = [int(t.strip()) for (i, t) in enumerate(data[y]) if i < x]
        upper = [int(t[x].strip()) for (i, t) in enumerate(data) if i < y]

        right = [int(t.strip()) for (i, t) in enumerate(data[y]) if i > x]
        lower = [int(t[x].strip()) for (i, t) in enumerate(data) if i > y]

        return all([i < num for i in left]) or\
               all([i < num for i in upper]) or\
               all([i < num for i in right]) or\
               all([i < num for i in lower])

    for (y, horizontal) in enumerate(data):
        for (x, num) in enumerate(horizontal):
            if num:
                num = int(num)
                if is_visible(x, y, num):
                    visible_trees.append((x, y))
            else:
                assert False

    def lower_limit():
        return len(data) * 2 + len(data[0]) * 2 - 4
    print("\n".join(data))
    print(len(visible_trees))



    #print(lower_limit())
def parttwo(data):
    scores = {}

    def tree_to_key(x, y):
        return str(x) + ":" + str(y)

    def score_of_tree(x, y, height):
        factors = 1
        for dir in ["left", "right"]:
            depth = 0

            for _x in range(1, len(data[0])):

                if dir == "left":
                    if x-_x < 0:
                        break

                    tree = int(data[y][x-_x])
                else:
                    if x+_x >= len(data[0]):
                        break
                    tree = int(data[y][x+_x])
                depth += 1
                if tree >= height:
                    break

            if depth == 0:
                return 0
            factors *= depth

        for dir in ["up", "down"]:
            depth = 0
            for _y in range(1, len(data)):
                if dir == "up":
                    if y - _y < 0:
                        break
                    tree = int(data[y-_y][x])
                else:
                    if y + _y >= len(data[0]):
                        break
                    tree = int(data[y+_y][x])
                depth += 1
                if tree >= height:
                    break

            if depth == 0:
                return 0
            factors *= depth
        return factors

    for x in range(0, len(data[0])):
        for y in range(0, len(data)):
            tree = data[y][x]
            scores[tree_to_key(x, y)] = score_of_tree(x, y, int(tree))

    print(scores)
    """assert scores[tree_to_key(0, 0)] == 0
    assert scores[tree_to_key(2, 1)] == 4
    assert scores[tree_to_key(2, 3)] == 8"""
    print(sorted(scores.items(), key=lambda t: -t[1])[:5])

if __name__ == "__main__":

    """data = ["30373",
            "25512",
            "65332",
            "33549",
            "35390"]"""
    data = readfile("input.txt")
    parttwo(data) # 1118 wrong