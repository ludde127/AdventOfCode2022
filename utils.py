def readfile(path: str) -> list[str]:
    with open(path, "r") as f:
        return [l.strip() for l in f.readlines()]