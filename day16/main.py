from tqdm import tqdm

from utils import readfile, Position, Line

time_limit = 30
time_cost = 1 # per opening of valve
time_cost_tunnel = 1 # per tunnel

class Tunnel:
    def __init__(self, _from, to, cost=1):
        self._from = _from
        self.to = to
        self.cost = cost

    def inc_cost(self):
        self.cost += 1

    def start_end(self):
        return self._from, self.to

    def __repr__(self):
        return f"Tunnel({self._from.name} to {self.to.name}, cost {self.cost})"

class Valve:
    def __init__(self, flow_rate: int, name: str):
        self.flow_rate = flow_rate
        self.name = name
        self.tunnels_to: dict[str, Tunnel] = dict()
        self.visited = False

    def set_visited(self):
        self.visited = True
    def add_tunnel(self, tunnel: Tunnel):
        self.tunnels_to[tunnel.to.name] = tunnel

    def remove_tunnel(self, tunnel: Tunnel):
        del self.tunnels_to[tunnel.to.name]

    def __repr__(self):
        names = [str(t) for t in self.tunnels_to.values()]
        return f"[{self.name}]|Flow-rate {self.flow_rate} to {names}"
    def __getitem__(self, item):
        if isinstance(item, str) and item.isupper():
            return self.tunnels_to[item]

    def __iter__(self):
        for v in self.tunnels_to.values():
            yield v.to

    def copy(self):
        v = Valve(self.flow_rate, self.name)
        for tunnel in self.tunnels_to.values():
            v.add_tunnel(tunnel)
        return v


class ValveHolder:
    def __init__(self, starting_pressure: int, valves: list[Valve], start: Valve, max_time: int):
        self.pressure = starting_pressure

        self.valves = valves
        self.__valve_dict = {v.name: v for v in self.valves}
        self.__start = start
        self.current: Valve = start
        self.path = [start, ]
        self.visited = set()
        self.visited.add(start)
        self.time_left = max_time
        self.__opened = set()


        self.__reversion_mode = False
        self.__revert_to = tuple()

    def __enter__(self):
        self.__reversion_mode = True
        self.__revert_to = (self.time_left, self.current, self.path.copy(), self.visited.copy(), self.__opened.copy())

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__reversion_mode = False
        self.time_left, self.current, self.path, self.visited, self.__opened = self.__revert_to

        self.__revert_to = []

    def goto(self, valve: Valve, should_open=False):
        if isinstance(valve, Valve):
            #print(list(t.to for t in self.current.tunnels_to.values()), "Cool", valve)
            try:
                tunnel = next((t for t in self.current.tunnels_to.values() if t.to.name == valve.name))
                self.time_left -= tunnel.cost
                if should_open:
                    assert not valve in self.__opened
                    self.time_left -= 1
                    self.pressure -= valve.flow_rate * self.time_left
                    self.__opened.add(valve)
                self.path.append(valve)
                self.visited.add(valve)
                self.current = valve
            except StopIteration:
                raise ValueError("Not a neighbor. ", valve, " Of ", self.current.tunnels_to.values())
        else:
            valve = self.__valve_dict[valve]
            self.goto(valve, should_open=should_open)
    def __repr__(self):
        return "-->".join([str(v) for v in self.path])

    def tunnels(self):
        for t in self.current.tunnels_to.values():
            yield t

def parse_valves(data, reduce=False):
    valves = dict()
    tunnels = dict()

    def reduce_func(valve: Valve, tunnel_now: Tunnel, depth=1) -> list[Tunnel]:
        new_tunnels = list()
        valve_from, valve_to = tunnel_now.start_end()
        if valve_to.flow_rate:
            new_tunnels.append(Tunnel(valve, valve_to, depth))
        else:
            #print(valve_to)
            for next_step in valve_to.tunnels_to.values():
                if next_step.to != valve_from:
                    new_tunnels.extend(reduce_func(valve, next_step, depth+1))

        return new_tunnels

    for row in data:
        valve, _tunnels = row.split(";")
        valve_name = valve.split(" ")[1]
        valve_flow_rate = int(valve.split(" ")[-1].split("=")[-1])
        tunnels_to = set()
        for word in _tunnels.split(" "):
            word: str = word.replace(",", "")
            if len(word) and word.isupper():
                tunnels_to.add(word)
        tunnels[valve_name] = tunnels_to
        valves[valve_name]=Valve(valve_flow_rate, valve_name)

    for valve in valves.values():
        valves_tunnels = tunnels[valve.name]

        for tunnel in valves_tunnels:

            valve.add_tunnel(Tunnel(_from=valve, to=valves[tunnel]))

    if reduce:
        new_valves = dict()
        for valve in valves.values():
            temp_valve = valve.copy()
            for t in valve.tunnels_to.values():
                if not t.to.flow_rate and not t.to == valve:
                    temp_valve.remove_tunnel(t)
                    for r in reduce_func(valve, t, 1):
                        temp_valve.add_tunnel(r)
                elif t.to == valve:
                    temp_valve.remove_tunnel(t)
            new_valves[valve.name] = temp_valve

        return new_valves
    return valves

def partone(valves: ValveHolder):

    #def dfs(current, time_left, visited, )
    with valves:
        while 0 < valves.time_left:
            best = None
            best_score = 0
            for tunnel in valves.tunnels():
                s = tunnel.to.flow_rate/tunnel.cost
                if s > best_score or best is None:
                    best_score = s
                    best = tunnel

            valves.goto(best.to, not best.to)

if __name__ == "__main__":
    example = readfile("input.txt")
    real = readfile("input_real.txt")
    parsed = parse_valves(example, reduce=True)
    valve_AA = parsed["AA"]
    valves = ValveHolder(starting_pressure=0, valves=list(parsed.values()), start=parsed["AA"], max_time=30)
    print(valves)
    partone(valves)
