from utils import readfile


def partone():
    data = readfile("input.txt")
    total_overlaps = 0
    for left, right in [l.split(",") for l in data]:
        left_begin, left_end = left.split("-")
        right_begin, right_end = right.split("-")
        if int(left_begin) <= int(right_begin) and int(right_end) <= int(left_end):
            total_overlaps += 1
        elif int(right_begin) <= int(left_begin) and int(left_end) <= int(right_end):
            total_overlaps += 1
    print(total_overlaps)


def parttwo():
    data = readfile("input.txt")
    partial = 0
    for left, right in [l.split(",") for l in data]:
        left_begin, left_end = left.split("-")
        right_begin, right_end = right.split("-")
        rang = set(range(int(left_begin), int(left_end)+1))
        if any((c in rang for c in range(int(right_begin), int(right_end)+1))):
            partial+=1
    print(partial)

if __name__ == "__main__":
    parttwo()