import time

from utils import  readfile
from ast import literal_eval
from functools import cmp_to_key
def partone(data):
    pairs = extract_pairs(data)
    #print(pairs)
    i = 1
    summed = 0
    for pair in pairs:
        comp = top_level_compare(*pair)
        if comp:
            print(i)

            summed+=i
        i+=1

    print("summed ", summed)
    return summed

def parttwo(data: list[str]):
    t0 = time.time()
    data = [d for d in data if d]
    ind1 = "[[2]]"
    ind2 = "[[6]]"
    data.append(ind1)
    data.append(ind2)
    data.sort(key=cmp_to_key(lambda a,b: compare_pair(literal_eval(a), literal_eval(b))), reverse=True)

    ind1index = None
    ind2index = None

    for (i, d) in enumerate(data):
        if d == ind1:
            ind1index = i+1
        elif d == ind2:
            ind2index = i+1
    t1 = time.time()
    print("\n".join(data))
    print(ind1index, ind2index)
    print(ind1index*ind2index)
    print(t1-t0)


def run_over_data(data):
    pairs = extract_pairs(data)
    # print(pairs)

    for pair in pairs:
        yield top_level_compare(*pair)
def top_level_compare(left: str, right: str) -> bool:
    left = literal_eval(left)
    right = literal_eval(right)
    comp = compare_pair(left, right)
    return comp != -1

def compare_pair(left: list | int, right: list | int) -> int:

    """Return 1 if they are in correct order 0 if same"""
    if isinstance(left, int) and isinstance(right, int):
        if right < left:
            return -1
        elif right == left:
            return 0
        elif right > left:
            return 1
    elif isinstance(left, int) != isinstance(right, int):
        # One is int
        if isinstance(left, int):
            return compare_pair([left, ], right)
        else:
            return compare_pair(left, [right, ])
    elif isinstance(left, list) and isinstance(right, list):
        for i in range(max(len(left), len(right))):
            try:
                left_item = left[i]
            except IndexError:
                try:
                    right_item = right[i]
                    return 1
                except IndexError:
                    return -1
            try:
                right_item = right[i]
            except IndexError:
                return -1

            comp = compare_pair(left_item, right_item)
            if comp == -1:
                return -1
            elif comp == 1:
                return 1

    else:
        print(left, right)
        assert False
    return 0
def extract_pairs(data):
    pairs = list()
    current_pair = list()
    for row in [r for r in data if r]:
        if len(current_pair) == 2:
            pairs.append(current_pair)
            current_pair = list()
        current_pair.append(row)
    if len(current_pair) == 2:
        pairs.append(current_pair)
    return pairs

if __name__ == "__main__":
    example = readfile("input.txt")
    real = readfile("input_real.txt")
    hugos = readfile("hugos.txt")
    parttwo(real) # 645 is to low # to low 2313 lower than 6081 3920 incorrect.