from utils import readfile


def marker_finder(amount_unique: int) -> int:
    data = readfile("input.txt")[0]
    l = list()

    res = 0
    for (i, c) in enumerate(data):
        l.append(c)
        if len(l) >= amount_unique and len(set(l[-amount_unique:])) == amount_unique:
            res = i + 1
            break

    print(res)


def partone():
    marker_finder(4)

def parttwo():
    marker_finder(14)


if __name__ == "__main__":
    parttwo()