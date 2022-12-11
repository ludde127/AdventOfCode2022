from typing import Optional

from utils import readfile

def partone(data):
    x = 1
    cycle = 0
    signal_strengths = list()
    def inc_cycle(cycle):
        cycle += 1
        if cycle == 20:
            signal_strengths.append((cycle, cycle * x))
        elif cycle >= 60 and (cycle-20) % 40 == 0:
            signal_strengths.append((cycle, cycle * x))
        return cycle

    for row in data:
        if row.startswith("addx"):
            cycle = inc_cycle(cycle)
            cycle = inc_cycle(cycle)

            x += int(row.split(" ")[1])
        elif row.startswith("noop"):
            cycle = inc_cycle(cycle)
        else:
            assert False, row

    print(signal_strengths)
    print(sum([a[1] for a in signal_strengths]))

def parttwo(data):
    x = 1 # Middle of a sprite, sprite is xXx where larger x is at var x pos.
    cycle = 0
    x_width = 40

    image = ""
    last_y = 0
    def cycle_to_pixel():
        _y = int(cycle/x_width)
        _x = cycle - _y * x_width
        return _x, _y

    def draw(image, _x, _y, last_y):
        if last_y != _y:
            image += "\n"
            last_y = _y
        if _x in range(x-1, x+2):
            image += "#"
        else:
            image += "."
        return image, last_y

    def inc_cycle(cycle, image, last_y):
        cycle += 1

        image, last_y = draw(image, *cycle_to_pixel(), last_y)
        return cycle, image, last_y

    for row in data:
        if row.startswith("addx"):
            cycle, image, last_y = inc_cycle(cycle, image, last_y)
            cycle, image, last_y = inc_cycle(cycle, image, last_y)

            x += int(row.split(" ")[1])
        elif row.startswith("noop"):
            cycle, image, last_y = inc_cycle(cycle, image, last_y)
        else:
            assert False, row

    print(image)

if __name__ == "__main__":
    real_data = readfile("input_real.txt")
    data = readfile("input.txt") # 6097 to low, 8k to high 6098 correct
    parttwo(real_data) # 1466 wrong, too low
