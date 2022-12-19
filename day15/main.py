from tqdm import tqdm

from utils import readfile, Position, Line

class Sensor:
    def __init__(self, pos: Position, max_dist: int):
        self.pos = pos
        self.pos_x, self.pos_y = pos.x, pos.y

        self.max_dist = abs(max_dist)

    def __contains__(self, item):
        #assert (isinstance(item, Position))
        return self.max_dist >= item.manhattan_distance(self.pos)

    def where_to(self, p):
        if p.x == self.pos_x:
            return p.x+1

        to = self.pos_x + abs(self.pos_x-p.x) + 1
        if to -p.x > 1:
            print(to-p.x, to, p)
        return to


def parse_sensor_beacon(data):
    sensors = list()
    beacons = list()
    sender_to_beacon = dict()
    for row in data:
        sens, beac = row.split(":")
        sx = int(sens.split(", ")[0].split("=")[1])
        sy = int(sens.split(", ")[1].split("=")[1])

        bx = int(beac.split(", ")[0].split("=")[1])
        by = int(beac.split(", ")[1].split("=")[1])
        sensors.append(Sensor(Position(sx, sy), max_dist=Position(sx, sy).manhattan_distance(Position(bx, by))))
        beacons.append(Position(bx, by))
        sender_to_beacon[Position(sx, sy)] = Position(bx, by)

    return sensors, beacons, sender_to_beacon





def partone(data, row=10):
    sensors, beacons, sender_to_beacon = parse_sensor_beacon(data)
    every = set(sensors)

    every.update(beacons)
    #impossible_lines = find_impossible(closest)


    sensors = list()
    for sensor in sender_to_beacon.keys():
        dist = sensor.manhattan_distance(sender_to_beacon[sensor])
        sensors.append(Sensor(sensor, dist))


    def in_any_sensor(p):
        for s in sensors:
            if p in s:
                return True
        return False

    #y10 = [i for i in impossible if i.y==10]
    #print(len(y10))
    minimum_x = min((e.x for e in beacons)) - 4000000
    maximum_x = max((e.x for e in beacons)) + 4000000

    print("Checking points")
    #print(every)
    impossible = set()
    t = tqdm(total=maximum_x+abs(minimum_x))
    for x in range(minimum_x, maximum_x+1):
        p = Position(x, row)
        #print(p)
        if in_any_sensor(p) and p not in beacons:
            impossible.add(p)
        t.update(1)
    #print(impossible)
    print(len(impossible))

def parttwo(data, limit=20):
    sensors, beacons, sender_to_beacon = parse_sensor_beacon(data)
    every = set(sensors)

    every.update(beacons)
    # impossible_lines = find_impossible(closest)

    sensors: list[Sensor] = list()
    for sensor in sender_to_beacon.keys():
        dist = sensor.manhattan_distance(sender_to_beacon[sensor])
        sensors.append(Sensor(sensor, dist, max_width=max(abs(sensor.x-sender_to_beacon[sensor].x), abs(sensor.y-sender_to_beacon[sensor].y))))

    def in_any_sensor(p):
        for s in sensors:
            if p in s:
                #print(p.x)
                to = s.where_to(p)
                #print("-->", to)
                return True, to
        #print("HUH")
        return False, p.x

    print("Checking points")
    # print(every)
    t = tqdm(total=limit)
    for y in range(limit):
        x = 0
        while x <= limit:
            p = Position(x, y)
            # print(p)
            is_in, end = in_any_sensor(p)
            if is_in:

                #print(x)
                x = end
                #print(x)
            else:
                return p


        t.update(1)

    return


def find_impossible(closest) -> set[Line]:
    print("Building lines")
    impossible = set()
    for sensor in tqdm(closest.keys(), total=len(closest.keys())):

        beacon = closest[sensor]  # Beacon
        dist = beacon.manhattan_distance(sensor)  # Beacon to sensor
        delta = abs(beacon-sensor)

        xy_abs_range = Position(delta.y-dist, delta.x-dist)
        #print(xy_abs_range)
        # CHECK RAND
        y = -(delta.x-dist)
        for x in range(sensor.x-abs(xy_abs_range.x), sensor.x+abs(xy_abs_range.x)+1):
            impossible.add(Line(Position(x, y), Position(x, -y)))
            y += 1


        #print(sensor)
    print("Build lines ", len(impossible))
    return impossible


def parttwo_monke(data, limit = 20):
    sensors, beacons, sender_to_beacon = parse_sensor_beacon(data)
    every = set(sensors)

    every.update(beacons)
    # impossible_lines = find_impossible(closest)
    def any_contains_it(pos: Position):
        for sens in sensors:
            if pos in sens:
                return True
        return False

    for sensor in tqdm(sensors, total=len(sensors)):
        x = sensor.pos_x - sensor.max_dist -1
        y = 0
        #print(sensor.max_dist, sensor.pos, x, y)

        assert not Position(x, sensor.pos_y+y) in sensor
        while x <= sensor.pos_x + sensor.max_dist and x <= limit:
            #print(x, y)
            yplus=sensor.pos_y+y
            yminus=sensor.pos_y-y

            cond_plus = limit >= x >= 0 and limit >= yplus >= 0
            cond_minus = limit >= x >= 0 and limit >= yminus >= 0

            if x < sensor.pos_x:
                if not any_contains_it(Position(x, yplus)) and cond_plus:
                    return Position(x, yplus)
                if not any_contains_it(Position(x, yminus)) and cond_minus:
                    return Position(x, yminus)

                y += 1
            else:
                #print("RIGHT OVER")
                if not any_contains_it(Position(x, yplus)) and cond_plus:
                    return Position(x, yplus)
                if not any_contains_it(Position(x, yminus)) and cond_minus:
                    return Position(x, yminus)
                y -= 1
            x += 1


if __name__ == "__main__":
    example = readfile("input.txt")
    real = readfile("input_real.txt")
    p1 = 2000000 # 4640520 TO LOW 4660320 to low
    res = parttwo_monke(real, limit=int(4 * 1e6))
    print(res)
    print(res.x*4000000+res.y)
    #partone(example, 10)