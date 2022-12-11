from typing import Optional, Iterable

from tqdm import tqdm
from utils import readfile

def parse_monkeys(data: Iterable[str]):
    monkes = list()
    monke = list()
    test = list()
    for row in data:
        if row.startswith("Monkey") and len(monke) > 0:
            monke.append(test)
            monkes.append(Monke(monke[0], monke[1], monke[2]))
            monke = list()
            test = list()
        elif row.startswith("Starting"):
            l = [int(i) for i in row.split(":")[1].strip().split(", ")]
            monke.append(l)
        elif row.startswith("Operation"):
            monke.append(row.split(":")[1].strip())
        elif row.startswith("Test"):
            test.append(row.split(":")[1].strip())
        elif len(test) != 0 and row:
            test.append(row)
        elif row.startswith("Monkey 0:"):
            pass
        else:
            assert not row, "This should only be here if empty not " + row
    if len(monke) > 1:
        monke.append(test)
        monkes.append(Monke(monke[0], monke[1], monke[2]))

    return monkes
class Monke:
    def __init__(self, starting_items, op, test):
        self.items = starting_items
        self.op = op
        self.test = test
        self.inspects = 0
        self.div_by_num = int(self.test[0].split(" ")[-1])


    def apply_op(self, worry):
        op = self.op.split("=")[1]
        if "+" in op:
            to_add = [o.strip() for o in op.split("+")]
            if to_add[0] == "old":
                if to_add[1] != "old":
                    worry += int(to_add[1])

                else:
                    worry *= 2
            else:
                raise ValueError(op)
        elif "*" in op:
            todo = [o.strip() for o in op.split("*")]
            if todo[0] == "old":
                if todo[1] == "old":
                    worry *= worry
                else:
                    worry *= int(todo[1])
        return worry
    def inspect_one_item(self):
        item = self.items.pop(0)
        worry = self.apply_op(item)
        worry = worry//3
        self.inspects += 1
        return self.run_test(worry), worry

    def inspect_one_item_2(self, mod_to_use):
        item = self.items.pop(0)
        worry = self.apply_op(item)
        worry = worry % mod_to_use
        self.inspects += 1
        return self.run_test(worry), worry
    def run_test(self, worry) -> int:
        if worry % self.div_by_num == 0:
            return int(self.test[1].split(" ")[-1])
        else:
            return int(self.test[2].split(" ")[-1])


class MonkeMaster:
    def __init__(self, monkes):
        self.monkes = monkes
        self.rounds = 0

    def run_round(self):
        m = 1
        t = [m.div_by_num for m in self.monkes]
        for i in t:
            m*=i
        for monke in self.monkes:
            for _ in list(monke.items):
                give_to, item = monke.inspect_one_item_2(mod_to_use=m)
                self.monkes[give_to].items.append(item)
            assert len(monke.items) == 0
        self.rounds += 1
    def __repr__(self):
        text = f"Round {self.rounds}:\n"
        for (i, monke) in enumerate(self.monkes):
            text += f"Monkey {i}: {', '.join((str(i) for i in monke.items))}, Inspected {monke.inspects}\n"
        return text
def partone(monkes):
    num = 10000
    for i in tqdm(range(num), total=num):
        monkes.run_round()

    monke_business = sorted([m.inspects for m in monkes.monkes], reverse=True)
    print(monkes)
    print(monke_business[0] * monke_business[1])

if __name__ == "__main__":
    real_data = readfile("input_real.txt")
    data = readfile("input.txt")
    monkes =  MonkeMaster(parse_monkeys(readfile("input_real.txt")))

    partone(monkes) # 1466 wrong, too low
