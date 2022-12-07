from pprint import pprint

from utils import readfile
from pathlib import Path


class Dir:
    def __init__(self, path: str, past_dir=None):
        self.path = path
        self.files = []
        self.dirs = []
        self.past_dir = past_dir

    def __str__(self):
        d = '\n--'.join((str(d) for d in self.dirs))
        return f"{self.path} Files {self.files}\n DIRS {d}"

    def __repr__(self):
        return self.__str__()

    def total_size(self):
        size = 0
        for file in self.files:
            size += int(file.split(" ")[0])
        for dir in self.dirs:
            size += dir.total_size()
        #print(f"{self.path}, {size}")
        #print(self.files)
        #print(self.dirs)
        return size

    def all_sizes(self):
        size = 0
        for file in self.files:
            size += int(file.split(" ")[0])
        for dir in self.dirs:
            size += dir.total_size()
        yield (self.path, size)
        for dir in self.dirs:
            for i in dir.all_sizes():
                yield i


def parse():
    data = readfile("input.txt", strip=True)
    current_path = "/"
    full_tree = Dir("/")
    current_dir = full_tree
    ls_mode = False
    for row in data:
        if row[0] == "$":
            ls_mode = False
            if "cd /" in row:
                current_path = "/"
                current_dir = full_tree
            elif "cd .." in row:
                current_path = current_path.rsplit("/", 2)[0] + "/"
                if current_dir.past_dir:
                    current_dir = current_dir.past_dir
            elif "cd" in row:
                dir_to = row.split(" ")[2]
                current_path += dir_to + "/"
                if Dir(dir_to, current_dir) not in current_dir.dirs:
                    last = current_dir
                    current_dir = Dir(dir_to, current_dir)
                    last.dirs.append(current_dir)
                else:
                    current_dir = [d for d in current_dir.dirs if d.path == dir_to][0]
            elif "ls" in row:
                ls_mode = True
            continue
        elif ls_mode:
            if "dir" == row[:3]:
                d = Dir(row[4:].strip(), current_dir)
                if d not in current_dir.dirs:
                    current_dir.dirs.append(d)
            else:
                current_dir.files.append(row.strip())
        else:
            assert False
    return full_tree


def partone():
    full_tree = parse()
    tot = 0
    for (p, s) in list(full_tree.all_sizes()):
        if s <= 100000:
            tot += s
    print(tot)


def parttwo():
    full_tree = parse()
    total_size = 70000000
    need = 30000000
    used = full_tree.total_size()
    available = total_size - used
    free_up = need - available

    possible = list()
    possible.append(10000000000000000)
    for (p, s) in list(full_tree.all_sizes()):
        if free_up <= s <= min(possible):
            possible.append(s)
    print(free_up)
    print(min(possible))


if __name__ == "__main__":
    parttwo()