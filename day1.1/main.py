def readfile(path: str) -> list[str]:
    with open(path, "r") as f:
        return [l.strip() for l in f.readlines()]


if __name__ == "__main__":
    input = readfile("input.txt")
    elves = list()
    current_elve = 0
    for row in input:
        if row:
            if current_elve >= len(elves):
                elves.append(0)
                elves[current_elve] = int(row)
            else:
                elves[current_elve] += int(row)
        else:

            current_elve+=1
    print(max(elves))

    print(sum(sorted(elves, reverse=True)[0:3]))
