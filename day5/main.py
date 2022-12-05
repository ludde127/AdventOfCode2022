from utils import readfile

CRATES = {
        1: ["N", "W", "F", "R", "Z", "S", "M", "D"],
        2: ["S", "G", "Q", "P", "W"],
        3: ["C", "J", "N", "F", "Q", "V", "R", "W"],
        4: ["L", "D", "G", "C", "P", "Z", "F"],
        5: ["S", "P", "T"],
        6: ["L", "R", "W", "F", "D", "H"],
        7: ["C", "D", "N", "Z"],
        8: ["Q", "J", "S", "V", "F", "R", "N", "W"],
        9: ["V", "W", "Z", "G", "S", "M", "R"]
    }


def partone():
    data = readfile("input.txt")

    crates = {k: list(reversed(v)) for k, v in CRATES.items()}

    def move(_from, to, amount):
        for i in range(amount):
            crates[to].append(crates[_from].pop())
    for row in data:
        row = [c for c in row.replace("move", "").replace("from", "").replace("to", "").split(" ") if c]
        move(int(row[1]), int(row[2]), int(row[0]))
    print(crates)
    print([v[-1] for v in crates.values()])


def parttwo():
    data = readfile("input.txt")

    crates = {k: list(reversed(v)) for k, v in CRATES.items()}

    def move(_from, to, amount):
        temp = list()
        for i in range(amount):
            temp.append(crates[_from].pop())
        for i in reversed(temp):
            crates[to].append(i)

    for row in data:
        row = [c for c in row.replace("move", "").replace("from", "").replace("to", "").split(" ") if c]
        move(int(row[1]), int(row[2]), int(row[0]))
    print(crates)
    print([v[-1] for v in crates.values()])


if __name__ == "__main__":
    parttwo()