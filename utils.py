def readfile(path: str, strip=True) -> list[str]:
    with open(path, "r") as f:
        if strip:
            return [l.strip() for l in f.readlines()]
        else:
            return list(f.readlines())
