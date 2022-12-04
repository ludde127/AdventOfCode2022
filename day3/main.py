from utils import readfile


def to_prio(char: str) -> int:
    if char.islower():
        return 1 + ord(char) - ord("a")
    else:
        return 27 + ord(char) - ord("A")


def partone():
    data = readfile("input.txt")
    sum_ = 0
    for row in data:
        first_part, second_part = set(row[:int(len(row)/2)]), set(row[int(len(row)/2):])
        intersect = first_part.intersection(second_part)
        sum_ += sum(map(lambda i: to_prio(i), intersect))
    print(sum_)


def parttwo():
    data = readfile("input.txt")
    score = 0
    group_index = 0
    group = []
    for row in data:
        if group_index <= 2:
            group.append(set(row))
        if group_index == 2:
            score += to_prio(list(group[0].intersection(group[1]).intersection(group[2]))[0])
        group_index+=1
        if group_index == 3:
            group_index = 0
            group = []
    print(score)


if __name__ == "__main__":
    parttwo()