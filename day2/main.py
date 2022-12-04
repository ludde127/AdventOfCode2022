from utils import readfile
def partone():
    data = readfile("input.txt")
    score = 0
    score_worth = {"X": 1, "Y": 2, "Z": 3}  # ROCK PAPER SCISSOR
    draws = {"A X", "B Y", "C Z"}
    wins = {"A Y", "B Z", "C X"}
    for row in data:
        other, mine = row.split(" ")
        if row in draws:
            score += 3
        elif row in wins:
            score += 6
        score += score_worth[mine]
    print(score)


def parttwo():
    data = readfile("input.txt")
    score = 0
    score_worth = {"X": 1, "Y": 2, "Z": 3}  # ROCK PAPER SCISSOR
    lose_draw_win = {"A": "ZXY", "B": "XYZ", "C": "YZX"}
    for row in data:
        other, mine = row.split(" ")
        choice = lose_draw_win[other][lose_draw_win["B"].find(mine)]
        score += 3 * lose_draw_win["B"].find(mine) + score_worth[choice]
    print(score)


if __name__ == "__main__":
    parttwo()